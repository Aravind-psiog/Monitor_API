from fastapi.testclient import TestClient
from main import app
from configs import loadconfigs

client = TestClient(app)


def test_list_server():
    response = client.get("/api/server/list-server-group", headers={
                          "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]})
    assert response.status_code in [200, 404]


def test_create_server():
    response = client.post(
        "/api/server/create-server",
        headers={
            "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]
        },
        json={
            "ip_address": "1.1.1.1",
            "server_group": "Local"
        },
    )
    assert response.status_code in [200, 409]


def test_create_server_n():
    response = client.post(
        "/api/server/create-server",
        headers={
            "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]
        },
        json={
            "ipaddress": "663.1.334.1",
            "server_group": "Local"
        },
    )
    assert response.status_code in [200, 409]
