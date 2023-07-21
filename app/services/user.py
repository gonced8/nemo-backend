from flask import jsonify, request

from app.dal import dal


class Users:
    @staticmethod
    def add():
        """Register new user"""
        username = request.json["username"]
        user = dal.get_user(username)
        if user is None:
            user = dal.add_user(username)
            return jsonify({"message": "User added", "user_id": user["id"]})
        else:
            return jsonify({"message": "User already exists", "user_id": user["id"]})

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
