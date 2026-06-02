from functools import wraps
from flask_jwt_extended import get_jwt_identity
from model import User

def role_required(allowed_roles):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args,**kwargs):
            current_user_id = get_jwt_identity()

            current_user = User.query.get(current_user_id)

            if current_user.role not in allowed_roles:
                return {
                    "success":False,
                    "message" : "Access denied"
                },403
            

            return fn(*args,**kwargs)
        
        return wrapper
    return decorator
