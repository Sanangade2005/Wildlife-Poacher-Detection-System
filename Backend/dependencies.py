from db import SessionLocal

def get_db():
    return SessionLocal()
