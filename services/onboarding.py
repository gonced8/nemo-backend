from flask import jsonify, request

from dal import get_messages, get_user


def onboarding(user_id: str):
    """Onboarding function that asks essential questions to the user and saves the answers to the database"""
    username = request.json["username"]
    user = get_user(username)
    messages = get_messages(user, "onboarding") 
    if len(messages) == 0:
        pass
    else:
        pass

    # Generate initial message from bot
    # Add message to supabase
    # Return starting message
    # Get previous messages
    # Save user response
    # Checklist
    # Generate new bot message
    # Save message
    # Return message

    return jsonify({"message": "hello"})