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

    def get_user(self, username: str):
        """ "Get user from user table adn return None if doens't exist"""
        user = (
            self.supabase.table("users").select("*").eq("username", username).execute()
        )
        if len(user.data) == 0:
            return None
        return user.data[0]

    def add_user(self, username: str):
        """Add new user"""
        user = self.supabase.table("users").insert({"username": username}).execute()
        return user.data[0]

    def save_message(self, user_id: str, message: str, agent: str):
        """Save message to messages table"""
        self.supabase.table("messages").insert(
            {"user_id": user_id, "message": message, "agent": agent}
        ).execute()

    def get_messages(self, user_id: str, agent: str):
        """Get messages from messages table"""
        messages = (
            self.supabase.table("messages")
            .select("*")
            .eq("user_id", user_id)
            .eq("agent", agent)
            .execute()
        )
        return messages.data

    def add_message(self, user_id: str, message: str, agent: str, speaker: str):
        """Add message to messages table"""
        self.supabase.table("messages").insert(
            {"user_id": user_id, "message": message, "agent": agent, "speaker": speaker}
        ).execute()


dal = DAL()
