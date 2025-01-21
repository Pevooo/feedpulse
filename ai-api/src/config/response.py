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
