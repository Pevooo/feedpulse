from collections.abc import Callable
from typing import Any

from flask import make_response, jsonify


class Response:
    @staticmethod
    def success(data: Any, status: int = 200):
        response = {
            "status": "SUCCESS",
            "code": status,
            "body": data,
        }
        return make_response(jsonify(response))

    @staticmethod
    def failure(details: Any, status: int = 400):
        response = {
            "status": "FAILURE",
            "code": status,
            "body": details,
        }
        return make_response(jsonify(response))

    @staticmethod
    def not_found():
        response = {
            "status": "FAILURE",
            "code": 404,
            "body": "Endpoint does not exist",
        }
        return make_response(jsonify(response))

    @staticmethod
    def pending():
        response = {
            "status": "PENDING",
            "code": 102,
            "body": "Request in progress",
        }
        return make_response(jsonify(response))

    @staticmethod
    def server_error():
        response = {
            "status": "FAILURE",
            "code": 500,
            "body": "Server error",
        }
        return make_response(jsonify(response))

    @staticmethod
    def deprecated(original_response: Callable[[Any], Any]) -> Any:
        def wrapped(*args, **kwargs):
            # Get the original response
            original = original_response(*args, **kwargs)

            # Modify the response to add a deprecation notice
            modified_response = original.get_json()
            modified_response["deprecation_warning"] = (
                "This endpoint is deprecated and will be removed in future versions."
            )

            # Return the modified response
            return make_response(jsonify(modified_response), original.status_code)

        return wrapped