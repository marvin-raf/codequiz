"""
Entry point to application
"""

from app import app
from config import config


def run_server():
    app.run(host="0.0.0.0", port=config["PORT"], threaded=True)


if __name__ == "__main__":
    run_server()
