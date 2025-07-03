#!/usr/bin/env python3
"""
Scripts for handling encrypted environment files using cryptography.
"""

import sys
from pathlib import Path

from cryptography.fernet import Fernet


def generate_key():
    """Generate a new encryption key."""
    return Fernet.generate_key()


def save_key(key, key_file=".env.key"):
    """Save the encryption key to a file."""
    with open(key_file, "wb") as f:
        f.write(key)
    print(f"🔑 Key saved to {key_file}")


def load_key(key_file=".env.key"):
    """Load the encryption key from a file."""
    try:
        with open(key_file, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Key file {key_file} not found!")
        print("Please ensure you have the encryption key file.")
        sys.exit(1)


def encrypt_env():
    """Encrypt .env.test file using cryptography."""
    env_file = Path(".env.test")
    vault_file = Path(".env.test.vault")
    key_file = Path(".env.key")

    if not env_file.exists():
        print("❌ .env.test file not found!")
        print("Please create a .env.test file with your test API keys first.")
        sys.exit(1)

    print("🔐 Encrypting .env.test file...")

    # Generate or load key
    if key_file.exists():
        key = load_key()
        print("🔑 Using existing key")
    else:
        key = generate_key()
        save_key(key)
        print("🔑 Generated new key")

    # Create Fernet cipher
    f = Fernet(key)

    # Read and encrypt the file
    with open(env_file, "rb") as file:
        data = file.read()

    encrypted_data = f.encrypt(data)

    # Save encrypted data
    with open(vault_file, "wb") as file:
        file.write(encrypted_data)

    print("✅ Successfully encrypted .env.test")
    print(f"📁 Created {vault_file}")
    print("💡 Share both .env.test.vault and .env.key files with your team")
    print("⚠️  Make sure .env.key is in your .gitignore!")


def decrypt_env():
    """Decrypt .env.test file using cryptography."""
    vault_file = Path(".env.test.vault")
    key_file = Path(".env.key")
    env_file = Path(".env.test")

    if not vault_file.exists():
        print("❌ .env.test.vault file not found!")
        print("Please ensure the encrypted .env.test.vault file is present.")
        sys.exit(1)

    if not key_file.exists():
        print("❌ .env.key file not found!")
        print("Please ensure you have the encryption key file.")
        sys.exit(1)

    print("🔓 Decrypting .env.test file...")

    # Load key and create cipher
    key = load_key()
    f = Fernet(key)

    # Read and decrypt the file
    with open(vault_file, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except Exception:  # noqa: F841
        print("❌ Failed to decrypt file. Invalid key or corrupted data.")
        sys.exit(1)

    # Save decrypted data
    with open(env_file, "wb") as file:
        file.write(decrypted_data)

    print("✅ Successfully decrypted .env.test")
    print(f"📁 Created {env_file}")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/env_vault.py [encrypt|decrypt]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "encrypt":
        encrypt_env()
    elif command == "decrypt":
        decrypt_env()
    else:
        print("Invalid command. Use 'encrypt' or 'decrypt'")
        sys.exit(1)


if __name__ == "__main__":
    main()
