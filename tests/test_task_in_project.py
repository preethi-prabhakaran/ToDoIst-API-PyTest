import pytest
import requests
from selenium.webdriver.common.by import By

from config.locators import task_content
from config.variables import BASE_URL, endpoint_task, endpoint_project, URL
from pages.login_page import LoginPage
from utils.common import get_todoist_token, get_creds_todoist

endpoint = f"{BASE_URL}{endpoint_task}"
username, password = get_creds_todoist()

@pytest.fixture(scope="session")
def test_create_project(get_todoist_token):
    headers = {
        "Authorization": get_todoist_token
    }
    payload = {
        "name": "my_new_project",
        "description": "A test project created by automation"
    }

    response = requests.post(f"{BASE_URL}{endpoint_project}", json=payload, headers=headers)
    print(response.status_code, response.text)
    assert response.status_code == 200
    json_data = response.json()
    assert "my_new_project" in json_data['name']
    project_id = json_data['id']
    yield project_id, get_todoist_token

    # Delete the created project after the tests are run
    response = requests.delete(f"{BASE_URL}{endpoint_project}/{project_id}", headers=headers)
    assert response.status_code == 204

@pytest.fixture(scope="session")
def test_create_task(test_create_project):
    project_id, key = test_create_project
    headers = {
        "Authorization": key
    }
    payload = {
        "content" : "Bake Cookies",
        "label" : "personal",
        "project_id" : project_id,
        "due_string" : "today by 4 pm"
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    assert response.status_code == 200

    task_id = response.json()['id']
    yield task_id, key, project_id

    # Delete the task created after all task related tests are run
    response = requests.delete(f"{endpoint}/{task_id}", headers=headers)
    assert response.status_code == 204

def test_view_task(test_create_task):
    task_id, key, project_id = test_create_task
    headers = {
        "Authorization": key
    }

    response = requests.get(f"{endpoint}/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["project_id"] == project_id

def test_ui_view_task(test_create_task):
    login_page = LoginPage(URL, username, password)
    driver = login_page.launch_todoist()
    login_page.login_to_todoist(driver)

    assert "Bake Cookies" in driver.find_element(By.XPATH, task_content).text


