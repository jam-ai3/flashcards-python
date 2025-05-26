#!/bin/bash
# reload_gunicorn.sh - Send HUP signal to Gunicorn master process

# The PID of your Gunicorn master process
MASTER_PID=154032

# Send the HUP signal
kill -HUP $MASTER_PID

# Output confirmation message
echo "HUP signal sent to Gunicorn master process (PID: $MASTER_PID)"
echo "Application is now gracefully reloading with zero downtime."
