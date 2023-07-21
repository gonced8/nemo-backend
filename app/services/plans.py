import json
import re

from flask import jsonify, request

from app.dal import dal
from app.services.agents import (
    plans_chat_model,
    plans_chat_system_prompt,
    plans_model,
    plans_system_prompt,
    plans_user_prompt,
)
from app.services.gpt import GPT


class Plans:
    @staticmethod
    def get(user_id: str):
        """Get plans from database."""
        plans = dal.get_plans()
        return jsonify({"plans": plans})

    @staticmethod
    def add(user_id: str):
        """Add plans to database."""
        plans: dict = request.json["plans"]
        dal.add_plans(plans)
        return jsonify({"plans": plans})

    @staticmethod
    def generate(user_id: str, n: int = 1):
        """Generate n new plans and returns.
        (n defaults to 1)
        """
        n: int = request.args.get("n", n)

        # Get existing exercises
        exercises = dal.get_exercises()

        # Format exercises to string
        exercises = [
            {
                k: v
                for k, v in exercise.items()
                if k
                in [
                    "exercise_name",
                    "description",
                    "difficulty",
                    "repetitions",
                    "estimated_duration",
                    "target",
                ]
            }
            for exercise in exercises
        ]
        exercises = "\n".join(json.dumps(exercise) for exercise in exercises)

        # Get existing plans (filtering unnecessary fields)
        plans = dal.get_plans(user_id)
        plans = [
            {
                k: v
                for k, v in plan.items()
                if k in ["plan_name", "exercises_names", "estimated_duration"]
            }
            for plan in plans
        ]
        plans = "\n".join(json.dumps(plan) for plan in plans)

        # Generate new plan
        response = GPT(plans_model).chat_completion(
            [
                (
                    "system",
                    plans_system_prompt.format(exercises=exercises, plans=plans),
                ),
                ("user", plans_user_prompt.format(n=n)),
            ]
        )

        # Parse JSONL to list of dicts
        plans = [
            json.loads(plan) for plan in re.sub("\n+", "\n", response).splitlines()
        ]

        # Add user_id to plans
        plans = [plan | {"user_id": user_id} for plan in plans]

        # Return plans
        return jsonify({"plans": plans})

    @staticmethod
    def chat(user_id: str, start: bool = False):
        # Read query parameters
        start: bool = request.args.get("start", start)

        # Get existing exercises
        exercises = dal.get_exercises()

        # Format exercises to string
        exercises = [
            {
                k: v
                for k, v in exercise.items()
                if k
                in [
                    "exercise_name",
                    "description",
                    "difficulty",
                    "repetitions",
                    "estimated_duration",
                    "target",
                ]
            }
            for exercise in exercises
        ]
        exercises = "\n".join(json.dumps(exercise) for exercise in exercises)

        if not start:
            # Get previous messages
            ...
        else:
            messages = [
                ("system", plans_chat_system_prompt.format(exercises=exercises))
            ]

        # Generate response
        response = GPT(plans_chat_model).chat_completion(messages)

        # Parse response JSON to dict
        response = json.loads(response)
        response.pop("finish", None)

        # Add response to messages database
        message = {
            "user_id": user_id,
            "agent": "plans",
            "message": response,
            "role": "assistant",
        }
        message = dal.add_message(message)

        # Return plan
        return jsonify(response)
