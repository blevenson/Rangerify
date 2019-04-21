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

    context = {
        "url": "/api/v1/addsong",
    }

    # Check if song already in queue
    if flask.request.json["song_title"].lower() in (song[1].lower() for song in music.SONG_QUEUE):
        # song already added
        context["error"] = "Song already in queue"
        return flask.jsonify(**context)

    heapq.heappush(music.SONG_QUEUE, [0, flask.request.json["song_title"]])

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


@music.app.route('/api/v1/deletesong', methods=["POST"])
def delete_song():
    """Delete song from queue
    Example:
    {
        "url": "/api/v1/deletesong"
    }
    """

    context = {
        "url": "/api/v1/deletesong",
    }

    song_title = flask.request.json["song_title"]

    # Remove song
    for song in music.SONG_QUEUE:
        if song[1] == song_title:
            music.SONG_QUEUE.remove(song)
            break

    heapq.heapify(music.SONG_QUEUE)

    return flask.jsonify(**context)
