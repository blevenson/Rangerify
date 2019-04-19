"""REST API for votes."""
import flask
import quiplash


@quiplash.app.route('/api/v1/votes', methods=["GET"])
def get_votes():
    """Return list of votes.

    Example:
    {
        "votes": [] 
        "url": "/api/v1/votes"
    }
    """

    context = {}

    # url
    context["url"] = flask.request.path

    # Database
    db = quiplash.model.get_db()

    cur = db.execute("SELECT * FROM votes",)
    output = cur.fetchall()

    context["votes"] = output

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/votedPlayers', methods=["GET"])
def get_voted_players():
    """Return list of player names who have voted.

    Example:
    {
        "voters": ["name1", "username2", "player3"],
        "url": "/api/v1/votes"
    }
    """

    context = {}

    # Init context
    context["url"] = flask.request.path

    # Database
    db = quiplash.model.get_db()

    cur = db.execute("SELECT * FROM votes",)
    votes = cur.fetchall()

    players = {}
    for vote in votes:
        players[vote['name']] = True

    context["voters"] = list(players.keys())

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/resetvotes', methods=["GET"])
def reset_votes():
    """Reset votes
    """

    context = {
        "url": "/api/v1/resetvotes",
    }

    cur = quiplash.model.get_db().cursor()

    cur.execute(('DELETE FROM votes'))

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/winners', methods=["GET"])
def get_winners():
    """Returns question with num votes.

    Example:
    {
        "winners": [{
            "questionid": 1,
            "question": "Why did the chicken cross the road?",
            "ansA": "something funny",
            "ansB": "something hilarious",
            "votesA": [player2],
            "votesB": [player1, player3],
            "winnerName": ralph,
            "loserName": brett
        }] 
        "url": "/api/v1/votes"
    }
    """

    context = {}

    # url
    context["url"] = flask.request.path
    context['winners'] = []

    # Database
    db = quiplash.model.get_db()

    # Grab all the votes
    cur = db.execute("SELECT * FROM votes",)
    votes = cur.fetchall()

    # Group votes by question id
    questionsToVotes = {}
    for vote in votes:
        if vote['questionid'] not in questionsToVotes:
            questionsToVotes[vote['questionid']] = []

        questionsToVotes[vote['questionid']].append(vote)

    playersAnswered = {}
    for row in db.cursor().execute("SELECT * FROM questions"):
        newQuestion = {}
        newQuestion['question'] = row['question']
        newQuestion['questionid'] = row['questionid']

        # Grab all the votes
        votesForQ = []
        if row['questionid'] in questionsToVotes:
            votesForQ = questionsToVotes[row['questionid']]

        # Grab players who answered these questions
        cur = db.execute(
            ("SELECT * FROM players WHERE name = \'%s\'") % (row['name1']),)
        playerA = cur.fetchone()
        cur = db.execute(
            ("SELECT * FROM players WHERE name = \'%s\'") % (row['name2']),)
        playerB = cur.fetchone()

        # Get votes for each player
        newQuestion['votesA'] = []
        newQuestion['votesB'] = []
        for vote in votesForQ:
            if playerA['playerid'] == vote['playerid']:
                newQuestion['votesA'].append(vote['name'])
            else:
                newQuestion['votesB'].append(vote['name'])

        # Determine winners
        if len(newQuestion['votesA']) > len(newQuestion['votesB']):
            newQuestion['winnerName'] = playerA['name']
            newQuestion['loserName'] = playerB['name']
        else:
            newQuestion['winnerName'] = playerB['name']
            newQuestion['loserName'] = playerA['name']

        # Grab player's answer
        newQuestion["ansA"] = playerA['ans1'] if row[
            'name1'] not in playersAnswered else playerA['ans2']
        newQuestion["ansB"] = playerB['ans1'] if row[
            'name2'] not in playersAnswered else playerB['ans2']

        playersAnswered[row['name1']] = True
        playersAnswered[row['name2']] = True

        context['winners'].append(newQuestion)

    return flask.jsonify(**context)
