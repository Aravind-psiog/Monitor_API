from fastapi.testclient import TestClient
from main import app
from configs import loadconfigs

client = TestClient(app)


def test_create_group():
    response = client.post(
        "/api/member/create-group",
        headers={
            "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]},
        json={
            "server_group": "Local"
        },
    )
    assert response.status_code in [200, 409]


def test_create_group_n():
    response = client.post(
        "/api/member/create-group",
        json={
            "server_group": "Local"
        },
    )
    assert response.status_code in [200, 409]


def test_accept_invite():
    email = "aravind.prabaharan121@psiog.com"
    code = "62be72c0"
    response = client.get(f"/api/member/accept-invite/{email}/{code}")
    assert response.status_code in [200, 404]


def test_accept_invite():
    email = "aravind.prabaharan121@psiog.com"
    code = "62be72sxwc0"
    response = client.get(f"/api/member/accept-invite/{email}/{code}")
    assert response.status_code in [200, 404]
