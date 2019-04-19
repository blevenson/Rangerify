"""
Quiplash server host server view.

URLs include:
/
"""
import flask
import quiplash


@quiplash.app.route('/host', methods=['GET'])
def show_host():
    """Display /host route."""
    context = {
    }

    return flask.render_template("host.html", **context)
