# src/dummyfinance/config.py
import os
import sys

# cross-platform, Linux/macOS/Windows
if sys.platform == "win32":
    data_home = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
elif sys.platform == "darwin":
    data_home = os.path.expanduser("~/Library/Application Support")
else:
    data_home = os.environ.get(
        "XDG_DATA_HOME", os.path.join(os.path.expanduser("~"), ".local", "share")
    )

APP_NAME = "dummyfinance"

data_path = os.path.join(data_home, APP_NAME)
os.makedirs(data_path, exist_ok=True)

DATA_FILE = os.path.join(data_path, "data.json")

# Create the file if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        import json

        json.dump({"income": [], "expenses": []}, f)
