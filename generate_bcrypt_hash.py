#!/usr/bin/env python3
"""Simple script to generate bcrypt hash for app_metrics_password"""
from passlib.context import CryptContext

# Initialize CryptContext with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"])

# Password
password = "ShRushti@12$2026"

# Generate hash
password_hash = pwd_context.hash(password)

print("Password:", password)
print("Bcrypt Hash:", password_hash)
print("\nSQL Update Command:")
print(f"UPDATE app_metrics_password SET password_hash = '{password_hash}', updated_at = NOW() WHERE id = (SELECT id FROM (SELECT id FROM app_metrics_password ORDER BY id DESC LIMIT 1) AS t);")
