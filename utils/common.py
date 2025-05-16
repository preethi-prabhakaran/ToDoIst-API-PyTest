import pytest


@pytest.fixture(scope="session")
def get_todoist_token():
    with open("../api_token", 'r') as token_file:
        key = token_file.read()
    return f"Bearer {key}"


