"""
Quiplash server index (main) view.

URLs include:
/
"""
import flask
import quiplash
import socket


@quiplash.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    context = {
    }

    # Show server IP so know what to connect to
    context['IP'] = socket.gethostbyname(socket.gethostname()) + ":8000/"

    return flask.render_template("index.html", **context)
