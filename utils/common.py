import pytest


@pytest.fixture(scope="session")
def get_todoist_token():
    with open("api_token", 'r') as token_file:
        key = token_file.read()
    return f"Bearer {key}"


def get_creds_todoist():
    with open("creds", 'r') as creds_file:
        username, password = creds_file.readlines()
        print(username, password)
        return username, password