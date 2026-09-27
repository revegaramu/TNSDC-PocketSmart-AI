import secrets

from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return a secure password hash."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its stored hash."""
    try:
        return password_hasher.verify(password, hashed_password)
    except Exception:
        return False


def create_session_token() -> str:
    """Create a cryptographically random session token."""
    return secrets.token_urlsafe(32)