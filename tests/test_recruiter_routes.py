"""
Tests for the recruiter-directory and application-tracking endpoints.

Covers:
  GET  /recruiters                – full list
  GET  /recruiters?city=Berlin    – filtered by city
  GET  /recruiters?city=Dubai     – filtered by city
  GET  /recruiters?role_type=...  – filtered by role type
  POST /recruiters/{name}/apply   – record an application
  POST /recruiters/{name}/apply   – 400 on duplicate application
  POST /recruiters/{name}/apply   – 404 on unknown recruiter
"""
import copy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, recruiters

INITIAL_RECRUITERS = copy.deepcopy(recruiters)
TEST_EMAIL = "imran.ismail2003@gmail.com"


@pytest.fixture(autouse=True)
def reset_recruiters_state():
    """Reset recruiter applications before/after every test."""
    for entry in recruiters.values():
        entry["applications"].clear()
    yield
    for entry in recruiters.values():
        entry["applications"].clear()


@pytest.fixture
def client():
    return TestClient(app)


# ── GET /recruiters ─────────────────────────────────────────────────────────

def test_get_recruiters_returns_dict(client):
    response = client.get("/recruiters")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_recruiters_contains_berlin_entries(client):
    response = client.get("/recruiters")
    data = response.json()
    berlin_entries = [v for v in data.values() if v["city"] == "Berlin"]
    assert len(berlin_entries) >= 1


def test_get_recruiters_contains_dubai_entries(client):
    response = client.get("/recruiters")
    data = response.json()
    dubai_entries = [v for v in data.values() if v["city"] == "Dubai"]
    assert len(dubai_entries) >= 1


def test_filter_recruiters_by_city_berlin(client):
    response = client.get("/recruiters", params={"city": "Berlin"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for entry in data.values():
        assert entry["city"] == "Berlin"


def test_filter_recruiters_by_city_dubai(client):
    response = client.get("/recruiters", params={"city": "Dubai"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for entry in data.values():
        assert entry["city"] == "Dubai"


def test_filter_recruiters_by_role_type_werkstudent(client):
    response = client.get("/recruiters", params={"role_type": "Werkstudent"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for entry in data.values():
        assert entry["role_type"] == "Werkstudent"


def test_filter_recruiters_by_role_type_regular(client):
    response = client.get("/recruiters", params={"role_type": "Regular"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for entry in data.values():
        assert entry["role_type"] == "Regular"


def test_berlin_recruiters_have_werkstudent_role_type(client):
    response = client.get("/recruiters", params={"city": "Berlin"})
    data = response.json()
    for entry in data.values():
        assert entry["role_type"] == "Werkstudent"


def test_dubai_recruiters_have_regular_role_type(client):
    response = client.get("/recruiters", params={"city": "Dubai"})
    data = response.json()
    for entry in data.values():
        assert entry["role_type"] == "Regular"


def test_each_recruiter_entry_has_required_fields(client):
    response = client.get("/recruiters")
    data = response.json()
    required_fields = {"city", "role_type", "company", "contact_name",
                       "contact_email", "linkedin", "sector", "notes",
                       "applications"}
    for name, entry in data.items():
        for field in required_fields:
            assert field in entry, f"'{field}' missing from recruiter '{name}'"


# ── POST /recruiters/{name}/apply ───────────────────────────────────────────

def test_apply_werkstudent_records_application(client):
    name = "Marriott Berlin (Werkstudent)"
    encoded = quote(name, safe="")
    email = TEST_EMAIL

    response = client.post(f"/recruiters/{encoded}/apply", params={"email": email})

    assert response.status_code == 200
    msg = response.json()["message"]
    assert "Werkstudent application" in msg
    assert email in msg
    assert "Berlin" in msg


def test_apply_werkstudent_persists_in_applications_list(client):
    name = "Hilton Berlin (Werkstudent)"
    encoded = quote(name, safe="")
    email = TEST_EMAIL

    client.post(f"/recruiters/{encoded}/apply", params={"email": email})

    recruiters_response = client.get("/recruiters")
    applications = recruiters_response.json()[name]["applications"]
    assert email in applications


def test_apply_dubai_regular_records_application(client):
    name = "Jumeirah Group Dubai"
    encoded = quote(name, safe="")
    email = TEST_EMAIL

    response = client.post(f"/recruiters/{encoded}/apply", params={"email": email})

    assert response.status_code == 200
    msg = response.json()["message"]
    assert "conditions" in msg
    assert email in msg
    assert "Dubai" in msg


def test_apply_dubai_regular_mentions_conditions_guidance(client):
    name = "Rotana Hotels Dubai"
    encoded = quote(name, safe="")
    email = TEST_EMAIL

    response = client.post(f"/recruiters/{encoded}/apply", params={"email": email})

    msg = response.json()["message"]
    assert "salary" in msg.lower() or "conditions" in msg.lower()


def test_apply_returns_400_on_duplicate(client):
    name = "Meininger Hotels Berlin (Werkstudent)"
    encoded = quote(name, safe="")
    email = TEST_EMAIL

    client.post(f"/recruiters/{encoded}/apply", params={"email": email})
    response = client.post(f"/recruiters/{encoded}/apply", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Application already submitted to this recruiter"


def test_apply_returns_404_for_unknown_recruiter(client):
    response = client.post(
        "/recruiters/Unknown%20Company/apply",
        params={"email": TEST_EMAIL},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Recruiter not found"
