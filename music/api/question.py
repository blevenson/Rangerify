"""REST API for questions."""
import flask
import quiplash
import random


@quiplash.app.route('/api/v1/questions', methods=["GET"])
def get_questions():
    """Return list of questions
    """

    num_questions = 1

    # return set number of questions
    if flask.request.json and "num" in flask.request.json:
        num_questions = flask.request.json['num']

    context = {
        "url": "/api/v1/question",
        "questions": []
    }

    questions = []
    for i in range(num_questions):
        questions.append(random.choice(quiplash.QUESTIONS))

    context["questions"] = questions

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/playerquestions', methods=["GET"])
def get_player_questions():
    """Return list of player questions to answer
    """

    context = {
        "url": "/api/v1/playerquestions",
    }

    questions = []

    cur = quiplash.model.get_db().cursor()

    # Store question answers
    cur.execute(('SELECT * FROM questions WHERE name1 = \'%s\' OR name2 = \'%s\'')
                % (flask.session['username'], flask.session['username']))

    output = cur.fetchall()

    context["questions"] = output

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/assignquestions', methods=["GET"])
def assign_questions():
    """Return list of questions assigned to players
    """

    context = {
        "url": "/api/v1/assignquestions",
    }

    questions = []

    cur = quiplash.model.get_db().cursor()

    cur.execute(('DELETE FROM questions'))
    cur.execute(('DELETE FROM votes'))

    cur.execute(('SELECT * FROM players'))
    players = cur.fetchall()

    # Grab num of questions
    questions = []
    for i in range(len(players)):
        questions.append(random.choice(quiplash.QUESTIONS))

    print(questions)

    for i, q in enumerate(questions):
        n1 = players[(i - 1) % len(players)]['name']
        n2 = players[i]['name']

        ques = q.replace("'", "`").replace("\\", "").replace("\"", "")
        cur.execute(
            (('INSERT INTO questions (question, name1, name2) VALUES (\'%s\', \'%s\', \'%s\')') % (ques, n1, n2)))

    # Store question answers
    cur.execute(('SELECT * FROM questions'))
    output = cur.fetchall()

    context["assignments"] = output

    return flask.jsonify(**context)


@quiplash.app.route('/api/v1/resetquestions', methods=["GET"])
def reset_questions():
    """Reset assigned questions
    """

    context = {
        "url": "/api/v1/resetquestions",
    }

    cur = quiplash.model.get_db().cursor()

    cur.execute(('DELETE FROM questions'))

    return flask.jsonify(**context)
