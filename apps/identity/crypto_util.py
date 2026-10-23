"""Keys, passwords, TOTP, and signed tokens for the local identity provider."""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
from pathlib import Path
from typing import Any

import bcrypt
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm

BCRYPT_ROUNDS = 8
BLOCKLIST = {
    "password",
    "123456",
    "12345678",
    "qwerty",
    "letmein",
    "admin123",
    "welcome",
    "password1234567",
}
DEMO_TOTP_SECRET = "JBSWY3DPEHPK3PXP"
RFC_SHA1_SECRET = b"12345678901234567890"


def hash_password(password: str) -> str:
    digest = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=BCRYPT_ROUNDS))
    return digest.decode("ascii")


def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("ascii"))
    except ValueError:
        return False


def dummy_hash() -> str:
    return hash_password("not-a-real-password")


def password_problem(password: str, *, mfa_enrolled: bool) -> str | None:
    length = len(password)
    if length > 64:
        return "Password must be 64 characters or fewer."
    minimum = 8 if mfa_enrolled else 15
    if length < minimum:
        if mfa_enrolled:
            return "Password must be at least 8 characters when a one-time code is enrolled."
        return "Password must be at least 15 characters, or 8 when a one-time code is enrolled."
    if password.casefold() in BLOCKLIST:
        return "That password is on the blocklist."
    return None


def totp_at(secret: str | bytes, when: int, *, ascii_secret: bool = False) -> str:
    import pyotp

    if ascii_secret:
        raw = secret if isinstance(secret, bytes) else secret.encode("ascii")
        secret = base64.b32encode(raw).decode("ascii").rstrip("=")
    return pyotp.TOTP(secret).at(when)


def totp_ok(secret: str, code: str, when: float) -> bool:
    import pyotp

    if not secret or not code:
        return False
    return bool(pyotp.TOTP(secret).verify(code.strip(), for_time=when, valid_window=1))


def current_step(when: float) -> int:
    return int(when) // 30


def load_or_create_key(directory: Path) -> tuple[bytes, Any, str]:
    path = directory / "signing_key.pem"
    if path.is_file():
        private_pem = path.read_bytes()
    else:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        path.write_bytes(private_pem)
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    private_key = serialization.load_pem_private_key(private_pem, password=None)
    public_key = private_key.public_key()
    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    kid = hashlib.sha256(der).hexdigest()[:16]
    jwk = json_jwk(public_key, kid)
    jwks_path = directory / "jwks.json"
    import json

    jwks_path.write_text(json.dumps({"keys": [jwk]}), encoding="utf-8")
    return private_pem, public_key, kid


def json_jwk(public_key: Any, kid: str) -> dict[str, Any]:
    import json

    data = json.loads(RSAAlgorithm.to_jwk(public_key))
    data["kid"] = kid
    data["use"] = "sig"
    data["alg"] = "RS256"
    return data


def sign_jwt(payload: dict[str, Any], private_pem: bytes, kid: str) -> str:
    return jwt.encode(payload, private_pem, algorithm="RS256", headers={"kid": kid})


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def hashes_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
