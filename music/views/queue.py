"""
Music server show queue

URLs include:
/
"""
import flask
import music


@music.app.route('/queue', methods=['GET'])
def show_queue():
    """Display /queue route."""
    context = {
    }

    return flask.render_template("queue.html", **context)
