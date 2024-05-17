from datetime import datetime
import os
import time
import threading
import asyncio
import io
import logging
from typing import BinaryIO, List
from commit_log.data import Entry, EntrySerializer, DEFAULT_SERIALIZER
from commit_log.exceptions import CommitLogException
from commit_log.utils import thread_safe


def default_on_cache_error(ex: Exception):
    logging.error("Error when writing commit log cache", exc_info=ex)


class CommitLogWriter:
    def __init__(
        self,
        filepath: str,
        serializer: EntrySerializer = DEFAULT_SERIALIZER,
        cache_loop_interval_ms: float = 100,
        cache_internals_idle_time_ms: float = None,
        on_cache_error: default_on_cache_error = default_on_cache_error,
    ) -> None:
        assert filepath and os.path.exists(os.path.dirname(filepath)), ValueError(
            "filepath or filepath directory dose not exist"
        )

        self.filepath = filepath
        """The log file filepath"""
        self.serializer = serializer
        """The entry serializer"""
        self.cache_loop_interval_ms = cache_loop_interval_ms
        """The cache loop interval in milliseconds"""
        self.cache_internals_idle_time_ms = (
            cache_internals_idle_time_ms or cache_loop_interval_ms * 10
        )
        """The time, in milliseconds, for which to keep the log file open."""
        self.on_cache_error: callable = on_cache_error
        """A method (Exception) to be called when a cache error happens"""
        self.__entry_cache = []
        """Hols the log cache that would be flushed to disk at interval times"""

        self.__cache_running: bool = False
        self.__cache_thread: threading.Thread = None

        self.__logical_clock: int = 0
        self.__file_handler: BinaryIO = None
        self.__last_flushed: datetime = datetime.fromtimestamp(0)

    @property
    def cache_loop_running(self) -> bool:
        return self.__cache_running

    @property
    def logical_clock(self) -> int:
        return self.__logical_clock

    @thread_safe
    def __cache_idle_checks(self):
        # Cleaning up the file handler.
        if self.__file_handler and (
            self.__last_flushed is None
            or (datetime.now() - self.__last_flushed).total_seconds() * 1000
            > self.cache_internals_idle_time_ms
        ):
            self.__file_handler.flush()
            self.__file_handler.close()
            self.__file_handler = None

    @thread_safe
    def __cache_loop_iter(
        self,
        force=False,
        raise_exceptions: bool = False,
    ):
        if not force and not self.__cache_running:
            # Aborted
            return False
        # flush current entries
        if self.__entry_cache:
            try:
                self.__flush_entries(self.__entry_cache)
            except Exception as ex:
                if raise_exceptions:
                    raise ex
                default_on_cache_error(ex)
                return True

            self.__entry_cache = []
        else:
            # Do the cache idle checks.
            self.__cache_idle_checks()

        return True

    @thread_safe
    def __flush_entries(self, entries: List[Entry]):
        # Updating the logical clock entries
        buffer = io.BytesIO()

        for entry in entries:
            entry.logical_clock = self.logical_clock
            self.__logical_clock += 1
            self.write_entry(entry, buffer)

        # all entries are now written
        self.__last_flushed = datetime.now()
        handler = self.__file_handler
        if not handler:
            handler = open(
                self.filepath,
                mode="ab",
                buffering=10000000,
            )
            self.__file_handler = handler

        # writing to handler.
        handler.write(buffer.getbuffer())
        handler.flush()

    def write_entry(self, entry: Entry, buffer: io.BytesIO):
        buffer.write(self.serializer.serialize(entry))

    async def cache_loop(self):
        if self.__cache_running:
            raise CommitLogException("Cache loop has already been started")
        self.__cache_running = True

        while self.__cache_loop_iter():
            await asyncio.sleep(self.cache_loop_interval_ms)

        self.__cache_running = False

    def start_cache_loop_thread(self):
        if self.__cache_running:
            raise CommitLogException("Cache loop has already been started")

        def loop():
            while self.__cache_loop_iter():
                time.sleep(self.cache_loop_interval_ms)
            self.__cache_running = False

        tr = threading.Thread(target=loop)
        self.__cache_thread = tr
        self.__cache_running = True
        tr.start()
        return tr

    def stop_cache_loop(self):
        self.__cache_running = False
        if self.__cache_thread:
            # Wait for thread to complete
            self.__cache_thread.join(timeout=10)
            if self.__cache_thread.is_alive():
                raise CommitLogException("Failed to stop cache thread")
            self.__cache_thread = None

    def write(self, entry: Entry, use_cache: bool = True):
        self.__entry_cache.append(entry)
        if use_cache:
            assert self.cache_loop_running, ValueError(
                "Cannot use cache if the cash loop is not running",
            )
        else:
            self.__cache_loop_iter(True, True)

    def flush(self):
        self.__cache_loop_iter(True, True)
