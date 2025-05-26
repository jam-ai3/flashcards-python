# gunicorn.conf.py

# Server socket
bind = "0.0.0.0:8000"  # Binds to all IPs on port 8000

# Worker processes — Flask usually works well with 2-4 workers
workers = 2
worker_class = "sync"  # Default synchronous worker (good for most Flask apps)

# Performance tuning
threads = 2  # Each worker gets 2 threads
timeout = 30  # 30-second timeout for long requests
keepalive = 2  # Keep connections open for 2 seconds

# Logging
accesslog = "-"  # Log access to stdout
errorlog = "-"  # Log errors to stdout
loglevel = "info"  # Can be "debug", "info", "warning", "error", "critical"


# limit_request_field_size = 65536  # 64KB headers
# limit_request_line = 8190  # Request line length

# Process naming (optional)
proc_name = "flask_app"

# Daemon mode (optional — useful for systemd setups)
# daemon = True
