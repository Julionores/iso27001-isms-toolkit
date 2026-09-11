"""Tests unitaires des contrôles de conformité, plus un test d'intégration léger
contre un compte AWS simulé par `moto` (aucun compte réel, aucun coût).

Les contrôles individuels sont testés avec des doublures (MagicMock) construites pour
reproduire précisément la forme des réponses de l'API AWS documentée par boto3 : cela
rend les tests déterministes, indépendants des évolutions de comportement de `moto` ou
d'AWS (par exemple le chiffrement S3 par défaut désormais actif côté AWS)."""

from unittest.mock import MagicMock

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_aws

from controls.aws_compliance_check import (
    ControlResult,
    check_cloudtrail_enabled,
    check_iam_wildcard_policies,
    check_password_policy,
    check_root_mfa,
    check_s3_encryption,
    check_s3_public_access,
    run_all_checks,
)


def _client_error(code: str) -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": "test"}}, "TestOperation")


# ---------------------------------------------------------------------------
# 8.2 / 8.5 -- MFA sur le compte racine
# ---------------------------------------------------------------------------


def test_check_root_mfa_passes_when_enabled():
    iam = MagicMock()
    iam.get_account_summary.return_value = {"SummaryMap": {"AccountMFAEnabled": 1}}

    result = check_root_mfa(iam)

    assert result.passed is True
    assert result.control_id == "8.2 / 8.5"


def test_check_root_mfa_fails_when_disabled():
    iam = MagicMock()
    iam.get_account_summary.return_value = {"SummaryMap": {"AccountMFAEnabled": 0}}

    result = check_root_mfa(iam)

    assert result.passed is False
    assert "R1" in result.message


# ---------------------------------------------------------------------------
# 8.2 -- politiques IAM trop permissives
# ---------------------------------------------------------------------------


def _iam_with_policy(statement: dict) -> MagicMock:
    iam = MagicMock()
    page = {
        "Policies": [
            {
                "PolicyName": "PolicySousTest",
                "Arn": "arn:aws:iam::123:policy/x",
                "DefaultVersionId": "v1",
            }
        ]
    }
    iam.get_paginator.return_value.paginate.return_value = [page]
    iam.get_policy_version.return_value = {
        "PolicyVersion": {"Document": {"Statement": [statement]}}
    }
    return iam


def test_check_iam_wildcard_policies_detects_full_access():
    iam = _iam_with_policy({"Effect": "Allow", "Action": "*", "Resource": "*"})

    result = check_iam_wildcard_policies(iam)

    assert result.passed is False
    assert "PolicySousTest" in result.message


def test_check_iam_wildcard_policies_passes_when_scoped():
    iam = _iam_with_policy(
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*",
        }
    )

    result = check_iam_wildcard_policies(iam)

    assert result.passed is True


def test_check_iam_wildcard_policies_passes_when_no_policies():
    iam = MagicMock()
    iam.get_paginator.return_value.paginate.return_value = [{"Policies": []}]

    result = check_iam_wildcard_policies(iam)

    assert result.passed is True


# ---------------------------------------------------------------------------
# 5.17 -- politique de mot de passe
# ---------------------------------------------------------------------------


def test_check_password_policy_passes_when_strong():
    iam = MagicMock()
    iam.get_account_password_policy.return_value = {
        "PasswordPolicy": {
            "MinimumPasswordLength": 14,
            "RequireUppercaseCharacters": True,
            "RequireLowercaseCharacters": True,
            "RequireNumbers": True,
            "RequireSymbols": True,
        }
    }

    result = check_password_policy(iam)

    assert result.passed is True


def test_check_password_policy_fails_when_too_short():
    iam = MagicMock()
    iam.get_account_password_policy.return_value = {
        "PasswordPolicy": {
            "MinimumPasswordLength": 8,
            "RequireUppercaseCharacters": True,
            "RequireLowercaseCharacters": True,
            "RequireNumbers": True,
            "RequireSymbols": True,
        }
    }

    result = check_password_policy(iam)

    assert result.passed is False


def test_check_password_policy_fails_when_absent():
    iam = MagicMock()
    iam.get_account_password_policy.side_effect = _client_error("NoSuchEntity")

    result = check_password_policy(iam)

    assert result.passed is False
    assert "Aucune politique" in result.message


def test_check_password_policy_reraises_unexpected_errors():
    iam = MagicMock()
    iam.get_account_password_policy.side_effect = _client_error("AccessDenied")

    with pytest.raises(ClientError):
        check_password_policy(iam)


# ---------------------------------------------------------------------------
# 8.12 -- blocage de l'accès public S3
# ---------------------------------------------------------------------------


def test_check_s3_public_access_passes_when_fully_blocked():
    s3control = MagicMock()
    s3control.get_public_access_block.return_value = {
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        }
    }

    result = check_s3_public_access(s3control, account_id="123456789012")

    assert result.passed is True


def test_check_s3_public_access_fails_when_partially_blocked():
    s3control = MagicMock()
    s3control.get_public_access_block.return_value = {
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        }
    }

    result = check_s3_public_access(s3control, account_id="123456789012")

    assert result.passed is False


def test_check_s3_public_access_fails_when_not_configured():
    s3control = MagicMock()
    s3control.get_public_access_block.side_effect = _client_error(
        "NoSuchPublicAccessBlockConfiguration"
    )

    result = check_s3_public_access(s3control, account_id="123456789012")

    assert result.passed is False


# ---------------------------------------------------------------------------
# 8.24 -- chiffrement au repos des compartiments S3
# ---------------------------------------------------------------------------


def test_check_s3_encryption_passes_when_all_encrypted():
    s3 = MagicMock()
    s3.list_buckets.return_value = {
        "Buckets": [{"Name": "bucket-a"}, {"Name": "bucket-b"}]
    }
    s3.get_bucket_encryption.return_value = {"ServerSideEncryptionConfiguration": {}}

    result = check_s3_encryption(s3)

    assert result.passed is True


def test_check_s3_encryption_fails_and_names_offending_bucket():
    s3 = MagicMock()
    s3.list_buckets.return_value = {"Buckets": [{"Name": "bucket-nue"}]}
    s3.get_bucket_encryption.side_effect = _client_error(
        "ServerSideEncryptionConfigurationNotFoundError"
    )

    result = check_s3_encryption(s3)

    assert result.passed is False
    assert "bucket-nue" in result.message


# ---------------------------------------------------------------------------
# 8.15 -- AWS CloudTrail actif
# ---------------------------------------------------------------------------


def test_check_cloudtrail_enabled_passes_when_active():
    cloudtrail = MagicMock()
    cloudtrail.describe_trails.return_value = {
        "trailList": [{"TrailARN": "arn:aws:cloudtrail:x", "IsMultiRegionTrail": True}]
    }
    cloudtrail.get_trail_status.return_value = {"IsLogging": True}

    result = check_cloudtrail_enabled(cloudtrail)

    assert result.passed is True


def test_check_cloudtrail_enabled_fails_when_not_logging():
    cloudtrail = MagicMock()
    cloudtrail.describe_trails.return_value = {
        "trailList": [{"TrailARN": "arn:aws:cloudtrail:x", "IsMultiRegionTrail": True}]
    }
    cloudtrail.get_trail_status.return_value = {"IsLogging": False}

    result = check_cloudtrail_enabled(cloudtrail)

    assert result.passed is False


def test_check_cloudtrail_enabled_fails_when_single_region_only():
    cloudtrail = MagicMock()
    cloudtrail.describe_trails.return_value = {
        "trailList": [{"TrailARN": "arn:aws:cloudtrail:x", "IsMultiRegionTrail": False}]
    }

    result = check_cloudtrail_enabled(cloudtrail)

    assert result.passed is False


# ---------------------------------------------------------------------------
# Test d'intégration léger : le pipeline complet s'exécute contre un compte
# AWS entièrement simulé par moto, sans toucher au réseau ni à un vrai compte.
# ---------------------------------------------------------------------------


@mock_aws
def test_run_all_checks_executes_end_to_end_against_simulated_account():
    session = boto3.Session(region_name="eu-west-3")

    results = run_all_checks(session)

    assert len(results) == 6
    assert all(isinstance(result, ControlResult) for result in results)
    # Ce test vérifie que le pipeline complet s'exécute sans erreur contre un
    # compte simulé, pas qu'il soit conforme. Un compte fraîchement simulé n'a
    # par construction ni MFA racine ni politique de mot de passe : ces deux
    # contrôles doivent donc échouer de façon déterministe.
    by_control_id = {result.control_id: result for result in results}
    assert by_control_id["8.2 / 8.5"].passed is False
    assert by_control_id["5.17"].passed is False
