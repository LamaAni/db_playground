# Note that we are not using any data models
# to generate the data entries. This is since
# we want the fastest implementation of the serialization
# data model.
# Each entry in the class can use a serializer/deserializer
# that is configurable.
import json


class EntrySerializer:
    def serialize(entry: "Entry", encoding: str = "utf-8") -> bytes:
        return json.dumps(
            dict(
                lc=entry.logical_clock,
                md=entry.metadata,
                d=entry.data,
            )
        ).encode(encoding=encoding)

    def deserialize(entry: bytes | str, encoding: str = "utf-8"):
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
        logical_clock: int = None,
        metadata: dict = None,
        data: bytes | str = None,
    ) -> None:
        """Creates a new data entry

        Args:
            logical_clock (int, optional): The logical clock (index) of the data entry, within a log file.
                Denotes the order of the logs in the file.
                Defaults to None.
            metadata (dict, optional): The log metadata as dictionary.
                May include timestamp, type .. etc. JSON dictionary values only.
                Defaults to None.
            data (bytes | str | dict, optional): The log entry data. Defaults to None.
        """
        self.logical_clock = logical_clock
        self.metadata = metadata
        self.data = data
