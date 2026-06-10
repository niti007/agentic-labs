"""Session handling — a CALLER of login.verify. One of the files a password-hashing
migration would have to touch."""
from src.auth.login import verify


# Fake user store: username -> (salt, stored_hash)
_USERS = {
    "nitish": ("s1", "8f4e...placeholder"),
}


def login_user(username: str, password: str) -> bool:
    """Return True if the username exists and the password verifies."""
    if username not in _USERS:
        return False
    salt, stored_hash = _USERS[username]
    return verify(password, salt, stored_hash)
