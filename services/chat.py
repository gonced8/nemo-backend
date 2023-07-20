from flask import jsonify, request
from dal import dal
import json
from services.gpt import GPT
from services.agents import (
    onboarding_model,
    onboarding_prompt,
)


class Chat:
    @staticmethod
    def chat(user_id):
        """Chat function for the user to talk to and saves the answers to the database"""
        message = request.json["message"]
        previous_messages = dal.get_messages(user_id, "*")
