"""Auth core. The MIGRATION TARGET for the Plan-mode demo: hashing currently uses
sha256; the lab task is to migrate this to a salted bcrypt-style API and update every
caller + test. Intentionally simple."""
import hashlib


def hash_password(password: str, salt: str) -> str:
    """Hash a password with a salt. (Demo uses sha256; real code: bcrypt/argon2.)"""
    return hashlib.sha256((salt + password).encode()).hexdigest()


def verify(password: str, salt: str, stored_hash: str) -> bool:
    """Return True if the password matches the stored hash."""
    return hash_password(password, salt) == stored_hash
