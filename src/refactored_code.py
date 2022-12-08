from typing import Dict, List, Optional
from abc import ABCMeta, abstractmethod
import json
import xml.etree.ElementTree as et


# added type hints
class Song:
    """Song"""
    def __init__(self, song_id: int, title: str, artist: str):
        self.song_id = song_id
        self.title = title
        self.artist = artist


# SongSerializer Interface
class ISongSerializer(metaclass=ABCMeta):
    """Interface for all dedicated SongSerializers"""

    @abstractmethod
    def serialize(self, song: Song):
        raise NotImplementedError


# Refactored Song Serializer
class SongSerializer():
    """
    Serializes a song to a defined format
    """
    def serialize(self, song, format):
        factory = SongSerializerFactory()
        serializer = factory.create_serializer(format)
        return serializer.serialize(song)


# dedicated Serializer to JSON Format
class JsonSongSerializer(ISongSerializer):
    """dedicated Serializer to JSON Format"""

    def serialize(self, song: Song):
        song_info = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return json.dumps(song_info)


# dedicated Serializer to XML Format
class XmlSongSerializer(ISongSerializer):
    """dedicated Serializer to XML Format"""

    def serialize(self, song: Song):
        song_info = et.Element('song', attrib={'id': str(song.song_id)})
        title = et.SubElement(song_info, 'title')
        title.text = song.title
        artist = et.SubElement(song_info, 'artist')
        artist.text = song.artist
        return et.tostring(song_info, encoding='unicode')


# Returns a dedicated Serializer that extends the ISongSerializer Interface
class SongSerializerFactory:
    """Factory to Creating the correct dedicated SongSerializer"""
    serializers = {
        "JSON": JsonSongSerializer,
        "XML": XmlSongSerializer,
        "DEFAULT": JsonSongSerializer,
    }

    def create_serializer(self, format):
        if format.upper() in self.serializers:
            return self.serializers[format.upper()]()
        return self.serializers["DEFAULT"]()


# Abstract the logic from userinput
class InputHandler:
    """Responsible for handling the user input type safety"""

    @staticmethod
    def int_input(message: str = None, header: str = None) -> int:
        while True:
            try:
                if header:
                    print(header)
                inp = int(input(f"{message}: "))
                return inp
            except ValueError:
                print("invalid input. Please provide a number")

    @staticmethod
    def str_input(message: str = None, header: str = None) -> str:
        if header:
            print(header)
        inp = (input(f"{message}: "))
        return inp


# User Interaction Layer
class View:
    """Responsible for all interactions with the user"""

    def send_message(self, message):
        print(message)

    def menu(self):
        print("=================================================================================================")
        choice = InputHandler.str_input(
            header="ACTIONS: [0] Exit  [1] upload Song  [2] Select Song  [3] Serialize Song  [4] list all songs",
            message="enter")

        if choice not in {"0", "1", "2", "3", "4"}:
            print("Invalid Choice...")
            self.menu()
        return choice

    def upload_song(self):
        print("define Song you want to upload")
        title = InputHandler.str_input(message="title")
        artist = InputHandler.str_input(message="artist")
        return title, artist

    def select_song_by_id(self):
        selected_id = InputHandler.int_input(message="id", header="Please Select a song by id")
        return selected_id

    def select_serializing_format(self):
        print("please Select a Format for serializing")
        print("[1] JSON  [2] XML  [3]  STRING")
        format_choice = InputHandler.str_input(message="format: ",
                                               header="please Select a Format for serializing" + "\n" +
                                                      "[JSON]  [XML]  [STRING]"
                                               )
        return format_choice

    def show_all_songs(self, songs):
        for song in songs:
            print(song)


# Data Layer
class Database:
    """Responsible for storing and interacting with the data of the program"""
    songs: List[Song] = list()

    def insert(self, title: str, artist: str) -> bool:
        for song in self.songs:
            if song.title == title:
                return False

        new_song_id = 1
        for song in self.songs:
            if song.song_id >= new_song_id:
                new_song_id = song.song_id + 1
        self.songs.append(Song(new_song_id, title, artist))
        return True

    def get_song(self, song_id: int) -> Song or None:
        for song in self.songs:
            if song.song_id == song_id:
                return song
        return None

    def get_songs(self):
        return self.songs


# Use Cases
def _uc_post_new_song(db: Database, view: View, serializer: SongSerializer):
    """Responsible for running the use case of posting a new song to database"""
    new_title, new_artist = view.upload_song()
    db.insert(new_title, new_artist)
    return True


def _uc_select_song(db: Database, view: View, serializer: SongSerializer):
    """Responsible for running the use case of viewing a selected song"""
    song_id = view.select_song_by_id()
    song = db.get_song(song_id)
    if song:
        view.send_message(serializer.serialize(song, ""))
    else:
        view.send_message(f"Sorry No song for id: {song_id}")
    return True


def _uc_serialize_song(db: Database, view: View, serializer: SongSerializer):
    """Responsible for running the use case of serializing a selected song in a selected format"""
    song_id = view.select_song_by_id()
    song = db.get_song(song_id)
    if song:
        _format = view.select_serializing_format()
        view.send_message(serializer.serialize(song, _format))
    return True


def _uc_list_all_songs(db: Database, view: View, serializer: SongSerializer):
    """Responsible for Running the use case of viewing all uploaded songs"""
    songs = list()
    for song in db.get_songs():
        songs.append(serializer.serialize(song, ""))
    view.show_all_songs(songs)
    return True


def _uc_exit_program(db: Database, view: View, serializer: SongSerializer):
    """Responsible for Running the use case of exiting the program"""
    print("Goodbye")
    return False


# Rules engine to take supply a controller for each use case
class ChoiceEngine:
    """
    takes the input in menu and then executes based on the choice
    """
    _options = {
        "0": _uc_exit_program,
        "1": _uc_post_new_song,
        "2": _uc_select_song,
        "3": _uc_serialize_song,
        "4": _uc_list_all_songs
    }

    def execute_choice(self, choice, db, view, serializer):
        default = view.menu
        if choice in self._options:
            return self._options[choice](db, view, serializer)
        return default()


# app is reduced to basic setup and run loop
def app():
    # Setup basic components of this app
    db = Database()
    view = View()
    serializer = SongSerializer()
    choice_engine = ChoiceEngine()
    run = True
    while run:
        # the user selects what he wants to do in the menu
        choice = view.menu()
        # the users choice is now handed to the choice engine to give the user the chosen use case
        run = choice_engine.execute_choice(choice, db, view, serializer)


if __name__ == '__main__':
    app()
