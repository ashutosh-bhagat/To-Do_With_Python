import hashlib

users_db = {}  # username: hashed_password

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    if username in users_db:
        return False
    users_db[username] = hash_password(password)
    return True

def verify_user(username: str, password: str) -> bool:
    hashed = hash_password(password)
    return users_db.get(username) == hashed
