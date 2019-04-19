"""REST API for queue."""
import flask
import music
import heapq


@music.app.route('/api/v1/queue', methods=["GET"])
def get_queue():
    """Return queue
    Example:
    {
        "url": "/api/v1/queue"
        "songs": [(priority, {song})]
    }
    """

    context = {
        "url": "/api/v1/queue",
        "queue": heapq.nlargest(len(music.SONG_QUEUE), music.SONG_QUEUE),
    }

    return flask.jsonify(**context)


@music.app.route('/api/v1/addsong', methods=["POST"])
def add_song():
    """Add song to queue
    Example:
    {
        "url": "/api/v1/addsong"
    }
    """

    heapq.heappush(music.SONG_QUEUE, [1, flask.request.json["song_title"]])

    context = {
        "url": "/api/v1/addsong",
    }

    return flask.jsonify(**context)


@music.app.route('/api/v1/updatepriority', methods=["POST"])
def update_priority():
    """Update priority of song
    Example:
    {
        "url": "/api/v1/updatepriority"
    }
    """

    song_title = flask.request.json["song_title"]
    weight = flask.request.json["weight"]

    # Find index of song
    for song in music.SONG_QUEUE:
        if song[1] == song_title:
            song[0] += weight

    heapq.heapify(music.SONG_QUEUE)

    context = {
        "url": "/api/v1/updatepriority",
    }

    return flask.jsonify(**context)
