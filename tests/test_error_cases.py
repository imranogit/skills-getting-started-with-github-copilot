from urllib.parse import quote


def test_signup_returns_400_for_duplicate_participant(client):
    activity_name = "Chess Club"
    encoded_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{encoded_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/participants", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_not_found(client):
    activity_name = "Robotics Club"
    encoded_name = quote(activity_name, safe="")
    email = "nobody@mergington.edu"

    response = client.delete(f"/activities/{encoded_name}/participants", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
