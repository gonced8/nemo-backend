import json
import re
from datetime import datetime

from flask import jsonify, request

from app.dal import dal
from app.services.agents import (
    plan_executor_feedback_info_prompt,
    plan_executor_feedback_prompt,
    plan_executor_model,
    plan_executor_prompt,
)
from app.services.gpt import GPT


class PlanExecutor:
    @staticmethod
    def chat(user_id: str):
        """Chat with the user to execute the plan."""

        # Read plan and messages from request body
        user_plan = request.json["user_plan"]
        messages = request.json["messages"]

        # Format dicts to json
        user_plan = json.dumps(user_plan, indent=4, ensure_ascii=False)
        messages = [
            (role, json.dumps(text, indent=4, ensure_ascii=False))
            for role, text in messages
        ]

        # Read user info from database
        info = dal.get_info(user_id, "*")
        info = "\n".join([f"[{entry['created_at']}] {entry['info']}" for entry in info])

        # Add system instruction
        messages.insert(
            0,
            (
                "system",
                plan_executor_prompt.format(
                    info=info, current_time=datetime.utcnow(), user_plan=user_plan
                ),
            ),
        )

        # Get response from GPT
        response = GPT(plan_executor_model).chat_completion(messages)

        # Parse response
        response = json.loads(response)

        return jsonify(response)

    @staticmethod
    def feedback_interface(user_id: str):
        """Receive feedback from the user about the plan execution."""

        # Read plan from request body
        user_plan = request.json["user_plan"]
        user_plan = json.dumps(user_plan, indent=4, ensure_ascii=False)

        # Read user info from database
        info = dal.get_info(user_id, "*")
        info = "\n".join([f"[{entry['created_at']}] {entry['info']}" for entry in info])

        # Format prompt
        messages = [
            (
                "system",
                plan_executor_feedback_prompt.format(
                    info=info, current_time=datetime.utcnow(), user_plan=user_plan
                ),
            ),
        ]

        # Get response from GPT
        response = GPT(plan_executor_model).chat_completion(messages)
        response = json.loads(response)

        return jsonify(response)

    @staticmethod
    def feedback_info(user_id: str):
        """Receive feedback from the user about the plan execution."""

        # Read user feedback from request body
        user_feedback = request.json["user_feedback"]

        # Format prompt
        messages = [
            (
                "system",
                plan_executor_feedback_info_prompt.format(user_feedback=user_feedback),
            ),
        ]

        # Get response from GPT
        response = GPT(plan_executor_model).chat_completion(messages)

        # Parse info
        info = re.sub(r"^- ", "", response, flags=re.MULTILINE).splitlines()

        # Add info to database
        new_info = [
            {"user_id": user_id, "info": entry, "agent": "plan_executor_feedback"}
            for entry in info
        ]
        new_info = dal.add_info(new_info)

        return jsonify({"info": info})
