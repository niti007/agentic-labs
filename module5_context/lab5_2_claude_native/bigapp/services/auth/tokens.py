"""Auth — token helpers. (Sample file, just here to be explored.)"""
from shared.utils import now_ts


def issue_token(user):
    return f"{user}.{now_ts()}"
