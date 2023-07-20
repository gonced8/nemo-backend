import os

from dotenv import load_dotenv
from supabase import Client, create_client

# Load .env file
load_dotenv()


class DAL:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(supabase_url=url, supabase_key=key)

    def get_user(self, user_id: str):
        """ "Get user from user table and return None if doens't exist"""
        user = self.supabase.table("users").select("*").eq("id", user_id).execute()
        if len(user.data) == 0:
            return None
        return user.data[0]

    def add_user(self, username: str):
        """Add new user"""
        user = self.supabase.table("users").insert({"username": username}).execute()
        return user.data[0]

    def get_messages(self, user_id: str, agent: str):
        """Get messages from messages table"""
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

    def add_exercise(self, exercise: list | dict):
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
        info = (
            self.supabase.table("info")
            .select("*")
            .eq("id", user_id)
            .eq("agent", agent)
            .execute()
        )
        return info.data

    def add_info(self, info) -> None:
        """Add info to info table"""
        self.supabase.table("info").insert(info).execute()

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


dal = DAL()
