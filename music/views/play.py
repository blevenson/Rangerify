"""
Quiplash play view.

URLs include:
/
"""
import flask
import quiplash


@quiplash.app.route('/play', methods=['GET'])
def show_play():
    """Display /play route."""
    context = {
    }

    # Check is user joined game
    if 'username' not in flask.session:
        return flask.redirect('/join')

    return flask.render_template("play.html", **context)


@quiplash.app.route('/join', methods=['GET', 'POST'])
def show_join():
    """Display /join route."""
    context = {
    }

    connection = quiplash.model.get_db()

    # Check is user already joined game
    if 'username' in flask.session and quiplash.model.check_exists(connection, flask.session['username']):
        return flask.redirect('/play')

    if flask.request.method == 'POST':
        # Get Username
        username_input = flask.request.form['username']

        cursor = connection.cursor()

        cursor.execute('INSERT INTO players(name, points, ans1, ans2) VALUES(\'' +
                       username_input + '\', 0, \'\',\'\')',)

        flask.session['username'] = username_input

        return flask.redirect('/play')

    return flask.render_template("join.html", **context)


@quiplash.app.route('/vote', methods=['GET', 'POST'])
def show_vote():
    """Display /vote route."""
    context = {}

    connection = quiplash.model.get_db()

    # Check is user already joined game
    if 'username' not in flask.session:
        return flask.redirect('/')

    if flask.request.method == 'POST':

        for question, vote in flask.request.form.items():
            if question == 'submit':
                continue

            cursor = connection.cursor()

            cursor.execute(
                ('INSERT INTO votes(name, questionid, playerid) VALUES(\'%s\', %s, %s)') % (flask.session['username'], question, vote),)

        return flask.redirect('/')

    cursor = connection.cursor()

    # Check if all players have answered
    context['waitingToVote'] = False
    for player in connection.cursor().execute("SELECT * FROM players"):
        if player['ans1'] == "" and player['ans2'] == "":
            context['waitingToVote'] = True

    questions = []

    # Used to check if use ans1 or ans2
    playersAnswered = {}

    for row in connection.cursor().execute("SELECT * FROM questions"):
        newQuestion = {}

        cursor.execute('SELECT * FROM players WHERE name = ?',
                       (row['name1'],))
        player1 = cursor.fetchone()
        cursor.execute('SELECT * FROM players WHERE name = ?',
                       (row['name2'],))
        player2 = cursor.fetchone()

        newQuestion["question"] = row['question']
        newQuestion['questionId'] = row['questionid']
        newQuestion["playerId1"] = player1['playerid']
        newQuestion["playerId2"] = player2['playerid']

        newQuestion["ans1"] = player1['ans1'] if row[
            'name1'] not in playersAnswered else player1['ans2']
        newQuestion["ans2"] = player2['ans1'] if row[
            'name2'] not in playersAnswered else player2['ans2']

        playersAnswered[row['name1']] = True
        playersAnswered[row['name2']] = True

        # Can't vote on own answer
        if row['name1'] != flask.session['username'] and row['name2'] != flask.session['username']:
            questions.append(newQuestion)

    context['questions'] = questions

    return flask.render_template("vote.html", **context)
