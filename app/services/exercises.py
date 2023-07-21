import json
import re

from flask import jsonify, request

from app.dal import dal
from app.services.agents import (
    exercises_model,
    exercises_system_prompt,
    exercises_user_prompt,
)
from app.services.gpt import GPT


class Exercises:
    @staticmethod
    def get():
        """Get exercises from database."""
        exercises = dal.get_exercises()
        return jsonify({"exercises": exercises})

    @staticmethod
    def add():
        """Add exercises to database."""
        exercises = request.json["exercises"]
        dal.add_exercise(exercises)
        return jsonify({"exercises": exercises})

    @staticmethod
    def generate(n: int = 1):
        """Generate n new exercises and returns.
        (n defaults to 1)
        """
        n: int = request.args.get("n", n)

        # Get existing exercises names
        exercises_names = ", ".join(dal.get_exercises_names())

        # Generate new exercises
        response = GPT(exercises_model).chat_completion(
            [
                (
                    "system",
                    exercises_system_prompt.format(exercises_names=exercises_names),
                ),
                ("user", exercises_user_prompt.format(n=n)),
            ]
        )
        print(response)

        # Parse JSONL to list of dicts
        exercises = [
            json.loads(exercise)
            for exercise in re.sub("\n+", "\n", response).splitlines()
        ]

        # Return exercises
        return jsonify({"exercises": exercises})
