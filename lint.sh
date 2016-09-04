#!/bin/bash

flake8 .
# It could be failed if version of python lower than 3.4.
# because enum is not standard package on it.
import-order --only-file sqlalchemy_enum_list.py test.py
