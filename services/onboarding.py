from flask import jsonify, request
from dal import DAL
import json
from services.gpt import GPT
from services.agents import (
    onboarding_model,
    onboarding_prompt,
)


class Onboarding:
    @staticmethod
    def chat(user_id):
        """Onboarding function that asks essential questions to the user and saves the answers to the database"""
        overallOnboardingDone = DAL.get_user(user_id=user_id)["OnboardingStatus"]

        if not overallOnboardingDone:
            # Get previous messages
            messages = [
                (message["role"], message["message"])
                for message in DAL.get_messages(user_id, "onboarding")
            ]

            if len(messages) == 0:
                pass
            # If an onboarding is already happening, then we need to add the new message to the previous messages
            else:
                messages += ("user", request.json["message"])
                new_message = {
                    "user_id": user_id,
                    "message": messages,
                    "agent": "onboarding",
                    "role": "user",
                }
                DAL.add_message(message=new_message)

            messages = [("system", onboarding_prompt)] + messages
            print("Messages ", messages)
            response = GPT(onboarding_model).chat_completion(messages)

            response = json.loads(response)

            nextQuestion = response.get("nextQuestion", None)
            retrievedFacts = response.get("retrievedFacts", None)
            personalityType = response.get("personalityType", None)
            overallOnboardingDone = response.get("overallOnboardingDone", False)
            print("nextQuestion ", nextQuestion)
            print("retrievedFacts ", retrievedFacts)
            print("personalityType ", personalityType)
            print("overallOnboardingDone ", overallOnboardingDone)

            if nextQuestion:
                message = {
                    "user_id": user_id,
                    "message": nextQuestion,
                    "agent": "onboarding",
                    "role": "system",
                }
                DAL.add_message(message)

            if retrievedFacts:
                info = [
                    {
                        "user_id": user_id,
                        "info": fact,
                        "agent": "onboarding",
                        "tag": "facts",
                    }
                    for fact in retrievedFacts
                ]
                DAL.add_info(info)

            if personalityType:
                persona_info = {
                    "user_id": user_id,
                    "info": personalityType,
                    "agent": "onboarding",
                    "tag": "personality_traits",
                }
                DAL.add_info(persona_info)

            if bool(overallOnboardingDone):
                user = DAL.get_user(user_id=user_id)
                user["OnboardingStatus"] = True
                DAL.update_user(user)

            return jsonify(
                {
                    "message": nextQuestion,
                    "overallOnboardingDone": overallOnboardingDone,
                }
            )
        else:
            return jsonify({"message": "Onboarding already done"})
