#!/bin/sh
# List of source files containing translatable strings.
xgettext -L python -o billreminder.pot ../data/*.desktop ../src/*.py ../src/daemon/*.py ../src/db/*.py ../src/gui/*.py ../src/gui/widgets/*.py ../src/lib/*.py
