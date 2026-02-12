import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_unregister_participant():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_signup_invalid_activity():
    response = client.post("/activities/InvalidActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_participant():
    response = client.delete("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
