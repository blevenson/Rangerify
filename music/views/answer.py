"""
Quiplash answer view.

URLs include:
/
"""
import flask
import quiplash


@quiplash.app.route('/answer', methods=['GET', 'POST'])
def show_answer_form():
    """Display /answer route."""
    context = {
    }

    # Check is user not joined game
    if 'username' not in flask.session:
        return flask.redirect('/')

    if flask.request.method == 'POST':
        # Get Username and password
        ans1 = flask.request.form['ans1']
        ans2 = flask.request.form['ans2']

        connection = quiplash.model.get_db()

        # Store question answers
        connection.execute(('UPDATE players SET ans1 = \'%s\', ans2 = \'%s\' WHERE name = \'%s\'')
                           % (ans1, ans2, flask.session['username']))

        return flask.redirect('/vote')

    cur = quiplash.model.get_db().cursor()

    cur.execute(
        ('SELECT * FROM questions WHERE name1 = \'%s\' or name2 = \'%s\'') % (flask.session['username'], flask.session['username']))
    questions = cur.fetchall()

    # Store question answers
    cur.execute(('SELECT * FROM questions'))
    output = cur.fetchall()

    context['q1'] = questions[0]['question']
    context['q2'] = questions[1]['question']

    return flask.render_template("answer.html", **context)
