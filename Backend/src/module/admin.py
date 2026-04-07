from flask import Blueprint, jsonify
from src.database import get_conn
from src.middleware.admin import admin_required

# ✅ Blueprint define (VERY IMPORTANT)
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/activities", methods=["GET"])
@admin_required
def get_activities():
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_name, action, message, created_at
            FROM activities
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        data = []
        for r in rows:
            data.append({
                "user": r[0],
                "action": r[1],
                "message": r[2],
                "time": r[3]
            })

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500