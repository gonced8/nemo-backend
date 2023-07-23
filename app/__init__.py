from flask import Flask

from app.services.chat import Chat
from app.services.exercises import Exercises
from app.services.onboarding import Onboarding
from app.services.persona import Persona
from app.services.plan_executor import PlanExecutor
from app.services.plans import Plans
from app.services.scheduler import Scheduler
from app.services.user import Users
from app.services.apple_health_kit import AppleHealthKit


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    app.add_url_rule("/", "index", lambda: "Hello, world!", methods=["GET"])

    # Add routes
    # Chat
    app.add_url_rule("/users/<user_id>/chat", "chat", Chat.chat, methods=["POST"])
    # Exercises
    app.add_url_rule("/exercises", "exercises.get", Exercises.get, methods=["GET"])
    app.add_url_rule("/exercises", "exercises.add", Exercises.get, methods=["POST"])
    app.add_url_rule(
        "/exercises/generate", "exercises.generate", Exercises.generate, methods=["GET"]
    )
    # Onboarding
    app.add_url_rule("/users", "user.add", Users.add, methods=["POST"])
    app.add_url_rule("/users", "user.get", Users.get, methods=["GET"])
    app.add_url_rule(
        "/users/<user_id>/onboarding", "onboarding", Onboarding.chat, methods=["POST"]
    )
    # Persona
    app.add_url_rule(
        "/users/<user_id>/persona",
        "persona.get",
        Persona.get,
        methods=["GET"],
    )
    app.add_url_rule(
        "/users/<user_id>/persona",
        "persona.add",
        Persona.add,
        methods=["POST"],
    )
    app.add_url_rule(
        "/users/<user_id>/persona/generate",
        "persona.generate",
        Persona.generate,
        methods=["GET"],
    )
    # Plan Executor
    app.add_url_rule(
        "/users/<user_id>/plan-executor",
        "plan-executor.chat",
        PlanExecutor.chat,
        methods=["POST"],
    )
    app.add_url_rule(
        "/users/<user_id>/plan-executor/feedback",
        "plan-executor.feedback",
        PlanExecutor.feedback_interface,
        methods=["POST"],
    )
    app.add_url_rule(
        "/users/<user_id>/plan-executor/feedback/info",
        "plan-executor.feedback_info",
        PlanExecutor.feedback_info,
        methods=["POST"],
    )
    # Plans
    app.add_url_rule("/users/<user_id>/plans", "plans.get", Plans.get, methods=["GET"])
    app.add_url_rule("/users/<user_id>/plans", "plans.add", Plans.add, methods=["POST"])
    app.add_url_rule(
        "/users/<user_id>/plans/generate",
        "plans.generate",
        Plans.generate,
        methods=["GET"],
    )
    app.add_url_rule(
        "/users/<user_id>/plans/chat", "plans.chat", Plans.chat, methods=["POST"]
    )
    # Scheduler
    app.add_url_rule(
        "/scheduler/<user_id>", "scheduler.call", Scheduler.call, methods=["GET"]
    )
    # User Reset
    app.add_url_rule(
        "/users/<user_id>/reset", "user.reset", Users.reset, methods=["POST"]
    )
    app.add_url_rule(
        "/users/<user_id>/notifications",
        "user.notifications",
        Users.notifications,
        methods=["GET"],
    )
    # INFO
    app.add_url_rule("/users/<user_id>/info", "user.info", Users.info, methods=["POST"])

    # APPLE HEALTH KIT
    app.add_url_rule(
        "/users/apple-health-kit",
        "apple-health-kit.get",
        AppleHealthKit.get,
        methods=["GET"],
    )

    return app
