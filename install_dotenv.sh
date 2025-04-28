#!/usr/bin/env bash

# Navigate to your project directory
cd ~/Downloads/reflections_bot_live || exit 1

echo "Installing python-dotenv for your Python 3 environment..."

# Install or upgrade python-dotenv using the python3 interpreter
python3 -m pip install --upgrade python-dotenv

# Verify installation
echo "Verifying installation..."
python3 - << 'EOF'
try:
    import dotenv
    print(f"✅ python-dotenv version: {dotenv.__version__}")
except Exception as e:
    echo "❌ Failed to import python-dotenv";
    exit(1)
EOF

echo "Setup complete. Now restart your Python shell and retry send_trade_log_email()."

