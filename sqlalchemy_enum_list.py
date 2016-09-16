import enum

from six import text_type
from sqlalchemy.types import TypeDecorator, UnicodeText

__all__ = 'EnumListType', 'EnumListTypeException', 'EnumSetType', '__version__'
__version__ = '0.1.0'


class EnumListTypeException(ValueError):
    pass


class EnumListType(TypeDecorator):
    """List of :class:`enum.Enum`.

    .. code-block:: python

       import enum

       from sqlalchemy.schma import Column
       from sqlalchemy_enum_list import EnumListType

       class Genre(enum.Enum):

           pop = 1

           soul = 2

           jazz = 3


       class Song(Base):

           genre = Column(EnumListType(Genre, int))

       song = Song(genre=[Genre.soul, Genre.jazz])

    """

    impl = UnicodeText()

    def __init__(self, enum_cls, coerce_func, separator=u','):
        if not issubclass(enum_cls, enum.Enum):
            raise EnumListTypeException(
                '`enum_cls` MUST be subclass of `enum.Enum`. '
                'not {!r}.'.format(enum_cls)
            )
        if any(separator in text_type(item.value) for item in enum_cls):
            raise EnumListTypeException(
                "member of enum can't contain string '{}' (its being used as "
                "separator. If you wish for enum values to contain "
                "these strings, use a different separator string.)".format(
                    separator
                )
            )
        try:
            [coerce_func(item.value) for item in enum_cls]
        except (TypeError, ValueError):
            raise EnumListTypeException('member of enum cannot be coereced.')
        self.enum_cls = enum_cls
        self.separator = text_type(separator)
        self.coerce_func = coerce_func

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not all(item in self.enum_cls for item in value):
                raise EnumListTypeException(
                    "List values have to be member of {!r}.".format(
                        self.enum_cls
                    )
                )
            return self.separator.join(
                [text_type(item.value) for item in value]
            )

    def process_result_value(self, value, dialect):
        if value is not None:
            if value == u'':
                return []
            return [
                self.enum_cls(self.coerce_func(v))
                for v in value.split(self.separator)
            ]


class EnumSetType(EnumListType):

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not all(item in self.enum_cls for item in value):
                raise EnumListTypeException(
                    "Set values have to be member of {!r}.".format(
                        self.enum_cls
                    )
                )
            return self.separator.join(
                {text_type(item.value) for item in value}
            )

    def process_result_value(self, value, dialect):
        if value is not None:
            return set(super().process_result_value(value, dialect))
