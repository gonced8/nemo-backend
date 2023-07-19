from dotenv import load_dotenv
from flask import Flask

from services.exercises import Exercises
from services.onboarding import Onboarding
from services.user import User

app = Flask(__name__)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Add routes
# Onboarding
app.add_url_rule("/user", "user.add", User.add, methods=["POST"])
app.add_url_rule("/user", "user.get", User.get, methods=["GET"])
app.add_url_rule(
    "/user/<user_id>/onboarding", "onboarding", Onboarding.chat, methods=["POST"]
)
# Exercises
app.add_url_rule("/exercises", "exercises.get", Exercises.get, methods=["GET"])
app.add_url_rule(
    "/exercises", "exercises.generate", Exercises.generate, methods=["POST"]
)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
