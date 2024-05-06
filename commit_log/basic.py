import os
import time
from datetime import datetime
from utils.constants import REPO_LOCAL_PATH
from zthreading.tasks import Task
from utils.logs import create_logger

logger = create_logger("basic")

global logical_clock
logical_clock = 0
byte_data = ("abcd" * 100).encode("utf-8")
fpath = os.path.join(REPO_LOCAL_PATH, "test_writer.dump")
sep = " ".encode("utf-8")
lnend = "\n".encode("utf-8")


def test_writer():
    global logical_clock

    with open(
        fpath,
        mode="ab",
        buffering=10000000,
    ) as src:
        # 2 m actions per second. This would be much more then
        # the number of requests available.
        while True:
            logical_clock += 1
            src.write(byte_data)
            src.write(lnend)
            if logical_clock % 1e5 == 0:
                logger.info(logical_clock)
                src.flush()
            if logical_clock == 1e8:
                logger.info("Reached end")


if __name__ == "__main__":
    if os.path.exists(fpath):
        os.remove(fpath)

    started = datetime.now()
    tasks = [
        Task(test_writer).start(),
    ]

    time.sleep(10)
    ended = datetime.now()

    delta = ended - started
    logger.info(
        f"timed out @ {logical_clock} in {delta.total_seconds()}"
        + f" with {logical_clock/delta.total_seconds()} a/s"
    )
    os.kill(os.getpid(), 9)
    exit(0)
