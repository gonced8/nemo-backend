from flask import jsonify, request
from dal import dal
import json
from services.gpt import GPT
from services.agents import (
    onboarding_model,
    onboarding_prompt,
)


class Onboarding:
    @staticmethod
    def chat(user_id):
        # TODO get response in the right format
        """Onboarding function that asks essential questions to the user and saves the answers to the database"""
        overallOnboardingDone = dal.get_user(user_id=user_id)["onboarding_status"]

        if not overallOnboardingDone:
            # Get previous messages
            messages = [
                (message["role"], message["message"])
                for message in dal.get_messages(user_id, "onboarding")
            ]
            print("Retrieved Messages ", messages)
            if len(messages) == 0:
                pass
            # If an onboarding is already happening, then we need to add the new message to the previous messages
            else:
                message = request.json["message"]
                new_message = {
                    "user_id": user_id,
                    "message": message,
                    "agent": "onboarding",
                    "role": "user",
                }
                messages.append(("user", message))
                dal.add_message(message=new_message)

            messages = [("system", onboarding_prompt)] + messages
            print("Messages ", messages)
            response = GPT(onboarding_model).chat_completion(messages)
            print("Response ", response)
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
                    "role": "assistant",
                }
                dal.add_message(message)

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
                dal.add_info(info)

            if personalityType:
                persona_info = {
                    "user_id": user_id,
                    "info": personalityType,
                    "agent": "onboarding",
                    "tag": "personality_traits",
                }
                dal.add_info(persona_info)

            if bool(overallOnboardingDone):
                user = dal.get_user(user_id=user_id)
                user["OnboardingStatus"] = True
                dal.update_user(user)

            return jsonify(
                {
                    "message": nextQuestion,
                    "overallOnboardingDone": overallOnboardingDone,
                }
            )
        else:
            return jsonify({"message": "Onboarding already done"})
