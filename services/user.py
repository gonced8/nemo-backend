from flask import jsonify, request

from dal import DAL


class User:
    @staticmethod
    def add():
        """Register new user"""
        username = request.json["username"]
        user = DAL.get_user(username)
        if user is None:
            user = DAL.add_user(username)
            return jsonify({"message": "User added", "user_id": user["id"]})
        else:
            return jsonify({"message": "User already exists", "user_id": user["id"]})

    @staticmethod
    def get():
        """Get user"""
        username = request.json["username"]
        user = DAL.get_user(username)
        if user is None:
            return jsonify({"message": "User doesn't exist", "user_id": None})
        else:
            return jsonify({"message": "User exists", "user_id": user["id"]})
