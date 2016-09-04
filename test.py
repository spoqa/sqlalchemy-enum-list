import enum
import os

try:
    from psycopg2ct.compat import register
except ImportError:
    pass
else:
    register()
from pytest import fixture, mark, raises, yield_fixture
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer
from sqlalchemy_enum_list import EnumListType, EnumListTypeException


Base = declarative_base()
Session = sessionmaker()


try:
    database_urls = os.environ['TEST_DATABASE_URLS'].split()
except KeyError:
    database_urls = []


@fixture(scope='function', params=['sqlite://'] + database_urls)
def fx_engine(request):
    url = request.param
    engine = create_engine(url, poolclass=NullPool)
    request.addfinalizer(engine.dispose)
    return engine


@yield_fixture
def fx_connection(fx_engine):
    connection = fx_engine.connect()
    try:
        transaction = connection.begin()
        try:
            metadata = Base.metadata
            metadata.create_all(bind=connection)
            yield connection
        finally:
            transaction.rollback()
    finally:
        connection.close()


@yield_fixture
def fx_session(fx_connection):
    session = Session(bind=fx_connection)
    try:
        yield session
    finally:
        session.close()


class IntEnum(enum.Enum):

    a = 1

    b = 2


class StrEnum(enum.Enum):

    a = 'a'

    b = 'b'


class EnumTest(Base):

    id = Column(Integer, primary_key=True)

    int_column = Column(EnumListType(IntEnum, int))

    str_column = Column(EnumListType(StrEnum, str))

    __tablename__ = 'enum_test'


@mark.parametrize(
    'column_name, enum_cls',
    [
        ('int_column', IntEnum),
        ('str_column', StrEnum),
    ]
)
def test_enum_list(fx_session, column_name, enum_cls):
    entity = EnumTest(**{column_name: list(enum_cls)})
    fx_session.add(entity)
    fx_session.flush()
    assert getattr(entity, column_name) == list(enum_cls)


def test_enum_list_init_exception(fx_session):
    with raises(EnumListTypeException):
        EnumListType(StrEnum, float, 'a')
    with raises(EnumListTypeException):
        EnumListType(StrEnum, float)
    with raises(EnumListTypeException):
        EnumListType(int, str)


def test_enum_list_bind_exception(fx_session):
    fx_session.add(EnumTest(str_column='a'))
    with raises(StatementError):
        fx_session.flush()
