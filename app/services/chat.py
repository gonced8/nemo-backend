import json
from flask import jsonify, request
from app.dal import dal
from app.services.gpt import GPT
from app.services.agents import (
    chat_model,
    chat_prompt,
)


class Chat:
    @staticmethod
    def chat(user_id):
        """Chat function for the user to talk to and saves the answers to the database"""

        # Save user message to database
        message = request.json["message"]
        message = {
            "user_id": user_id,
            "message": message,
            "agent": "chat",
            "role": "user",
        }

        message_id = dal.add_message(message=message)[0]["id"]

        # Load previous messages and info

        previous_messages = [
            (message["role"], json.dumps(message["message"], ensure_ascii=False))
            for message in dal.get_messages(user_id, "chat")
        ]
        info = [info["info"] for info in dal.get_info(user_id, "*")]

        # Create prompt and get response
        messages = (
            previous_messages
            + [("system", chat_prompt.format(info=info))]
            + [("user", json.dumps(message["message"], ensure_ascii=False))]
        )

        print(f"Previous Messages: {previous_messages}\n\n")
        print(f"Info: {info}\n\n")
        print(f"Current Message: {message}\n\n")

        response = GPT(chat_model).chat_completion(messages)
        response = json.loads(response)

        nextQuestion = response.get("nextQuestion", None)
        retrievedFacts = response.get("retrievedFacts", None)
        personalityType = response.get("personalityType", None)
        actionTake = response.get("actionTake", None)

        print(f"Next Question: {nextQuestion}\n\n")
        print(f"Retrieved Facts: {retrievedFacts}\n\n")
        print(f"Personality Type: {personalityType}\n\n")
        print(f"Action Take: {actionTake}\n\n")

        if nextQuestion:
            message = {
                "user_id": user_id,
                "message": nextQuestion,
                "agent": "chat",
                "role": "assistant",
            }
            next_question_id = dal.add_message(message)[0]["id"]

        if retrievedFacts:
            info = [
                {
                    "message_id": message_id,
                    "call_id": next_question_id,
                    "user_id": user_id,
                    "info": fact,
                    "agent": "chat",
                    "tag": "facts",
                }
                for fact in retrievedFacts
            ]
            dal.add_info(info)

        if personalityType:
            persona_info = {
                "message_id": message_id,
                "call_id": next_question_id,
                "user_id": user_id,
                "info": personalityType,
                "agent": "chat",
                "tag": "personality_traits",
            }
            dal.add_info(persona_info)

        if actionTake:
            action_info = [
                {
                    "message_id": message_id,
                    "call_id": next_question_id,
                    "user_id": user_id,
                    "info": action,
                    "agent": "chat",
                    "tag": "action",
                }
                for action in actionTake
            ]
            dal.add_info(action_info)

        return jsonify({"message": nextQuestion})
