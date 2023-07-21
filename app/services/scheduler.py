import json

from flask import jsonify, request

from app.dal import dal
from app.services.agents import (
    scheduler_model,
    scheduler_prompt,
    time_preferences_model,
    time_preferences_prompt,
)
from app.services.gpt import GPT


class Scheduler:
    @staticmethod
    def call(user_id: str):
        """Call the scheduler agent and returns a schedule for the user."""

        # Get user plans
        planInfo = [
            (plan["plan_name"], plan["estimated_duration"])
            for plan in dal.get_plans(user_id)
        ]

        # Get user time preferences
        info = [
            (info["info"], info["created_at"]) for info in dal.get_info(user_id, "*")
        ]
        print("INFO: ", info)
        response = GPT(time_preferences_model).chat_completion(
            [
                (
                    "system",
                    time_preferences_prompt.format(
                        timeInfo=info,
                    ),
                )
            ]
        )
        timePreferences = json.loads(response)
        print("Time Preferences :", response)

        # Get user calendar
        notAvailableSlots = request.json["calendar"]

        response = GPT(scheduler_model).chat_completion(
            [
                (
                    "system",
                    scheduler_prompt.format(
                        timePreferences=timePreferences,
                        notAvailableSlots=notAvailableSlots,
                        planInfo=planInfo,
                    ),
                )
            ]
        )

        response = json.loads(response)

        for key in response["scheduledDays"].keys():
            dal.update_schedule(plan_name=key, schedule=response["scheduledDays"][key])

        # Return shedule
        return jsonify({"schedule": response})
