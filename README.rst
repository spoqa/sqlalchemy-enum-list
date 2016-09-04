SQAlchemy Enum List
~~~~~~~~~~~~~~~~~~~

Store list of enum member as unicode string. it works list of python on
python-side & stored unicode text in database. To store scalar values like
integer, float read about ScalarListType_ in SQLAlchemy-Utils_

.. _ScalarListType: https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.scalar_list
.. _SQLAlchemy-Utils: https://github.com/kvesteri/sqlalchemy-utils


Getting started
===============

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
