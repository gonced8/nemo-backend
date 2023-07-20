from dotenv import load_dotenv
from flask import Flask

from services.exercises import Exercises
from services.onboarding import Onboarding
from services.plans import Plans
from services.user import Users
from services.chat import Chat

app = Flask(__name__)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Add routes
# Onboarding
app.add_url_rule("/users", "user.add", Users.add, methods=["POST"])
app.add_url_rule("/users", "user.get", Users.get, methods=["GET"])
app.add_url_rule(
    "/users/<user_id>/onboarding", "onboarding", Onboarding.chat, methods=["POST"]
)
# Exercises
app.add_url_rule("/exercises", "exercises.get", Exercises.get, methods=["GET"])
app.add_url_rule(
    "/exercises", "exercises.generate", Exercises.generate, methods=["POST"]
)
# Plans
app.add_url_rule("/users/<user_id>/plans", "plans.get", Plans.get, methods=["GET"])
app.add_url_rule(
    "/users/<user_id>/plans", "users.generate", Plans.generate, methods=["POST"]
)
# Chat
app.add_url_rule("/users/<user_id>/chat", "chat", Chat.chat, methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
