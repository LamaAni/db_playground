import os

__DEFAULT_REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def __get_path(env: str, src: str):
    if not os.path.isabs(src):
        src = os.path.abspath(os.path.join(__DEFAULT_REPO_PATH, src))
    return os.environ.get(env, src)


REPO_PATH = __get_path("REPO_PATH", ".")
REPO_LOCAL_PATH = __get_path("REPO_LOCAL_PATH", "./.local")

if __name__ == "__main__":
    print(REPO_PATH, REPO_LOCAL_PATH)
