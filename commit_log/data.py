import json


class EntrySerializer:
    def serialize(self, entry: "Entry", encoding: str = "utf-8") -> bytes:

        return (
            json.dumps(
                dict(
                    lc=entry.logical_clock,
                    md=entry.metadata,
                    d=entry.data,
                )
            )
            + "\n"
        ).encode(encoding=encoding)

    def deserialize(self, entry: bytes | str, encoding: str = "utf-8"):
        if isinstance(entry, bytes):
            entry = entry.decode(encoding=encoding)
        entry_dict = json.loads(entry)
        return Entry(
            logical_clock=entry_dict["lc"],
            metadata=entry_dict.get("md"),
            data=entry_dict.get("d"),
        )


DEFAULT_SERIALIZER: EntrySerializer = EntrySerializer()
"""
The default serializer used when serializing an entry.
"""


class Entry:
    """Abstract class, handles the core functions of the entry
    class and holds information about an entry.
    """

    def __init__(
        self,
        data: bytes | str = None,
        metadata: dict = None,
        logical_clock: int = None,
    ) -> None:
        """Creates a new data entry

        Args:
            data (bytes | str | dict, optional): The log entry data. Defaults to None.
            metadata (dict, optional): The log metadata as dictionary.
                May include timestamp, type .. etc. JSON dictionary values only.
                Defaults to None.
            logical_clock (int, optional): The logical clock (index) of the data entry, within a log file.
                Denotes the order of the logs in the file.
                Defaults to None.
        """
        self.logical_clock = logical_clock
        self.metadata = metadata
        self.data = data
