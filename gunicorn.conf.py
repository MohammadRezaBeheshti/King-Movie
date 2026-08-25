import os
import multiprocessing

# Server socket
# ParsPack default port is 8000
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Worker processes
# Concurrency based on allocated CPU/RAM
workers = int(os.environ.get("WEB_CONCURRENCY", (multiprocessing.cpu_count() * 2) + 1 if multiprocessing.cpu_count() else 2))
threads = int(os.environ.get("PYTHON_MAX_THREADS", 2))
worker_class = "sync"
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")

# Process naming
proc_name = "king_movie_gunicorn"
