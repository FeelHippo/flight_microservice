import pytest
from flaskr import create_app

valid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1lenphc2Vnb2xhc0BnbWFpbC5jb20iLCJwYXNzd29yZCI6IkZpbGlwcG8zMzMhIn0.Fg6HJeae4DCjFuMS6IHmIz9yyeVoLbnbslZQE-JD9EY'

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def credentials():
    return [('Authorization', valid_token)]

def test_health_check(client):
    response = client.get("/health")
    assert response.json["exit_code"] == 0
    assert response.status_code == 200
    
def test_authenticate(client):
    response = client.post("/authenticate", json = {
        "user_data": {
            "username": "email@gmail.com",
            "password": "PasswordTest1234!"
        }
    })
    assert bool(response.json["authorization"])
    assert response.status_code == 201
    
def test_authenticate_no_valid_username(client):
    response = client.post("/authenticate", json = {
        "user_data": {
            "username": "email",
            "password": "PasswordTest1234!"
        }
    })
    assert hasattr(response, "authorization") == False
    assert response.status_code == 400
    
def test_authenticate_no_valid_password(client):
    response = client.post("/authenticate", json = {
        "user_data": {
            "username": "email@gmail.com",
            "password": "invalid"
        }
    })
    assert hasattr(response, "authorization") == False
    assert response.status_code == 400
    
def test_calculate_unauthenticated(client):
    response = client.post("/calculate", json = {
        "flights": [["SFO", "ATL"], ["ATL", "GSO"], ["IND", "EWR"], ["GSO", "IND"]]
    }, )
    assert response.status_code == 401
    
def test_calculate_authenticated_first(client, credentials):
    response = client.post("/calculate", json = {
        "flights": [["SFO", "ATL"], ["ATL", "GSO"], ["IND", "EWR"], ["GSO", "IND"]]
    }, headers = credentials)
    assert response.json == ["SFO","EWR"]
    assert response.status_code == 200
    
def test_calculate_authenticated_second(client, credentials):
    response = client.post("/calculate", json = {
        "flights": [['SFO', 'EWR']]
    }, headers = credentials)
    assert response.json == ["SFO","EWR"]
    assert response.status_code == 200
    
def test_calculate_authenticated_third(client, credentials):
    response = client.post("/calculate", json = {
        "flights": [['ATL', 'EWR'], ['SFO', 'ATL']]
    }, headers = credentials)
    assert response.json == ["SFO","EWR"]
    assert response.status_code == 200
    
def test_calculate_authenticated_fourth(client, credentials):
    response = client.post("/calculate", json = {
        "flights": [['IND', 'EWR'], ['SFO', 'ATL'], ['GSO', 'IND'], ['ATL', 'GSO']]
    }, headers = credentials)
    assert response.json == ["SFO","EWR"]
    assert response.status_code == 200
    
def test_calculate_authenticated_empty(client, credentials):
    response = client.post("/calculate", json = {
        "flights": []
    }, headers = credentials)
    assert response.status_code == 400
    
def test_calculate_authenticated_missing_link(client, credentials):
    response = client.post("/calculate", json = {
        "flights": [['IND', 'EWR'], ['SFO', 'ATL'], ['ATL', 'GSO']]
    }, headers = credentials)
    assert response.status_code == 422