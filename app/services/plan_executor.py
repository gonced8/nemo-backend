import json
import re

from flask import jsonify, request

from app.dal import dal
from app.services.agents import plan_executor_model, plan_executor_prompt
from app.services.gpt import GPT


class PlanExecutor:
    @staticmethod
    def chat(user_id: str):
        """Chat with the user to execute the plan."""

        # TODO: use info from user_id

        # Read plan and messages from request body
        user_plan = request.json["user_plan"]
        messages = request.json["messages"]

        # Format dicts to json
        user_plan = json.dumps(user_plan, indent=4, ensure_ascii=False)
        messages = [
            (role, json.dumps(text, indent=4, ensure_ascii=False))
            for role, text in messages
        ]

        # Add system instruction
        messages.insert(
            0,
            (
                "system",
                plan_executor_prompt.format(user_plan=user_plan),
            ),
        )

        print(messages)

        # Get response from GPT
        response = GPT(plan_executor_model).chat_completion(messages)

        # Parse response
        print(response)
        response = json.loads(response)

        return jsonify(response)
