from src.database import get_conn

def log_activity(user_name, action, message=""):
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            # We use public.activities to match your schema
            cursor.execute("""
                INSERT INTO public.activities (user_name, action, message)
                VALUES (%s, %s, %s)
            """, (user_name, action, message))
            conn.commit()
    except Exception as e:
        print(f"❌ Logging Error: {e}")
        conn.rollback()
    finally:
        conn.close()