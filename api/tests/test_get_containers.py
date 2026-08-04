from unittest.mock import Mock, patch
from api.services.docker import get_containers


def test_get_containers():

    fake_container = Mock()

    fake_container.short_id = "123"
    fake_container.name = "fake"
    fake_container.status = "running"

    with patch("services.docker.client") as mock_client:
        mock_client.containers.list.return_value = [fake_container]
        result = get_containers()

    assert result == [{
        "short_id": "123",
        "name": "fake",
        "status": "running"
    }]


def test_get_containers_empty():

    with patch("services.docker.client") as mock_client:
        mock_client.containers.list.return_value = []
        result = get_containers()

    assert result == []


def test_get_containers_calls_docker():
    with patch("services.docker.client") as mock_client:
        mock_client.containers.list.return_value = []
        get_containers()
        mock_client.containers.list.assert_called_once()
