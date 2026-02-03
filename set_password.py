"""
One-off script to set password for app@tirumakudaluproperties.com.
Run from backend dir: python set_password.py
Uses same DB and hashing as login, so login will work after this.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ensure .env is loaded (backend/.env or project root .env)
try:
    from dotenv import load_dotenv
    from pathlib import Path
    backend_dir = Path(__file__).resolve().parent
    for env_path in [backend_dir / ".env", backend_dir.parent / ".env"]:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            break
except ImportError:
    pass

from database import execute_update, execute_query, test_connection
from utils.auth import get_password_hash, verify_password

EMAIL = "app@tirumakudaluproperties.com"
PASSWORD = "sts@112025$"

def main():
    if not test_connection().get("connected"):
        print("Database connection failed. Check .env (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD).")
        sys.exit(1)
    users = execute_query("SELECT id FROM users WHERE email = %s", (EMAIL,))
    if not users:
        print(f"No user with email {EMAIL}. Create the user first (e.g. run inserts.sql).")
        sys.exit(1)
    password_hash = get_password_hash(PASSWORD)
    if not verify_password(PASSWORD, password_hash):
        print("Hash verification failed.")
        sys.exit(1)
    n = execute_update("UPDATE users SET password_hash = %s, is_active = 1 WHERE email = %s", (password_hash, EMAIL))
    print(f"Updated password for {EMAIL} (rows affected: {n}). You can now log in with password: {PASSWORD!r}")
    sys.exit(0)

if __name__ == "__main__":
    main()
