# Tests for eskiz-pkg

This directory contains tests for the eskiz-pkg library.

## Running Tests

To run the tests, you need to install the development dependencies:

```bash
pip install -e ".[dev]"
```

Then you can run the tests using pytest:

```bash
pytest
```

## Test Structure

- `test_sync_client.py`: Tests for the synchronous client
- `test_async_client.py`: Tests for the asynchronous client

## Writing Tests

When writing tests, please follow these guidelines:

1. Use unittest for test classes
2. Mock external API calls
3. Test both success and error cases
4. Use descriptive test names

## Running Tests with Coverage

To run tests with coverage:

```bash
pytest --cov=eskiz tests/
```
