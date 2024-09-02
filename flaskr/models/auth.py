from flask import request, make_response, jsonify
from functools import wraps
import jwt
import os

# Authentication decorator
def authenticate_route(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            
        if not token:
            return make_response(jsonify({'message': 'A valid token is missing!'}), 401)
        
        try:
            jwt.decode(token, os.getenv('SECRET_KEY', 'test-key'), algorithms=['HS256'])
        except:
            return make_response(jsonify({'message': 'Unauthorized'}), 401)
        
        return f(*args, **kwargs)
    return decorator