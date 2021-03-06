"""REST API for services."""
import flask
import music


@music.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Return list of services.

    Example:
    {
        "url": "/api/v1/"
    }
    """

    context = {
        "url": "/api/v1/",
        "queue": "/api/v1/queue",
    }

    return flask.jsonify(**context)
