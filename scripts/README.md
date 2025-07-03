# Environment File Management

This directory contains scripts for managing encrypted environment files using the `cryptography` library.

## Setup

1. **Install dependencies:**

   ```bash
   uv sync --dev
   ```

2. **Create your `.env.test` file** with your test API keys:

   ```bash
   # .env.test
   OPENAI_API_KEY=your_openai_test_key_here
   ANTHROPIC_API_KEY=your_anthropic_test_key_here
   GOOGLE_API_KEY=your_google_test_key_here
   ```

3. **Encrypt the file:**

   ```bash
   uv run python scripts/env_vault.py encrypt
   ```

4. **Commit the encrypted files:**
   ```bash
   git add .env.test.vault .env.key
   git commit -m "Add encrypted test environment file"
   ```

## For Other Developers

1. **Clone the repository** (includes `.env.test.vault`)

2. **Decrypt the environment file:**

   ```bash
   uv run python scripts/env_vault.py decrypt
   ```

3. **Run tests:**
   ```bash
   uv run pytest tests/ -v
   ```

## Commands

- **Encrypt:** `uv run python scripts/env_vault.py encrypt`
- **Decrypt:** `uv run python scripts/env_vault.py decrypt`

## Security Notes

- The `.env.test.vault` file is safe to commit to version control
- The `.env.key` file should be in your `.gitignore` (but you need to share it with your team)
- The `.env.test` file should be in your `.gitignore`
- Share both `.env.test.vault` and `.env.key` files with your team
- For production, use proper secret management (GitHub Secrets, etc.)

## Troubleshooting

If you get errors about missing `.env.test` or `.env.test.vault` files:

1. Make sure you have the correct file in your repository
2. Check that you're running the commands from the project root
3. Ensure `python-dotenv-vault` is installed: `uv sync --dev`
