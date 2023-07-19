from dotenv import load_dotenv
from flask import Flask

from services import exercises, onboarding, user

app = Flask(__name__)

# Load .env file
load_dotenv()

# Add routes
app.add_url_rule("/user", "user.add", user.add, methods=["POST"])
app.add_url_rule("/user", "user.get", user.get, methods=["GET"])
app.add_url_rule(
    "/user/<user_id>/onboarding", "onboarding", onboarding, methods=["POST"]
)
app.add_url_rule(
    "/exercises", "exercises.generate", exercises.generate, methods=["POST"]
)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
