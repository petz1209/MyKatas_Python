import json
import pytest
from refactored_code import Song
from refactored_code import SongSerializer


def test_song_creation():
    song = Song(1, "country roads", "john denver")
    assert isinstance(song, Song)


def test_serialize_to_json():

    song = Song(1, "country roads", "john denver")
    serializer = SongSerializer()
    json_song = serializer.serialize(song, "JSON")
    assert json_song == json.dumps({"id": song.song_id, "title": song.title, "artist": song.artist})


def test_serialize_to_xml():
    song = Song(1, "country roads", "john denver")
    serializer = SongSerializer()
    xml_song = serializer.serialize(song, "XML")
    assert xml_song == '<song id="1"><title>country roads</title><artist>john denver</artist></song>'


def test_serialize_to_json2():
    song = Song(1, "country roads", "john denver")
    serializer = SongSerializer()
    json_song = serializer.serialize(song, "json")
    assert json_song == json.dumps({"id": song.song_id, "title": song.title, "artist": song.artist})


def test_serialize_to_default():
    song = Song(1, "country roads", "john denver")
    serializer = SongSerializer()
    json_song = serializer.serialize(song, "")
    assert json_song == json.dumps({"id": song.song_id, "title": song.title, "artist": song.artist})
