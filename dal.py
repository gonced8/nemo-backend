import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_user(username: str):
    """"Get user from user table adn return None if doens't exist"""
    user = supabase.table('users').select("*").eq('username', username).execute()
    if len(user.data) == 0:
        return None
    return user.data[0]
     
def add_user(username: str):
    """Add new user"""
    user = supabase.table('users').insert({'username': username}).execute()
    return user.data[0]

def save_message(user_id: str, message: str, agent: str):
    """Save message to messages table"""
    supabase.table('messages').insert({'user_id': user_id, 'message': message, 'agent':agent}).execute()
        

def get_messages(user_id: str, agent: str):
    """Get messages from messages table""" 
    messages = supabase.table('messages').select("*").eq('user_id', user_id).eq('agent', agent).execute()
    return messages.data

def add_message(user_id: str, message: str, agent: str,speaker:str):
    """Add message to messages table"""
    supabase.table('messages').insert({'user_id': user_id, 'message': message, 'agent':agent, 'speaker':speaker}).execute()