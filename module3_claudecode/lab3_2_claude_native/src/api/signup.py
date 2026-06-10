"""Signup endpoint logic — a second CALLER of login.hash_password, in a different
package. Shows why the migration is genuinely multi-file (and multi-directory)."""
from src.auth.login import hash_password


def register(username: str, password: str, salt: str) -> dict:
    """Create a new user record with a hashed password."""
    return {
        "username": username,
        "salt": salt,
        "password_hash": hash_password(password, salt),
    }
