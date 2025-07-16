# 0x03. Unittests and Integration Tests

This project is focused on learning the principles of unit testing and integration testing in Python. It involves writing tests for a utility module and a GitHub API client, demonstrating key concepts like mocking, parametrization, and fixtures.

## Learning Objectives

-   Understand the difference between unit and integration tests.
-   Learn common testing patterns:
    -   **Mocking**: Isolating code from external services (like HTTP APIs) for predictable testing.
    -   **Parametrization**: Running a single test function with multiple sets of inputs to reduce code duplication.
    -   **Fixtures**: Using predefined sets of data to ensure tests are consistent and repeatable.
-   Gain proficiency with Python's `unittest` framework and the `parameterized` library.

## Project Files

-   `utils.py`: A module containing utility functions such as `access_nested_map` for dictionary access, `get_json` for making HTTP requests, and a `memoize` decorator for caching.
-   `client.py`: Contains the `GithubOrgClient` class, which interacts with the GitHub API to fetch information about organizations and their repositories.
-   `fixtures.py`: A file that stores test fixtures, including sample JSON payloads from the GitHub API, used for integration testing.
-   `test_utils.py`: Contains unit tests for all functions within `utils.py`.
-   `test_client.py`: Contains both unit tests and an integration test suite for the `GithubOrgClient` class.

## Requirements

-   Python 3.7
-   `pycodestyle` (version 2.5)
-   The `parameterized` library

## Setup

1.  Clone the repository and navigate to the project directory.

2.  Install the required Python package:
    ```bash
    pip install parameterized
    ```

3.  Make sure all Python script files are executable, as required by the project instructions:
    ```bash
    chmod +x utils.py
    chmod +x client.py
    chmod +x test_utils.py
    chmod +x test_client.py
    ```

## How to Run the Tests

You can run the tests for each module by executing the test files directly from your terminal.

-   To run the unit tests for `utils.py`:
    ```bash
    ./test_utils.py
    ```

-   To run the unit and integration tests for `client.py`:
    ```bash
    ./test_client.py
    ```

A successful test run will output something similar to this for each file, indicating that all tests passed:

...........
Ran 11 tests in 0.002s

OK


---

**Author**: Nissau96