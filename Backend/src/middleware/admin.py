from functools import wraps
from flask import session, jsonify

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "role" not in session or session["role"] != "admin":
            return jsonify({
                "success": False,
                "error": "Access Denied"
            }), 403
        return f(*args, **kwargs)
    return decorated