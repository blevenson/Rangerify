"""
Quiplash server package initializer.

Brett Levenson <brettlev@umich.edu>
"""
import os
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (quiplash/config.py)
app.config.from_object('quiplash.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/0.12/config/
app.config.from_envvar('QUIPLASH_SETTINGS', silent=True)


def load_questions():
    """Load questions."""
    output = []
    with open(os.path.dirname(__file__) + '/questions.txt', 'r') as f_in:
        for line in f_in:
            output.append(line.strip())
    return output

QUESTIONS = load_questions()

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/0.12/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import quiplash.api  # noqa: E402  pylint: disable=wrong-import-position
import quiplash.views  # noqa: E402  pylint: disable=wrong-import-position
import quiplash.model  # noqa: E402  pylint: disable=wrong-import-position
