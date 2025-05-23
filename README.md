### Todoist API Test Suite

This repository contains automated API tests for the [Todoist](https://developer.todoist.com/rest/v2/) app, built using:

- Python
- pytest
- requests
- selenium

### Features

- Token-based authentication
- Test coverage for CRUD operations on projects
- Pytest fixtures for reusability and teardown
- Clean test structure with scope management
- **UI test using Selenium to verify task added via API appears correctly in the Todoist web app**
    - Uses reliable locators to assert presence of task text
    - Waits for task to appear with WebDriverWait

### Getting Started

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v -s .\tests\
