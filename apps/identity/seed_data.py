"""Dummy users and clients for the local identity provider."""
from __future__ import annotations

import json
import sqlite3

from apps.identity.crypto_util import DEMO_TOTP_SECRET, hash_password

DEMO_PASSWORD = "ForceFab-Demo-2026!"

USERS = (
    ("reviewer.tw", "Mei Chen", ("RT-01",), ("FAB-01",), True),
    ("shiftlead.tw", "Wei Lin", ("RT-02",), ("FAB-01",), True),
    ("engineer.az", "Jordan Patel", ("RT-03",), ("FAB-02",), True),
    ("policy.owner", "Sofia Alvarez", ("RT-04",), ("FAB-01", "FAB-02"), True),
    ("analyst.az", "Liam Brooks", ("RT-05",), ("FAB-02",), False),
    ("opslead", "Ava Huang", ("RT-06",), ("FAB-01", "FAB-02"), True),
    ("admin", "Force Fab Admin", ("FF-ADMIN",), ("FAB-01", "FAB-02"), True),
    ("auditor", "Grace Kim", ("FF-AUDITOR",), ("FAB-01", "FAB-02"), True),
    ("breakglass", "Break Glass", ("FF-ADMIN", "RT-02"), ("FAB-01", "FAB-02"), True),
)

CLIENTS = (
    (
        "force-fab-app-a",
        "confidential",
        "dev-secret-a",
        (
            "http://127.0.0.1:8100/auth/callback",
            "http://localhost:8100/auth/callback",
        ),
        "force-fab-app-a",
    ),
    (
        "force-fab-app-b",
        "confidential",
        "dev-secret-b",
        (
            "http://127.0.0.1:8110/auth/callback",
            "http://localhost:8110/auth/callback",
        ),
        "force-fab-app-b",
    ),
    ("force-fab-svc-a", "client_credentials", "dev-svc-a", (), "force-fab-lake"),
    ("force-fab-svc-b", "client_credentials", "dev-svc-b", (), "force-fab-lake"),
    ("force-fab-scim", "client_credentials", "dev-scim", (), "force-fab-scim"),
)

ROLES = (
    "RT-01",
    "RT-02",
    "RT-03",
    "RT-04",
    "RT-05",
    "RT-06",
    "FF-ADMIN",
    "FF-AUDITOR",
    "SVC",
    "SCIM",
)


def seed(conn: sqlite3.Connection) -> None:
    existing = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    if existing:
        return
    for name in ROLES:
        conn.execute("INSERT OR IGNORE INTO roles(name) VALUES (?)", (name,))
    password_hash = hash_password(DEMO_PASSWORD)
    for username, name, roles, sites, enrolled in USERS:
        secret = DEMO_TOTP_SECRET if enrolled else None
        cur = conn.execute(
            """
            INSERT INTO users(username, name, email, password_hash, active, mfa_secret, mfa_enrolled)
            VALUES (?, ?, ?, ?, 1, ?, ?)
            """,
            (username, name, f"{username}@force-fab.local", password_hash, secret, 1 if enrolled else 0),
        )
        user_id = cur.lastrowid
        for role in roles:
            conn.execute("INSERT INTO user_roles(user_id, role) VALUES (?, ?)", (user_id, role))
        for site in sites:
            conn.execute("INSERT INTO user_sites(user_id, site) VALUES (?, ?)", (user_id, site))
    for client_id, client_type, secret, redirects, aud in CLIENTS:
        conn.execute(
            """
            INSERT INTO clients(client_id, secret_hash, client_type, redirect_uris, token_aud)
            VALUES (?, ?, ?, ?, ?)
            """,
            (client_id, hash_password(secret), client_type, json.dumps(list(redirects)), aud),
        )
    conn.commit()
