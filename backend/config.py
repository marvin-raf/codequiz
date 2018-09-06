import os

config = {}

config["PORT"] = 5000
config["UPLOAD_FOLDER"] = "uploads/excel_docs"
config["HOSTNAME"] = "localhost"
config["USER"] = "root"

DB_PASSWORD = os.environ.get("DB_PASSWORD")

config["DB_PASSWORD"] = DB_PASSWORD if DB_PASSWORD else ""
config["DB_NAME"] = "quiz_server"