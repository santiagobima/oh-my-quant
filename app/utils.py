import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import check_password_hash

load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("DATABASE_URL")

def check_user_credentials(username: str, password: str) -> bool:
    
    """Return True if (username, password) is valid according to DB (hash check)."""
    
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT password_hash FROM users WHERE username = %s;
                """,
                (username,)
            )
            row = cur.fetchone()
            
            if row is None:
                return False
            
            stored_hash = row[0]
            
            return check_password_hash(stored_hash, password)
        

def get_user_role(username: str) -> str | None: 
    "Return the role of the user or None if not found."
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT role FROM users WHERE username = %s;""",
                (username,)
            )
            row = cur.fetchone()
            return row[0] if row else None
        
        
