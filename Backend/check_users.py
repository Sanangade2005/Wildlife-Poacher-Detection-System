from db import SessionLocal, User

import sys

def list_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        print(f"--- Found {len(users)} Users in 'poacher_db' ---")
        for u in users:
            print(f"ID: {u.id} | RangerID: {u.ranger_id} | Name: {u.first_name} {u.last_name} | Email: {u.email_or_phone}")
        print("-------------------------------------------")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    list_users()
