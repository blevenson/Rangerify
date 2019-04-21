"""Music Server REST API."""

from music.api.index import get_services
from music.api.queue import get_queue, add_song, update_priority, delete_song
