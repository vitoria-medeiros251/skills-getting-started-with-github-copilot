from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate_and_unregister():
    activity = "Chess Club"
    email = "teststudent@mergington.edu"

    # Garantir estado inicial
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup deve funcionar
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Signup duplicado deve falhar
    res_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert res_dup.status_code == 400

    # Unregister deve funcionar
    res_un = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res_un.status_code == 200
    assert email not in activities[activity]["participants"]
