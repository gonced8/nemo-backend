import os
import uuid

from dotenv import load_dotenv
from supabase import Client, create_client

# Load .env file
load_dotenv()


class DAL:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(supabase_url=url, supabase_key=key)

    # Checks if string is valid UUID:
    def is_valid_uuid(self, uuid_to_test: str) -> bool:
        """Check if uuid_to_test is a valid UUID."""
        try:
            uuid_obj = uuid.UUID(uuid_to_test)
        except ValueError:
            return False

        return str(uuid_obj) == uuid_to_test

    def get_user(self, user_id: str):
        """ "Get user from user table and return None if doens't exist"""

        if self.is_valid_uuid(user_id.lower()):
            user = (
                self.supabase.table("users")
                .select("*")
                .eq("id", user_id.lower())
                .execute()
            )
        else:
            user = (
                self.supabase.table("users")
                .select("*")
                .eq("username", user_id)
                .execute()
            )

        if len(user.data) == 0:
            return None
        return user.data[0]

    def add_user(self, username: str):
        """Add new user"""
        user = self.supabase.table("users").insert({"username": username}).execute()
        return user.data[0]

    def get_messages(self, user_id: str, agent: str):
        """Get messages from messages table"""
        if agent == "*":
            messages = (
                self.supabase.table("messages")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )

        else:
            messages = (
                self.supabase.table("messages")
                .select("*")
                .eq("user_id", user_id)
                .eq("agent", agent)
                .order("created_at")
                .execute()
            )
        return messages.data

    def add_message(self, message: dict):
        """Add message to messages table"""
        message = self.supabase.table("messages").insert(message).execute()
        return message.data

    def add_exercise(self, exercise):
        """Adds exercise to exercises table"""
        print(exercise)
        self.supabase.table("exercises").insert(exercise).execute()

    def get_exercises(self) -> list[dict]:
        """Get exercises from exercises table"""
        exercises = self.supabase.table("exercises").select("*").execute()
        return exercises.data

    def get_exercises_names(self) -> list[str]:
        """Get exercise names from exercises table"""
        exercises = self.supabase.table("exercises").select("exercise_name").execute()
        return [exercise["exercise_name"] for exercise in exercises.data]

    def add_plans(self, plans: list[dict]):
        """Adds plans to plans table"""
        self.supabase.table("plans").insert(plans).execute()

    def get_plans(self, user_id: str) -> list[dict]:
        """Get plans of user_id from plans table"""
        plans = (
            self.supabase.table("plans").select("*").eq("user_id", user_id).execute()
        )
        return plans.data

    def get_plans_names(self, user_id: str) -> list[str]:
        """Get plans names of user_id from plans table"""
        plans = (
            self.supabase.table("plans")
            .select("plan_name")
            .eq("user_id", user_id)
            .execute()
        )
        return [plan["plan_name"] for plan in plans.data]

    def get_info(self, user_id: str, agent: str):
        """Get info from info table"""
        if agent == "*":
            info = (
                self.supabase.table("info")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=False)
                .execute()
            )
        else:
            info = (
                self.supabase.table("info")
                .select("*")
                .eq("user_id", user_id)
                .eq("agent", agent)
                .execute()
            )
        return info.data

    def update_schedule(self, plan_name: str, schedule: list[list]):
        """Update schedule in plans table"""
        self.supabase.table("plans").update({"schedule": schedule}).eq(
            "plan_name", plan_name
        ).execute()

    def add_info(self, info) -> list[dict]:
        """Add info to info table"""
        info = self.supabase.table("info").insert(info).execute()
        return info.data

    def get_info_by_id(self, message_id: str, tag: str) -> dict:
        """Get info by id from info table"""
        info = (
            self.supabase.table("info")
            .select("*")
            .eq("call_id", message_id)
            .eq("tag", tag)
            .execute()
        )
        return info.data

    def update_user(self, user_id: str):
        """Update user in users table"""
        self.supabase.table("users").update({"onboarding_status": True}).eq(
            "id", user_id
        ).execute()

    def reset_user(self, user_id: str, tables: list[str]):
        """Reset user in users table"""

        deleted = [
            self.supabase.table(table).delete().eq("id", user_id).execute()
            for table in tables
        ]
        print(f"Deleted Tables: {tables} for user {user_id}")

    def add_planner_chats(self, message):
        """Add planner chats to planner_chats table"""
        message = self.supabase.table("planner_chats").insert(message).execute()
        return message.data

    def get_planner_chats_last_chat_id(self, user_id: str):
        """Get last chat_id from user_id in planner_chats table"""
        last_chat_id = (
            self.supabase.table("planner_chats")
            .select("chat_id")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
            .data[0]["chat_id"]
        )
        return last_chat_id

    def get_planner_chats_by_chat_id(self, chat_id: str):
        """Get planner chats from user_id that match the last chat_id"""
        messages = (
            self.supabase.table("planner_chats")
            .select("*")
            .eq("chat_id", chat_id)
            .execute()
        )

        return messages.data

    def get_persona(self, user_id: str):
        """Get persona from user_id in personas table"""
        persona = (
            self.supabase.table("personas").select("*").eq("user_id", user_id).execute()
        )
        return persona.data

    def add_persona(self, persona: dict):
        """Add persona to personas table"""
        persona = self.supabase.table("personas").insert(persona).execute()
        return persona.data


dal = DAL()
