import json

from flask import jsonify, request

from app.dal import dal
from app.services.agents import scheduler_model, scheduler_prompt
from app.services.gpt import GPT


class Scheduler:
    @staticmethod
    def call(user_id: str):
        # TODO COPILIT Function NEEDS A LOT OF WORK
        """Schedule a plan for the user and returns the schedule."""
        # Get user time preferences
        time_preferences = dal.get_time_preferences(user_id)
        time_preferences = "\n".join(
            json.dumps(time_preference) for time_preference in time_preferences
        )

        # Get user calendar
        occupied_slots = dal.get_occupied_slots(user_id)
        occupied_slots = "\n".join(
            json.dumps(occupied_slot) for occupied_slot in occupied_slots
        )

        # Get plan duration
        plan_duration = dal.get_plan_duration(user_id)

        # Get plan periodicity
        periodicity = dal.get_plan_periodicity(user_id)

        # Generate schedule
        response = GPT(scheduler_model).chat_completion(
            [
                (
                    "system",
                    scheduler_prompt.format(
                        time_preferences=time_preferences,
                        occupied_slots=occupied_slots,
                        plan_duration=plan_duration,
                        periodicity=periodicity,
                    ),
                ),
            ]
        )

        # Parse JSONL to list of dicts
        schedule = [
            json.loads(schedule)
            for schedule in re.sub("\n+", "\n", response).splitlines()
        ]

        # Add schedule to database
        schedule = [schedule | {"user_id": user_id} for schedule in schedule]
        dal.add_schedule(schedule)

        # Return schedule
        return jsonify({"schedule": schedule})
