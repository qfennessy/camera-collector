# Camera Collector Testing Guidelines

This document outlines the testing strategy, conventions, and practices for the Camera Collector application. Effective testing ensures the reliability, correctness, and maintainability of the codebase.

## Philosophy

We aim for a comprehensive test suite that provides confidence in the application's behavior across different layers. Our testing strategy focuses on:

1.  **Correctness**: Verifying that features work as specified.
2.  **Regression Prevention**: Ensuring that bug fixes stay fixed and new changes don't break existing functionality.
3.  **Design Feedback**: Using tests to drive better API and code design.
4.  **Maintainability**: Writing clear, concise, and easy-to-maintain tests.

## Testing Framework

-   **Framework**: [pytest](https://docs.pytest.org/) is the primary testing framework.
-   **Plugins**: We utilize pytest plugins such as `pytest-asyncio` for testing async code and `pytest-cov` for coverage reporting.

## Test Structure and Location

-   All tests reside in the `tests/` directory at the root of the project.
-   The structure within `tests/` mirrors the `camera_collector/` source directory (e.g., tests for `camera_collector/api/routers/cameras.py` are in `tests/api/routers/test_cameras.py`).
-   Test filenames must start with `test_`.
-   Test function names must start with `test_`.
-   Test classes (optional, for grouping related tests) should start with `Test`.

## Types of Tests

1.  **Unit Tests**:
    *   Focus: Testing individual functions or classes in isolation.
    *   Location: Typically within `tests/services/`, `tests/db/repositories/`, `tests/core/`, etc.
    *   Dependencies: External dependencies (like databases or external APIs) are mocked.
2.  **Integration Tests**:
    *   Focus: Testing the interaction between multiple components, such as API endpoints interacting with services and repositories.
    *   Location: Primarily within `tests/api/`.
    *   Dependencies: Often involve a real (test) database connection and test client interactions.
3.  **End-to-End (E2E) Tests**:
    *   (Currently Limited) Focus: Testing complete user flows through the API. May be expanded in the future.

## Fixtures (`conftest.py`)

-   Common test setup and fixtures are defined in `tests/conftest.py`.
-   Fixtures are used extensively for:
    *   Setting up the FastAPI test client (`client`).
    *   Providing database connections/sessions for tests (`db_session`).
    *   Creating reusable test data (e.g., `test_user`, `test_camera`).
    *   Managing test database state (e.g., cleaning up data between tests).

## Mocking

-   The `unittest.mock` library (or pytest wrappers like `pytest-mock`) is used for mocking dependencies in unit tests.
-   Mocking is crucial for isolating the unit under test and avoiding reliance on external systems or complex setup.
-   Avoid excessive mocking in integration tests; aim to test the actual integration points.

## Running Tests

-   **Run all tests**:
    ```bash
    poetry run pytest
    ```
-   **Run tests in a specific file**:
    ```bash
    poetry run pytest tests/api/routers/test_cameras.py
    ```
-   **Run a specific test function or class**:
    ```bash
    poetry run pytest tests/api/routers/test_cameras.py::TestCameraRoutes::test_create_camera -v
    ```
-   **Run tests with coverage report**:
    ```bash
    poetry run pytest --cov=camera_collector --cov-report=term-missing
    ```
-   **Coverage Target**: Aim for at least 80% test coverage, focusing particularly on critical paths and business logic.

## Test Data

-   Use realistic but anonymized test data.
-   Leverage fixtures or factory patterns (if implemented) to generate consistent test data.
-   Ensure tests clean up any data they create to maintain isolation between tests.

## Assertions

-   Use standard `assert` statements provided by pytest.
-   Make assertions specific and clear. Check status codes, response body content, database state changes, etc., as appropriate for the test type.
-   For complex data structures, compare relevant fields rather than relying on exact object equality if IDs or timestamps might differ.

## Best Practices

1.  **Write tests alongside code**: Don't wait until the feature is complete.
2.  **Test edge cases and error conditions**: Don't just test the "happy path".
3.  **Keep tests independent**: Tests should not rely on the execution order or state left by previous tests.
4.  **Refactor tests**: Treat test code with the same care as production code. Keep it DRY and readable.
5.  **Run tests frequently**: Integrate testing into the development workflow.
