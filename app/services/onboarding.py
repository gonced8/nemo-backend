import json

from flask import jsonify, request

from app.dal import dal
from app.services.agents import onboarding_model, onboarding_prompt
from app.services.gpt import GPT


class Onboarding:
    @staticmethod
    def chat(user_id):
        # TODO get response in the right format
        """Onboarding function that asks essential questions to the user and saves the answers to the database"""

        overallOnboardingDone = dal.get_user(user_id=user_id)["onboarding_status"]
        if not overallOnboardingDone:
            # Get previous messages
            previous_messages = dal.get_messages(user_id, "onboarding")
            for message in previous_messages:
                if message["role"] == "assistant":
                    message["message"] = {"nextQuestion": message["message"]}
                    info_facts = dal.get_info_by_id(message["id"], "facts")
                    if info_facts:
                        message["message"]["retrievedFacts"] = [
                            info["info"] for info in info_facts
                        ]

                    personality_traits = dal.get_info_by_id(
                        message["id"], "personality_traits"
                    )

                    if personality_traits:
                        message["message"]["personalityType"] = personality_traits[0][
                            "info"
                        ]
                    message["message"] = json.dumps(
                        message["message"], ensure_ascii=False
                    )
                else:
                    pass
            messages = [
                (message["role"], str(message["message"]))
                for message in previous_messages
            ]

            print("Retrieved Messages ", messages)
            print("/n")
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
                message_id = dal.add_message(message=new_message)[0]["id"]

            messages = [("system", onboarding_prompt)] + messages
            print("Messages to gpt ", messages)
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
                next_question_id = dal.add_message(message)[0]["id"]

            if retrievedFacts:
                info = [
                    {
                        "message_id": message_id,
                        "call_id": next_question_id,
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
                    "message_id": message_id,
                    "call_id": next_question_id,
                    "user_id": user_id,
                    "info": personalityType,
                    "agent": "onboarding",
                    "tag": "personality_traits",
                }
                dal.add_info(persona_info)

            if bool(overallOnboardingDone):
                user = dal.get_user(user_id=user_id)
                user["OnboardingStatus"] = True
                dal.update_user(user_id=user_id)

            return jsonify(
                {
                    "message": nextQuestion,
                    "overallOnboardingDone": overallOnboardingDone,
                }
            )
        else:
            return jsonify({"message": "Onboarding already done"})
