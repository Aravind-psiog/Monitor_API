from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from AWS"}


def test_root_n():
    response = client.put("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from AWS"}


def test_login():
    response = client.post(
        "/login",
        data={"username": "aravind.prabaharan@psiog.com",
              "password": "Aravind@23"},
    )
    assert response.status_code == 200


def test_login_n():
    response = client.post(
        "/login",
        data={"username": "aravind.prabaharan21@psiog.com",
              "password": "Aravind@23"},
    )
    assert response.status_code == 200


def test_login_n():
    response = client.post(
        "/login",
        data={"username": "aravind.prabaharan21@psiog.com",
              "password": "Aravind22@23"},
    )
    assert response.status_code == 200
