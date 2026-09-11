"""Audit de conformité ISO/IEC 27001 pour l'infrastructure AWS de NovaDistrib.

Chaque fonction `check_*` interroge l'API AWS via boto3 et retourne un `ControlResult`
indiquant si le contrôle correspondant de l'annexe A est respecté. Les fonctions prennent
un client boto3 en paramètre plutôt que de le construire elles-mêmes, afin de rester
testables indépendamment (voir tests/test_aws_compliance_check.py, qui utilise `moto`
pour simuler AWS sans compte réel).

Utilisation :
    python aws_compliance_check.py
    echo $?   # 0 si tous les contrôles sont conformes, 1 sinon
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError


@dataclass
class ControlResult:
    control_id: str
    control_name: str
    passed: bool
    message: str


def check_root_mfa(iam_client) -> ControlResult:
    """Contrôle 8.2/8.5 — le compte racine doit avoir le MFA activé (risque R1)."""
    summary = iam_client.get_account_summary()["SummaryMap"]
    has_mfa = summary.get("AccountMFAEnabled", 0) == 1
    return ControlResult(
        control_id="8.2 / 8.5",
        control_name="MFA activé sur le compte racine",
        passed=has_mfa,
        message=(
            "Le compte racine a le MFA activé."
            if has_mfa
            else "Le compte racine n'a PAS de MFA activé — risque R1 (critique)."
        ),
    )


def check_iam_wildcard_policies(iam_client) -> ControlResult:
    """Contrôle 8.2 — aucune politique IAM gérée par le client ne doit accorder
    un accès total (Action="*" et Resource="*" combinés) sans justification."""
    offending: list[str] = []
    paginator = iam_client.get_paginator("list_policies")
    for page in paginator.paginate(Scope="Local"):
        for policy in page["Policies"]:
            version = iam_client.get_policy_version(
                PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"]
            )
            statements = version["PolicyVersion"]["Document"].get("Statement", [])
            if isinstance(statements, dict):
                statements = [statements]
            for statement in statements:
                if statement.get("Effect") != "Allow":
                    continue
                actions = statement.get("Action", [])
                resources = statement.get("Resource", [])
                if isinstance(actions, str):
                    actions = [actions]
                if isinstance(resources, str):
                    resources = [resources]
                if "*" in actions and "*" in resources:
                    offending.append(policy["PolicyName"])
                    break

    passed = len(offending) == 0
    return ControlResult(
        control_id="8.2",
        control_name="Absence de politiques IAM en accès total",
        passed=passed,
        message=(
            "Aucune politique IAM gérée par le client n'accorde un accès total."
            if passed
            else f"Politiques trop permissives détectées : {', '.join(offending)}"
        ),
    )


def check_password_policy(iam_client) -> ControlResult:
    """Contrôle 5.17 — la politique de mot de passe du compte doit respecter
    les exigences minimales (longueur, complexité)."""
    try:
        policy = iam_client.get_account_password_policy()["PasswordPolicy"]
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "NoSuchEntity":
            return ControlResult(
                control_id="5.17",
                control_name="Politique de mot de passe du compte",
                passed=False,
                message="Aucune politique de mot de passe n'est définie au niveau du compte.",
            )
        raise

    requirements_met = all(
        [
            policy.get("MinimumPasswordLength", 0) >= 14,
            policy.get("RequireUppercaseCharacters", False),
            policy.get("RequireLowercaseCharacters", False),
            policy.get("RequireNumbers", False),
            policy.get("RequireSymbols", False),
        ]
    )
    return ControlResult(
        control_id="5.17",
        control_name="Politique de mot de passe du compte",
        passed=requirements_met,
        message=(
            "La politique de mot de passe respecte les exigences minimales."
            if requirements_met
            else "La politique de mot de passe ne respecte pas toutes les exigences "
            "(longueur ≥ 14 caractères, complexité complète)."
        ),
    )


def check_s3_public_access(s3control_client, account_id: str) -> ControlResult:
    """Contrôle 8.12 — le blocage d'accès public S3 doit être actif au niveau du
    compte entier (risque R2)."""
    try:
        config = s3control_client.get_public_access_block(AccountId=account_id)[
            "PublicAccessBlockConfiguration"
        ]
        blocked = all(
            [
                config.get("BlockPublicAcls", False),
                config.get("IgnorePublicAcls", False),
                config.get("BlockPublicPolicy", False),
                config.get("RestrictPublicBuckets", False),
            ]
        )
    except ClientError:
        blocked = False

    return ControlResult(
        control_id="8.12",
        control_name="Blocage de l'accès public S3 au niveau du compte",
        passed=blocked,
        message=(
            "Le blocage d'accès public S3 est actif au niveau du compte."
            if blocked
            else "Le blocage d'accès public S3 n'est pas actif au niveau du compte — risque R2."
        ),
    )


def check_s3_encryption(s3_client) -> ControlResult:
    """Contrôle 8.24 — tous les compartiments S3 doivent avoir un chiffrement
    par défaut configuré."""
    buckets = s3_client.list_buckets()["Buckets"]
    unencrypted: list[str] = []
    for bucket in buckets:
        name = bucket["Name"]
        try:
            s3_client.get_bucket_encryption(Bucket=name)
        except ClientError as exc:
            if (
                exc.response["Error"]["Code"]
                == "ServerSideEncryptionConfigurationNotFoundError"
            ):
                unencrypted.append(name)
            else:
                raise

    passed = len(unencrypted) == 0
    return ControlResult(
        control_id="8.24",
        control_name="Chiffrement au repos des compartiments S3",
        passed=passed,
        message=(
            "Tous les compartiments S3 ont un chiffrement par défaut configuré."
            if passed
            else f"Compartiments sans chiffrement par défaut : {', '.join(unencrypted)}"
        ),
    )


def check_cloudtrail_enabled(cloudtrail_client) -> ControlResult:
    """Contrôle 8.15 — au moins un trail CloudTrail multi-régions doit être actif
    (risque R5)."""
    trails = cloudtrail_client.describe_trails(includeShadowTrails=True)["trailList"]
    multi_region_trails = [t for t in trails if t.get("IsMultiRegionTrail")]

    active = False
    for trail in multi_region_trails:
        status = cloudtrail_client.get_trail_status(Name=trail["TrailARN"])
        if status.get("IsLogging"):
            active = True
            break

    return ControlResult(
        control_id="8.15",
        control_name="AWS CloudTrail actif sur toutes les régions",
        passed=active,
        message=(
            "Au moins un trail CloudTrail multi-régions est actif et journalise."
            if active
            else "Aucun trail CloudTrail multi-régions actif n'a été trouvé — risque R5."
        ),
    )


def run_all_checks(session: boto3.Session | None = None) -> list[ControlResult]:
    """Exécute l'ensemble des contrôles contre le compte AWS de la session fournie."""
    session = session or boto3.Session()
    iam = session.client("iam")
    s3 = session.client("s3")
    s3control = session.client("s3control")
    cloudtrail = session.client("cloudtrail")
    account_id = session.client("sts").get_caller_identity()["Account"]

    return [
        check_root_mfa(iam),
        check_iam_wildcard_policies(iam),
        check_password_policy(iam),
        check_s3_public_access(s3control, account_id),
        check_s3_encryption(s3),
        check_cloudtrail_enabled(cloudtrail),
    ]


def print_report(results: list[ControlResult]) -> bool:
    """Affiche un rapport lisible et retourne True si tous les contrôles sont conformes."""
    passed_count = sum(r.passed for r in results)
    print("Rapport de conformite ISO/IEC 27001 -- NovaDistrib")
    print(f"{passed_count}/{len(results)} controles conformes\n")
    for result in results:
        status = "[OK]" if result.passed else "[NON CONFORME]"
        print(f"{status} [{result.control_id}] {result.control_name}")
        print(f"    {result.message}")
    return passed_count == len(results)


def main() -> None:
    results = run_all_checks()
    all_passed = print_report(results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
