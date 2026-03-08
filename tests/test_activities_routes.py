from urllib.parse import quote


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_new_participant(client):
    activity_name = "Chess Club"
    encoded_name = quote(activity_name, safe="")
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{encoded_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_unregister_removes_existing_participant(client):
    activity_name = "Basketball Team"
    encoded_name = quote(activity_name, safe="")
    email = "alex@mergington.edu"

    response = client.delete(f"/activities/{encoded_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants
