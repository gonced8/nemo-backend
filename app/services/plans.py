import json
import re
from datetime import datetime

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
        plans = dal.get_plans(user_id=user_id)
        return jsonify({"plans": plans})

    @staticmethod
    def add(user_id: str):
        """Add plans to database."""
        plans: dict = request.json["plans"]
        print("plans: ", plans)
        dal.add_plans(plans | {"user_id": user_id})
        return jsonify(plans)

    @staticmethod
    def generate(user_id: str, n: int = 1):
        """Generate n new plans and returns.
        (n defaults to 1)
        """
        n: int = request.args.get("n", n)

        # Read user info from database
        info = dal.get_info(user_id, "*")
        info = "\n".join([f"[{entry['created_at']}] {entry['info']}" for entry in info])

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
                    plans_system_prompt.format(
                        info=info,
                        current_time=datetime.utcnow(),
                        exercises=exercises,
                        plans=plans,
                    ),
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
        start: bool = request.args.get(
            "start", default=True, type=lambda v: v.lower() == "true"
        )

        # Read request body
        user_input: dict = request.json if request.data else None

        # Update start flag
        start = start or not user_input

        # First message
        if start:
            # Read user info from database
            info = dal.get_info(user_id, "*")
            info = "\n".join(
                [f"[{entry['created_at']}] {entry['info']}" for entry in info]
            )

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

            # Format messages to GPT
            messages = [
                (
                    "system",
                    plans_chat_system_prompt.format(
                        info=info, current_time=datetime.utcnow(), exercises=exercises
                    ),
                )
            ]

        # Other messages
        else:
            # Get chat_id from latest messages in database
            chat_id = dal.get_planner_chats_last_chat_id(user_id)

            # Get previous messages
            chat = dal.get_planner_chats_by_chat_id(chat_id)

            # Format messages to GPT
            messages = [
                (
                    message["role"],
                    json.dumps(message["message"], indent=4, ensure_ascii=False),
                )
                for message in chat
            ]
            messages.append(
                ("user", json.dumps(user_input, indent=4, ensure_ascii=False))
            )

        # Generate response
        response = GPT(plans_chat_model).chat_completion(messages)

        # Parse response JSON to dict
        response = json.loads(response)
        response.pop("finish", None)

        # Add response to messages database
        # First message
        if start:
            # Add system prompt
            message = dal.add_planner_chats(
                {"user_id": user_id, "role": "system", "message": messages[0][1]}
            )
            chat_id = message[0]["chat_id"]

            # Add assistant's response
            dal.add_planner_chats(
                {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "role": "assistant",
                    "message": response,
                }
            )

        # Other messages
        else:
            # Add user message and assistant response
            chat_id = chat[0]["chat_id"]
            chat = [
                {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "role": "user",
                    "message": user_input,
                },
                {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "role": "assistant",
                    "message": response,
                },
            ]
            dal.add_planner_chats(chat)

        # Return plan
        return jsonify(response)
