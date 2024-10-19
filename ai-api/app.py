import os
from flask import Flask, render_template, request, jsonify
from complaint_filter import ComplaintFilter

app = Flask(__name__)
complaint_filter = ComplaintFilter()

is_production = os.getenv("PROD")


@app.before_request
def check_production_env():
    if is_production:
        return jsonify("page dose not exist"), 404


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        text = request.form["text"]

        result = complaint_filter(text)
        has_topic = result.has_topic
        text_type = result.text_type

        return render_template("index.html", has_topic=has_topic, text_type=text_type)


if __name__ == "__main__":
    app.run()
