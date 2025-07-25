from datetime import datetime, timedelta
from typing import Dict

MAX_FAILED_ATTEMPTS = 5
LOCK_TIME_MINUTES = 15

# In-memory storage for login attempts
_attempts: Dict[str, Dict[str, any]] = {}


def _get_info(identifier: str) -> Dict[str, any]:
    return _attempts.setdefault(identifier, {"count": 0, "lock_until": None, "last": None})


def is_locked(identifier: str) -> bool:
    info = _attempts.get(identifier)
    if not info:
        return False
    lock_until = info.get("lock_until")
    if lock_until and lock_until > datetime.now():
        return True
    if lock_until and lock_until <= datetime.now():
        # Lock expired, reset info
        _attempts.pop(identifier, None)
    return False


def record_failed_attempt(identifier: str) -> None:
    info = _get_info(identifier)
    now = datetime.now()
    if info["last"] and now - info["last"] > timedelta(minutes=LOCK_TIME_MINUTES):
        # Reset counter after lock window passes
        info["count"] = 0
    info["last"] = now
    info["count"] += 1
    if info["count"] >= MAX_FAILED_ATTEMPTS:
        info["lock_until"] = now + timedelta(minutes=LOCK_TIME_MINUTES)


def reset_attempts(identifier: str) -> None:
    _attempts.pop(identifier, None)
