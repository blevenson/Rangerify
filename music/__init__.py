"""
Music server package initializer.

Brett Levenson <brettlev@umich.edu>
"""
import os
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (msusic/config.py)
app.config.from_object('music.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/0.12/config/
app.config.from_envvar('MUSIC_SETTINGS', silent=True)


# Stores [priority, {song}]
SONG_QUEUE = []

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/0.12/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import music.api  # noqa: E402  pylint: disable=wrong-import-position
import music.views  # noqa: E402  pylint: disable=wrong-import-position
