import json
import re

from flask import jsonify, request

from services.agents import (
    exercises_model,
    exercises_system_prompt,
    exercises_user_prompt,
)
from services.gpt import GPT


class Exercises:
    @staticmethod
    def generate():
        """Generate n new exercises and returns.
        (n defaults to 1)
        """
        n: int = request.args.get("n", 1)

        # Generate new exercises
        response = GPT(exercises_model).chat_completion(
            [
                ("system", exercises_system_prompt),
                ("user", exercises_user_prompt.format(n=n)),
            ]
        )

        # Parse JSON to list of dicts
        exercises = json.loads(response)

        # Add exercises to database

        # Return exercises
        return jsonify(exercises)

    @staticmethod
    def get():
        """Get exercises from database."""
        pass
