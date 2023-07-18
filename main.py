from flask import Flask, jsonify, request
from services import onboarding, user
app = Flask(__name__)


app.add_url_rule('/user',"user.add", user.add, methods=['POST'])
app.add_url_rule('/user',"user.get", user.get, methods=['GET'])
app.add_url_rule('/user/<user_id>/onboarding',"onboarding", onboarding, methods=['POST'])


if __name__ == "__main__":
    app.run(debug=True, port=5000)