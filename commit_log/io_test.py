import os
from commit_log.consts import LOCAL_PATH
from commit_log.data import Entry
from commit_log.io import CommitLogWriter

TEST_PATH = os.path.join(LOCAL_PATH, "tests", "io")
os.makedirs(TEST_PATH, exist_ok=True)


def test_log_writer():
    writer = CommitLogWriter(
        os.path.join(TEST_PATH, "writer.log"),
    )

    writer.start_cache_loop_thread()

    for i in range(100):
        writer.write(Entry(str(i)))

    writer.flush()
    writer.stop_cache_loop()

    for i in range(100):
        writer.write(Entry(str(i)), False)


if __name__ == "__main__":
    test_log_writer()
