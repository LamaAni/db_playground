import os
import time
import random
from utils.constants import REPO_LOCAL_PATH
from zthreading.tasks import Task


def test_writer():
    logical_clock = 0
    sep = " ".encode("utf-8")
    lnend = "\n".encode("utf-8")
    with open(
        os.path.join(REPO_LOCAL_PATH, "test_writer.dump"),
        mode="ab",
        buffering=10000,
    ) as src:
        while True:
            logical_clock += 1
            src.write(bytes(logical_clock))
            src.write(sep)
            src.write(str(random.random()).encode(encoding="utf-8"))
            src.write(lnend)
            if logical_clock == 1e10:
                break


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
