"""REST API for players."""
import flask
import quiplash


@quiplash.app.route('/api/v1/players', methods=["GET"])
def get_players():
    """Return list of players.

    Example:
    {
        "url": "/api/v1/"
    }
    """

    context = {}

    # url
    context["url"] = flask.request.path

    # Database
    db = quiplash.model.get_db()

    cur = db.execute("SELECT * FROM players",)
    output = cur.fetchall()

    context["players"] = output

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/resetanswer', methods=["GET"])
def reset_answers():
    """Reset answers for all players.
    """

    context = {}

    # url
    context["url"] = flask.request.path

    # Database
    db = quiplash.model.get_db()

    cur = db.execute(('UPDATE players SET ans1 = \'\', ans2 = \'\' '))

    cur = db.execute("SELECT * FROM players",)
    output = cur.fetchall()

    context["players"] = output

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/resetplayers', methods=["GET"])
def reset_players():
    """Remove all players.
    """

    context = {}

    # url
    context["url"] = flask.request.path

    # Database
    db = quiplash.model.get_db()

    cur = db.execute(('DELETE FROM players'))

    cur = db.execute("SELECT * FROM players",)
    output = cur.fetchall()

    context["players"] = output

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/incrementScores', methods=["POST"])
def increment_scores():
    """Takes winners and increments the scores, 1 point per like
    """

    context = {}

    # url
    context["url"] = flask.request.path

    # Database
    db = quiplash.model.get_db()
    winners = flask.request.json['winners']

    for question in winners:
        point_delta_A = len(question['votesA'])
        point_delta_B = len(question['votesB'])

        point_delta = max(point_delta_A, point_delta_B)
        player_name = question[
            'winnerName'] if point_delta_A > point_delta_B else question['loserName']
        db.execute(('UPDATE players SET points = points + %s WHERE name = \'%s\'') %
                   (point_delta, player_name))

        point_delta = min(point_delta_A, point_delta_B)
        player_name = question[
            'loserName'] if point_delta_A > point_delta_B else question['winnerName']
        db.execute(('UPDATE players SET points = points + %s WHERE name = \'%s\'') %
                   (point_delta, player_name))

    return flask.jsonify(**context)
