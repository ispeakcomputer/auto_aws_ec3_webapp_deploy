#!/bin/bash
#run chmod +x start_here.sh to make this file execute

export AWS_SECRET_ACCESS_KEY=
export AWS_ACCESS_KEY_ID=
export YOUR_AWS_REGION=us-west-1

source venv/bin/active
python3 app.py

