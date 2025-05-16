import pytest
import requests

from config.variables import BASE_URL, endpoint_project
from utils.common import get_todoist_token

endpoint = f"{BASE_URL}{endpoint_project}"

@pytest.fixture(scope="session")
def test_create_project(get_todoist_token):
    headers = {
        "Authorization": get_todoist_token
    }
    payload = {
        "name": "my_new_project",
        "description": "A test project created by automation"
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    print(response.status_code, response.text)
    assert response.status_code == 200
    json_data = response.json()
    assert "my_new_project" in json_data['name']
    project_id = json_data['id']
    yield project_id, get_todoist_token


    # Delete the created project after the tests are run
    response = requests.delete(f"{endpoint}/{project_id}", headers=headers)
    assert response.status_code == 204

def test_view_project(test_create_project):
    project_id, key = test_create_project
    headers = {
        "Authorization": key
    }

    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 200
    print(response.json())

def test_update_project(test_create_project):
    project_id, key = test_create_project
    headers = {
        "Authorization" : key
    }
    payload = {
        "name" : "Updated_Project"
    }
    response = requests.post(f"{endpoint}/{project_id}", json=payload, headers=headers)
    assert response.status_code == 200

    assert response.json()['name'] == "Updated_Project"

def test_invalid_update_request(test_create_project):
    project_id, key = test_create_project
    headers = {
        "Authorization": key
    }

    response = requests.post(f"{endpoint}/{project_id}", headers=headers)
    assert response.status_code == 400

    assert response.text == "At least one of name, description, color, is_favorite or view_style fields should be set"

def test_view_single_project(test_create_project):
    project_id, key = test_create_project
    headers = {
        "Authorization": key
    }
    response = requests.get(f"{endpoint}/{project_id}", headers=headers)
    assert response.status_code == 200

    assert response.json()['name'] == "Updated_Project"

def test_unauthorized_view_project():
    response = requests.get(endpoint)
    assert response.status_code == 401
    assert response.text == "Forbidden"

