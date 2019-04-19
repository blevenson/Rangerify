"""Quiplash server model (database) API."""
import sqlite3
import flask
import quiplash


def dict_factory(cursor, row):
    """Create a dictionary Factory."""
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            quiplash.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


def check_exists(connection, name):
    """Check if name exists."""
    # Check if name exists
    check_if_exists = connection.execute(
        "SELECT 1 FROM players WHERE name = ? ",
        (name,)
    )
    exists = check_if_exists.fetchone()

    return (exists is not None)


@quiplash.app.teardown_appcontext
def close_db(error):
    # pylint: disable=unused-argument
    """Close the database at the end of a request."""
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()
