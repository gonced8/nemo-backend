import json
import re

from flask import jsonify, request

from app.dal import dal
from app.services.agents import plans_model, plans_system_prompt, plans_user_prompt
from app.services.gpt import GPT


class Plans:
    @staticmethod
    def generate(user_id: str):
        """Generate n new plans and returns.
        (n defaults to 1)
        """
        n: int = request.args.get("n", 1)

        # Get existing exercises
        exercises = dal.get_exercises()
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

        # Add plans to database
        plans = [plan | {"user_id": user_id} for plan in plans]
        dal.add_plans(plans)

        # Return plans
        return jsonify({"plans": plans})

    @staticmethod
    def get(user_id: str):
        """Get plans from database."""
        plans = dal.get_plans()
        return jsonify({"plans": plans})
