from flask import jsonify, request

def onboarding(user_id: str):
    start = request.args.get("start", False)
    username = request.json["username"]

    if start:
        # Generate initial message from bot
        # Add message to supabase
        # Return starting message
        pass
    else:
        pass
        # Get previous messages
        # Save user response
        # Checklist
        # Generate new bot message
        # Save message
        # Return message

    return jsonify({"message": "hello"})