"""SQLite tables for the local identity provider."""
from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    mfa_secret TEXT,
    mfa_enrolled INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,
    locked_until REAL NOT NULL DEFAULT 0,
    lock_strikes INTEGER NOT NULL DEFAULT 0,
    break_glass_until REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS roles (
    name TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (user_id, role)
);
CREATE TABLE IF NOT EXISTS user_sites (
    user_id INTEGER NOT NULL,
    site TEXT NOT NULL,
    PRIMARY KEY (user_id, site)
);
CREATE TABLE IF NOT EXISTS clients (
    client_id TEXT PRIMARY KEY,
    secret_hash TEXT NOT NULL,
    client_type TEXT NOT NULL,
    redirect_uris TEXT NOT NULL,
    token_aud TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS auth_requests (
    request_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    redirect_uri TEXT NOT NULL,
    state TEXT NOT NULL,
    nonce TEXT NOT NULL,
    code_challenge TEXT NOT NULL,
    acr_values TEXT NOT NULL DEFAULT '',
    prompt TEXT NOT NULL DEFAULT '',
    user_id INTEGER,
    stage TEXT NOT NULL,
    exp REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS auth_codes (
    code_hash TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    redirect_uri TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    nonce TEXT NOT NULL,
    code_challenge TEXT NOT NULL,
    exp REAL NOT NULL,
    used INTEGER NOT NULL DEFAULT 0,
    acr TEXT NOT NULL,
    amr TEXT NOT NULL,
    auth_time INTEGER NOT NULL,
    sid TEXT NOT NULL,
    break_glass INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sessions (
    sid TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    csrf TEXT NOT NULL,
    acr TEXT NOT NULL,
    amr TEXT NOT NULL,
    auth_time INTEGER NOT NULL,
    exp REAL NOT NULL,
    break_glass INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS refresh_tokens (
    token_hash TEXT PRIMARY KEY,
    family_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    client_id TEXT NOT NULL,
    exp REAL NOT NULL,
    used INTEGER NOT NULL DEFAULT 0,
    revoked INTEGER NOT NULL DEFAULT 0,
    acr TEXT NOT NULL,
    amr TEXT NOT NULL,
    auth_time INTEGER NOT NULL,
    sid TEXT NOT NULL,
    break_glass INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS revoked_jti (
    jti TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS jit_requests (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    minutes INTEGER NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    approver_id INTEGER,
    created REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS jit_grants (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    elevated_until REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS access_reviews (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS review_items (
    id INTEGER PRIMARY KEY,
    review_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    decision TEXT NOT NULL DEFAULT '',
    comment TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS auth_events (
    seq INTEGER PRIMARY KEY,
    prev_hash TEXT NOT NULL,
    hash TEXT NOT NULL,
    body TEXT NOT NULL,
    created REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS login_attempts (
    id INTEGER PRIMARY KEY,
    ip TEXT NOT NULL,
    at_ts REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS totp_steps (
    user_id INTEGER NOT NULL,
    step INTEGER NOT NULL,
    PRIMARY KEY (user_id, step)
);
"""


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=DELETE")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn
