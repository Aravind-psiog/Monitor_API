from fastapi.testclient import TestClient
from main import app
from configs import loadconfigs

client = TestClient(app)


def test_list():
    response = client.get("/api/user/list-users", headers={
                          "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]})
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        "/api/user/create-user",
        json={
            "email": "aravind.prabaharan121@psiog.com",
            "username": "Aravind1",
            "password1": "Aravind@23",
            "password2": "Aravind@23"
        },
    )
    assert response.status_code in [200, 409]


def test_invite():
    response = client.post(
        "/api/user/invite/",
        headers={
            "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]},
        json={
            "invited_to": "Local",
            "user": "aravind.prabaharan121@psiog.com"
        },
    )
    assert response.status_code in [200, 409]


def test_list_group_members():
    response = client.get("/api/user/get-group-members/Local", headers={
                          "Authorization": loadconfigs.read_config()["Tokens"]["bearer"]})
    assert response.status_code in [200, 409, 401]
