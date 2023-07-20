from flask import Flask

from app.services.chat import Chat
from app.services.exercises import Exercises
from app.services.onboarding import Onboarding
from app.services.plans import Plans
from app.services.user import Users


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    app.add_url_rule("/", "index", lambda: "Hello, world!", methods=["GET"])

    # Add routes
    # Chat
    app.add_url_rule("/users/<user_id>/chat", "chat", Chat.chat, methods=["POST"])
    # Exercises
    app.add_url_rule("/exercises", "exercises.get", Exercises.get, methods=["GET"])
    app.add_url_rule(
        "/exercises", "exercises.generate", Exercises.generate, methods=["POST"]
    )
    # Onboarding
    app.add_url_rule("/users", "user.add", Users.add, methods=["POST"])
    app.add_url_rule("/users", "user.get", Users.get, methods=["GET"])
    app.add_url_rule(
        "/users/<user_id>/onboarding", "onboarding", Onboarding.chat, methods=["POST"]
    )
    # Plans
    app.add_url_rule("/users/<user_id>/plans", "plans.get", Plans.get, methods=["GET"])
    app.add_url_rule(
        "/users/<user_id>/plans", "users.generate", Plans.generate, methods=["POST"]
    )

    return app
