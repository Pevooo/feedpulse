import os
from flask import Flask, render_template, request, jsonify
from src.feedback_classifier import FeedbackClassifier
from models.gemini_model import GeminiModel

app = Flask(__name__)
feedback_classifier = FeedbackClassifier(GeminiModel())

is_production = os.getenv("PROD")


@app.before_request
def check_production_env():
    # If this is running on production, don't show the testing functionallity
    if is_production:
        return jsonify("page dose not exist"), 404


@app.route("/", methods=["POST", "GET"])
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
