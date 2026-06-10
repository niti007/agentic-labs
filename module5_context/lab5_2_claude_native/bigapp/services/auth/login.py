"""Auth — login check. (Sample file, just here to be explored.)"""
from shared.utils import now_ts


def login(user, password, store):
    rec = store.get(user)
    if not rec:
        return {"ok": False, "at": now_ts()}
    return {"ok": rec["password"] == password, "at": now_ts()}
