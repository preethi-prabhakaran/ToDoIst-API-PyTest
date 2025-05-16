import pytest
import requests

from config.variables import BASE_URL, endpoint_task
from utils.common import get_todoist_token

endpoint = f"{BASE_URL}{endpoint_task}"

@pytest.fixture(scope="session")
def test_create_task(get_todoist_token):
    headers = {
        "Authorization": get_todoist_token
    }
    payload = {
        "content" : "Bake cookies",
        "label" : "personal",
        "due_string" : "today by 4 pm"
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    assert response.status_code == 200

    task_id = response.json()['id']
    yield task_id, get_todoist_token

    # Delete the task created after all task related tests are run
    response = requests.delete(f"{endpoint}/{task_id}", headers=headers)
    assert response.status_code == 204

def test_view_task(test_create_task):
    task_id, key = test_create_task
    headers = {
        "Authorization": key
    }

    response = requests.get(endpoint, headers=headers)
    assert response.status_code == 200

def test_update_task(test_create_task):
    task_id, key = test_create_task
    headers = {
        "Authorization": key
    }
    payload = {
        "due_string" : "Today by 6pm",
        "priority" : "2"
    }
    response = requests.post(f"{endpoint}/{task_id}", json=payload, headers=headers)
    assert response.status_code == 200

    assert response.json()["due"]["string"] == "Today by 6pm"

def test_update_task_with_invalid_payload(test_create_task):
    task_id, key = test_create_task
    headers = {
        "Authorization": key
    }
    payload = {
        "no_data" : "NA"
    }
    response = requests.post(f"{endpoint}/{task_id}", json=payload, headers=headers)
    assert response.status_code == 400


