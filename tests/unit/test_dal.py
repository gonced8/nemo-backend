import pytest

from app.dal import dal


def test_get_exercises(test_client):
    """Test get_exercises function"""
    exercises = dal.get_exercises()

    assert isinstance(exercises, list)

    if len(exercises) > 0:
        for exercise in exercises:
            assert isinstance(exercise, dict)
            assert "exercise_name" in exercise and isinstance(
                exercise["exercise_name"], str
            )
            assert "description" in exercise and isinstance(
                exercise["description"], str
            )
            assert "difficulty" in exercise and isinstance(exercise["difficulty"], int)
            assert "repetitions" in exercise and isinstance(
                exercise["repetitions"], str
            )
            assert "estimated_duration" in exercise and isinstance(
                exercise["estimated_duration"], int
            )
            assert "target" in exercise and isinstance(exercise["target"], str)
