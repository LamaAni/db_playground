# Note that we are not using any data models
# to generate the data entries. This is since
# we want the fastest implementation of the serialization
# data model.
# Each entry in the class can use a serializer/deserializer
# that is configurable.


class EntrySerializer:

    pass


class Entry:
    """Abstract class, handles the core functions of the entry
    class and holds information about an entry.
    """

    DEFAULT_SERIALIZER: EntrySerializer = EntrySerializer()
    """
    The default serializer used when serializing an entry.
    This would be replaced with
    """

    def __init__(self, serializer: EntrySerializer = None) -> None:
        pass
