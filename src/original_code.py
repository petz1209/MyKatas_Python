from abc import ABCMeta, abstractmethod
import json
import xml.etree.ElementTree as et


class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


class SongSerializer:
    def serialize(self, song, format):
        if format == 'JSON':
            song_info = {
                'id': song.song_id,
                'title': song.title,
                'artist': song.artist
            }
            return json.dumps(song_info)
        elif format == 'XML':
            song_info = et.Element('song', attrib={'id': song.song_id})
            title = et.SubElement(song_info, 'title')
            title.text = song.title
            artist = et.SubElement(song_info, 'artist')
            artist.text = song.artist
            return et.tostring(song_info, encoding='unicode')
        else:
            raise ValueError(format)


def app():
    run = True
    songs = list()
    while run:
        print("OPTIONS")
        print("[0] Exit  [1] upload Song  [2] Select Song  [3] Serialize Song  [4] list all songs")
        choice = input("enter: ")
        if choice not in {"0", "1", "2", "3", "4"}:
            print("Invalid Choice...")
        else:
            if choice == "0":
                print("Goodbye")
                run = False

            elif choice == "1":
                print("define Song you want to upload")
                new_title = input("title: ")
                new_artist = input("artist: ")
                # Check if this song exists in database:
                song_is_new = True
                for song in songs:
                    if song.title == new_title:
                        song_is_new = False
                        print("Song allready exists")
                        break
                if song_is_new:
                    new_song_id = 1
                    for song in songs:
                        if song.song_id >= new_song_id:
                            new_song_id = song.song_id + 1
                    songs.append(Song(new_song_id, new_title, new_artist))

                # Calculate id
            elif choice == "2":
                print("Please Select a song by id")
                while True:
                    try:
                        selected_id = int(input("id: "))
                        break
                    except:
                        print("invalid input, id must be a number")
                song_missing = True
                for song in songs:
                    if song.song_id == selected_id:
                        print("----------------------")
                        print(song.title)
                        print("----------------------")
                        song_missing = False
                        break
                if song_missing:
                    print(f"Sorry No song for id: {selected_id}")
            elif choice == "3":
                print("Please Select a song by id")
                while True:
                    try:
                        selected_id = int(input("id: "))
                        break
                    except:
                        print("invalid input, id must be a number")
                chosen_song = None
                for song in songs:
                    if song.song_id == selected_id:
                        chosen_song = song
                        break

                if not chosen_song:
                    print(f"Sorry No song for id: {selected_id}")
                if chosen_song:
                    print("please Select a Format for serializing")
                    print("[1] JSON  [2] XML  [3]  STRING")
                    format_choice = input("format: ")
                    if format_choice == "1":
                        _format = "JSON"
                    elif format_choice == "2":
                        _format = "XML"
                    elif format_choice == "3":
                        _format = "STRING"
                    else:
                        print("Unrecognised Format... using default (JSON).")
                        _format = "JSON"
                    serializer = SongSerializer()
                    serialized = serializer.serialize(chosen_song, _format)
                    print(serialized)
                    print("===============================================================")

            elif choice == "4":
                serializer = SongSerializer()
                for song in songs:
                    print("----------------------")
                    print(serializer.serialize(song, ""))
                print("----------------------")


if __name__ == '__main__':

    app()
