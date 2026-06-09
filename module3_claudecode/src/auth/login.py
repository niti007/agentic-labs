"""Sample auth module so the path-specific rules + Plan mode have real code
to act on. Intentionally simple."""
import hashlib


def hash_password(password: str, salt: str) -> str:
    """Hash a password with a salt. (Demo uses sha256; real code: bcrypt/argon2.)"""
    return hashlib.sha256((salt + password).encode()).hexdigest()


def verify(password: str, salt: str, stored_hash: str) -> bool:
    """Return True if the password matches the stored hash."""
    return hash_password(password, salt) == stored_hash
