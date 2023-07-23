import json
from collections import defaultdict

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

        # Get user time preferences
        info = [
            [info["info"], info["created_at"]] for info in dal.get_info(user_id, "*")
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
        print("resoonse kkkkk: ", response)
        timePreferences = json.loads(response)
        timePreferences = [elem[0] for elem in timePreferences["timeInfo"]]
        print("Time Preferences :", *timePreferences, sep="\n")

        # Get user plans
        planInfo = [
            [plan["plan_name"], plan["estimated_duration"]]
            for plan in dal.get_plans(user_id)
        ]
        print(f"{planInfo=}")

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

        response_dict = defaultdict(list)
        for plan_name, *day_time in response["schedule"]:
            response_dict[plan_name].append(day_time)

        for plan_name, day_time_list in response_dict.items():
            dal.update_schedule(plan_name=plan_name, schedule=day_time_list)
        print("SCHEDULE: ", response)
        # Return shedule
        return jsonify(response)
