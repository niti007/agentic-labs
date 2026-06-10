"""Tests for the auth core — the migration must update these too (they assert on the
current sha256 behavior)."""
from src.auth.login import hash_password, verify


def test_hash_is_deterministic():
    assert hash_password("hunter2", "salt") == hash_password("hunter2", "salt")


def test_verify_accepts_correct_password():
    h = hash_password("hunter2", "salt")
    assert verify("hunter2", "salt", h) is True


def test_verify_rejects_wrong_password():
    h = hash_password("hunter2", "salt")
    assert verify("wrong", "salt", h) is False
