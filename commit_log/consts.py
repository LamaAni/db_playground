import os

REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOCAL_PATH = os.environ.get("LOCAL_PATH", os.path.join(REPO_PATH, ".local"))
