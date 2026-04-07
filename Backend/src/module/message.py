from flask import Blueprint, request, jsonify, session
from src.database import get_conn
from src.utils.activity_logger import log_activity  # ✅ Import logger

messages_bp = Blueprint("messages", __name__)

# ===== SAVE MESSAGE =====
@messages_bp.route("/save_message", methods=["POST"])
def save_message():
    data = request.get_json()
    user_id = data.get("userId")
    message_text = data.get("message")

    if not user_id or not message_text:
        return jsonify({"error": "User ID and message are required"}), 400

    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO public.messages (user_id, message_text) VALUES (%s, %s) RETURNING id;",
                (user_id, message_text)
            )
            msg_id = cursor.fetchone()[0]
            conn.commit()

        # ✅ LOG ACTIVITY: This records that a user sent a message
        username = session.get("user_name") or f"User:{user_id}"
        log_activity(username, "SEND_MESSAGE", message_text[:50]) # Log first 50 chars

        return jsonify({"message": "Message saved", "id": msg_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# ===== GET MESSAGES (No change needed) =====
@messages_bp.route("/get_messages/<int:user_id>", methods=["GET"])
def get_messages(user_id):
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, message_text, created_at FROM public.messages WHERE user_id=%s ORDER BY created_at ASC;",
                (user_id,)
            )
            rows = cursor.fetchall()
        messages = [{"id": r[0], "message": r[1], "created_at": str(r[2])} for r in rows]
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# ===== DELETE ALL MESSAGES =====
@messages_bp.route("/delete_all/<int:user_id>", methods=["DELETE"])
def delete_all_messages(user_id):
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM public.messages WHERE user_id=%s;", (user_id,))
            conn.commit()
            
        # ✅ LOG ACTIVITY
        username = session.get("user_name") or "System"
        log_activity(username, "DELETE_CHAT", "Cleared all messages")

        return jsonify({"success": True}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()