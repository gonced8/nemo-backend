from flask import jsonify, request
import json
from app.dal import dal
from app.services.gpt import GPT
from app.services.agents import apple_health_kit_model, apple_health_kit_prompt


class AppleHealthKit:
    @staticmethod
    def get():
        """Obtains Apple Health Kit information from the user, suitable for a SwiftUI view"""
        apple_health_kit_data = request.json["apple_health_kit_data"]
        response = GPT(apple_health_kit_model).chat_completion(
            (
                [
                    (
                        "system",
                        apple_health_kit_prompt,
                    ),
                    ("user", apple_health_kit_data),
                ]
            )
        )
        return jsonify({"apple_health_cards": json.loads(response)})
