import json
from flask import jsonify, request

from app.dal import dal
from app.services.agents import persona_model, persona_prompt
from app.services.gpt import GPT


class Persona:
    @staticmethod
    def get(user_id: str):
        """Get the persona of a user"""
        persona = dal.get_persona(user_id)
        return jsonify({"persona": persona})

    @staticmethod
    def add(user_id: str):
        """Add the persona of a user"""
        persona = request.json
        persona = dal.add_persona(persona | {"user_id": user_id})
        return jsonify(persona[0])

    @staticmethod
    def generate(user_id: str):
        """Generate a persona for a user from their info"""

        # Get user info
        info = dal.get_info(user_id, "*")

        # Format info
        info = "\n".join([f"[{entry['created_at']}] {entry['info']}" for entry in info])

        # Make prompt
        messages = [("system", persona_prompt.format(info=info))]

        # Generate persona
        response = GPT(persona_model).chat_completion(messages)
        response = json.loads(response)
        dropout_risk = response["dropout_risk"]
        info = [
            {
                "user_id": user_id,
                "info": f"The dropout risk is {dropout_risk}.",
                "agent": "persona",
                "tag": "dropout_risk",
            }
        ]
        dal.add_info(info)
        return jsonify(response)
