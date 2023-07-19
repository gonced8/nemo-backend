from dotenv import load_dotenv
from flask import Flask

from services.exercises import Exercises
from services.onboarding import Onboarding
from services.user import User

app = Flask(__name__)

# Add routes
app.add_url_rule("/user", "user.add", User.add, methods=["POST"])
app.add_url_rule("/user", "user.get", User.get, methods=["GET"])
app.add_url_rule(
    "/user/<user_id>/onboarding", "onboarding", Onboarding.chat, methods=["POST"]
)
app.add_url_rule(
    "/exercises", "exercises.generate", Exercises.generate, methods=["POST"]
)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
