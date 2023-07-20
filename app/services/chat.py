import json

from flask import jsonify, request

from app.dal import dal
from app.services.agents import onboarding_model, onboarding_prompt
from app.services.gpt import GPT


class Chat:
    @staticmethod
    def chat(user_id):
        """Chat function for the user to talk to and saves the answers to the database"""
        message = request.json["message"]
        previous_messages = dal.get_messages(user_id, "*")
