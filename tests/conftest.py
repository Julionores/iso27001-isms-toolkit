"""Fixtures partagées pour les tests. Fournit des identifiants AWS factices : moto
intercepte les appels avant qu'ils n'atteignent le réseau, mais boto3 exige tout de
même des identifiants et une région pour construire ses clients."""

import os

import pytest


@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-3"
