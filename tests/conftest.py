"""
Shared test configuration and fixtures.
Uses the Arrange phase of AAA pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Arrange: Provide a test client for API requests"""
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Arrange: Provide a valid test email that's not already registered"""
    return "newstudent@mergington.edu"


@pytest.fixture
def existing_email():
    """Arrange: Provide an email already registered in Chess Club"""
    return activities["Chess Club"]["participants"][0]
