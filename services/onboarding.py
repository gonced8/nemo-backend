from flask import jsonify, request

def onboarding(user_id: str):
    """Onboarding function that asks essential questions to the user and saves the answers to the database"""
    username = request.json["username"]

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