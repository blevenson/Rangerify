"""REST API for queue."""
import flask
import music


@music.app.route('/api/v1/queue', methods=["GET", "POST"])
def get_queue():
    """Return queue or add song to queue.

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
