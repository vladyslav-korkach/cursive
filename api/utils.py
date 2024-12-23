from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt

def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()  # Get all claims from the JWT
            role = claims.get('role')  # Extract the 'role' claim
            current_app.logger.info(f"User role: {role}")  # Log the role
            if role != required_role:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper