import os
from functools import wraps

from flask import Flask, render_template, request, jsonify
from src.feedback_classifier import FeedbackClassifier
from models.gemini_model import GeminiModel

app = Flask(__name__)
feedback_classifier = FeedbackClassifier(GeminiModel())

is_production = os.getenv("PROD")


def internal(func):
    """Mark this route as internal and hide it when the app is on production."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_production:
            return jsonify({"error": "Endpoint does not exist"}), 404
        return func(*args, **kwargs)

    return wrapper


@app.route("/", methods=["POST", "GET"])
@internal
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        text = request.form["text"]

        result = feedback_classifier(text)
        has_topic = result.has_topic
        text_type = result.text_type

        return render_template("index.html", has_topic=has_topic, text_type=text_type)


if __name__ == "__main__":
    app.run()
