from typing import Any

from flask import make_response, jsonify


class Response:
    @staticmethod
    def success(data: Any, status: int = 200):
        response = {
            "status": "SUCCESS",
            "body": data,
        }
        return make_response(jsonify(response), status)

    @staticmethod
    def failure(details: Any, status: int = 400):
        response = {
            "status": "FAILURE",
            "body": details,
        }
        return make_response(jsonify(response), status)

    @staticmethod
    def not_found():
        response = {
            "status": "Failure",
            "body": "Endpoint does not exist",
        }
        return make_response(jsonify(response), 404)
