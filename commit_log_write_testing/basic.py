import os
import time
import random
from utils.constants import REPO_LOCAL_PATH
from zthreading.tasks import Task


def test_writer():
    with open(
        os.path.join(REPO_LOCAL_PATH, "test_writer.dump"), "w", encoding="utf-8"
    ) as src:
        while True:
            src.write(str(random.random()))
            src.write("\n")


def test_halter():
    time.sleep(2)
    exit(0)


if __name__ == "__main__":

    tasks = [
        Task(test_writer).start(),
        Task(test_halter).start(),
    ]

    for t in tasks:
        t.join()
