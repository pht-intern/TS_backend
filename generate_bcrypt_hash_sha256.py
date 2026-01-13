#!/usr/bin/env python3
"""Generate bcrypt hash of SHA-256 hashed password for app_metrics_password"""
import hashlib
from passlib.context import CryptContext

# Initialize CryptContext with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"])

# Original password
original_password = "ShRushti@12$2026"

# Step 1: Hash with SHA-256 (what the client will send)
sha256_hash = hashlib.sha256(original_password.encode('utf-8')).hexdigest()
print("Original Password:", original_password)
print("SHA-256 Hash (what client sends):", sha256_hash)

# Step 2: Hash the SHA-256 hash with bcrypt (what we store in database)
bcrypt_hash = pwd_context.hash(sha256_hash)
print("\nBcrypt Hash of SHA-256 (store in database):", bcrypt_hash)

print("\nSQL Update Command:")
print(f"UPDATE app_metrics_password SET password_hash = '{bcrypt_hash}', updated_at = NOW() WHERE id = (SELECT id FROM (SELECT id FROM app_metrics_password ORDER BY id DESC LIMIT 1) AS t);")

print("\nNote: The client will send the SHA-256 hash, and the server will verify it")
print("against this bcrypt hash using bcrypt's verify function.")
