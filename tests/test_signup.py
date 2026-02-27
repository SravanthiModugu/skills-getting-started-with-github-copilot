"""
Tests for the signup endpoint using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestSignupSuccessful:
    """Test successful signup scenarios"""

    def test_signup_new_student_to_activity(self, client, sample_email):
        """
        Arrange: A new student email not yet registered for an activity
        Act: POST to signup endpoint
        Assert: Student is added successfully with 200 status
        """
        # Arrange
        activity_name = "Chess Club"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {sample_email} for {activity_name}"
        assert sample_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1


class TestSignupActivityNotFound:
    """Test signup with invalid activity name"""

    def test_signup_to_nonexistent_activity(self, client, sample_email):
        """
        Arrange: A valid student email and a non-existent activity name
        Act: POST to signup endpoint with invalid activity
        Assert: Returns 404 with appropriate error message
        """
        # Arrange
        invalid_activity = "Nonexistent Activity"

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestSignupDuplicatePrevention:
    """Test duplicate signup prevention"""

    def test_signup_student_already_registered(self, client, existing_email):
        """
        Arrange: A student already registered for an activity
        Act: Attempt to sign them up again for the same activity
        Assert: Returns 400 with duplicate signup error
        """
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up"


class TestSignupEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_signup_with_different_case_email(self, client):
        """
        Arrange: A student registers with lowercase email, then attempts uppercase
        Act: POST with uppercase version of the same email
        Assert: System treats them as different (case-sensitive)
        """
        # Arrange
        activity_name = "Programming Class"
        email_lowercase = "newtest@mergington.edu"
        email_uppercase = "NEWTEST@MERGINGTON.EDU"

        # Act - First signup with lowercase
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email_lowercase}
        )

        # Act - Try signup with uppercase version
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email_uppercase}
        )

        # Assert - Both succeed (email comparison is case-sensitive)
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_signup_multiple_activities_same_student(self, client, sample_email):
        """
        Arrange: A student not registered for multiple activities
        Act: Sign them up for multiple different activities
        Assert: Student appears in participants list for each activity
        """
        # Arrange
        activities_to_join = ["Chess Club", "Programming Class", "Tennis Club"]

        # Act & Assert
        for activity_name in activities_to_join:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": sample_email}
            )
            assert response.status_code == 200
            assert sample_email in activities[activity_name]["participants"]
