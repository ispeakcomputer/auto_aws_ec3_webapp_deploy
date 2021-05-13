#!/bin/bash
# Kill python - it might be keeping the key file wrote open
# sudo pkill -9  python3

export AWS_SECRET_ACCESS_KEY=
export AWS_ACCESS_KEY_ID=
export YOUR_AWS_REGION=us-west-1

source venv/bin/activate

python3 app.py

