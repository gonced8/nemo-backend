from flask import jsonify, request
import json
from app.dal import dal
from app.services.gpt import GPT
from app.services.agents import notification_model, notification_prompt


class Users:
    @staticmethod
    def add():
        """Register new user"""
        username = request.json["username"]
        user = dal.get_user(username)
        if user is None:
            user = dal.add_user(username)
            return jsonify({"message": "User added", "user_id": user["id"], "onboarding_status": user["onboarding_status"]})
        else:
            return jsonify({"message": "User already exists", "user_id": user["id"], "onboarding_status": user["onboarding_status"]})

    @staticmethod
    def get():
        """Get user"""
        username = request.json["username"]
        user = dal.get_user(username)
        if user is None:
            return jsonify({"message": "User doesn't exist", "user_id": None})
        else:
            return jsonify({"message": "User exists", "user_id": user["id"]})

    @staticmethod
    def reset(user_id: str):
        """Reset user"""
        tables = request.json["tables"]
        user = dal.get_user(user_id=user_id)
        if user is None:
            return jsonify({"message": "User doesn't exist", "user_id": None})
        else:
            dal.reset_user(user_id=user_id, tables=tables)
            username = user["username"]
            return jsonify({"message": f"User {username} Deleted"})

    @staticmethod
    def notifications(user_id: str):
        """Get user notifications"""
        currentHour = request.json["current_hour"]
        info = dal.get_info(user_id=user_id, agent="*")
        info = [(info["info"], info["created_at"]) for info in info]
        response = GPT(notification_model).chat_completion(
            (
                [
                    (
                        "system",
                        notification_prompt.format(currentHour=currentHour, info=info),
                    )
                ]
            )
        )

        notifications = json.loads(response)

        return jsonify({"notifications": notifications})

    @staticmethod
    def info(user_id: str):
        """Add info to info table"""
        info = request.json["info"]
        info = {
            "user_id": user_id,
            "info": info,
            "agent": "frontend",
        }
        dal.add_info(info=info)
        return jsonify({"message": "Info added"})
