from unittest.mock import Mock, patch
from api.services.docker import get_logs
from exceptions import ContainerNotFoundError
import docker
import pytest


@pytest.fixture
def fake_container():
    container = Mock()
    container.short_id = "123"
    container.name = "fake"
    return container


def test_get_logs(fake_container):
    fake_container.logs.return_value = b"linha 1\nlinha 2"

    with patch("services.docker.client") as mock_client:
        mock_client.containers.get.return_value = fake_container
        result = get_logs("123")

    assert result == {
        "short_id": "123",
        "name": "fake",
        "logs": "linha 1\nlinha 2"
    }


def test_get_logs_exception():
    with patch("services.docker.client") as mock_client:
        mock_client.containers.get.side_effect = docker.errors.NotFound(
            "container not found")
        with pytest.raises(ContainerNotFoundError):
            get_logs("123")


def test_get_logs_empty(fake_container):
    fake_container.logs.return_value = b""
    with patch("services.docker.client") as mock_client:
        mock_client.containers.get.return_value = fake_container
        result = get_logs("123")

    assert result == {
        "short_id": "123",
        "name": "fake",
        "logs": ""
    }
