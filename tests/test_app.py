from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Expect some known activities from the seed data
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"].get("participants"), list)


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Get initial participants
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    initial = len(data[activity]["participants"])

    # Sign up the test user
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # Ensure the participant appears
    res2 = client.get("/activities")
    participants = res2.json()[activity]["participants"]
    assert email in participants
    assert len(participants) == initial + 1

    # Unregister the test user
    delete = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert delete.status_code == 200
    assert "Removed" in delete.json().get("message", "")

    # Ensure participant removed
    res3 = client.get("/activities")
    participants_after = res3.json()[activity]["participants"]
    assert email not in participants_after
    assert len(participants_after) == initial
