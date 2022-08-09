import os
import re
import sys
from pprint import pprint

import pymediainfo


def is_japanese_in_string(text):
    # https://gist.github.com/ryanmcgrath/982242
    regex = re.compile("[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B")
    # Car regex.match ne fonctionne pas si on n'a pas des chractères japonais dès le début
    return regex.search(text) if text else None

class Song():

    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []

    def check_rules(self):
        media_info = pymediainfo.MediaInfo.parse(self.filepath)
        for track in media_info.tracks:
            if track.track_type == "General":
                self.check_artist(track)
                self.check_multiple_artists(track)
                self.check_album(track)
                self.check_track(track)
                self.check_date(track)
                self.check_cover(track)
                self.check_catalog_number(track)

                # TODO: Numéro de piste existe ?

                #self.check_for_japanese_text(track)

            #if track.track_type == "Audio":
                #self.check_bitrate(track)

    # TODO: Artiste de l'album
    def check_artist(self, track):
        if not track.album:
            self.errors.append("👉 🎤 Nom d'artiste manquant")

    def check_multiple_artists(self, track):
        # Si le nom de l'artiste n'est pas en majuscule
        if track.performer:
            if "&" in str(track.performer) or ";" in str(track.performer):
                self.errors.append("👉 Multiples artistes: {}".format(track.performer))

            else:
                splitted = track.performer.split(" ")

                if len(splitted) >= 2:
                    name = splitted[-1]
                    if name.upper() != name:
                        self.errors.append("👉 L'artiste n'a pas son nom de famille Majuscule")

    def check_album(self, track):
        if not track.album:
            self.errors.append("👉 Nom d'album manquant")

    def check_track(self, track):
        if not track.title:
            self.errors.append("👉 Nom de piste manquant")

    def check_date(self, track):
        if not track.recorded_date:  # track.year
            self.errors.append("👉 Année manquante: (track.year: {})".format(track.year, track.recorded_date))

    def check_cover(self, track):
        if not track.cover:
            self.errors.append("👉 🖼️  Image manquante")

    def check_bitrate(self, track):
        if not track.bit_rate:
            self.errors.append("👉 📢 Pas de tags audio")

        # < 320Kbps
        elif track.bit_rate < 320000:
            self.errors.append("👉 📢 Le bitrate est inférieur à 320kbps: {}".format(track.bit_rate))

    def check_for_japanese_text(self, track):
        self.check_for_japanese_artist(track)
        self.check_for_japanese_album(track)
        self.check_for_japanese_track(track)

    def check_for_japanese_artist(self, track):
        if is_japanese_in_string(track.performer):
            self.errors.append("👉 🇯🇵 Nom de l'artiste en Japonais".format(track.performer))

    def check_for_japanese_album(self, track):
        if is_japanese_in_string(track.album):
            self.errors.append("👉 🇯🇵 Nom de l'album en Japonais".format(track.album))

    def check_for_japanese_track(self, track):
        if is_japanese_in_string(track.title):
            self.errors.append("👉 🇯🇵 Nom du morceau en Japonais".format(track.title))

    def check_catalog_number(self, track):
        #pprint(dir(track))
        if not track.catalognumber:
            self.errors.append("👉 📙 Pas de numéro de catalogue")

    def append_errors_to_list(self, errors_list):
        if self.errors:
            errors = {"filepath": self.filepath, "errors": self.errors}
            errors_list.append(errors)

def main():
    path = sys.argv[1]
    extensions = (".mp3")
    entries = []

    # ----- Filters -----
    ignore_paths = ()
    ignore_list_filename = "ignore.txt"
    if os.path.isfile(ignore_list_filename):
        with open(ignore_list_filename, "r", encoding="utf-8") as ignore_file:
            ignore_paths = tuple(map(lambda row: row.strip(), ignore_file.readlines()))

    # ----- Listing -----
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if not filepath.startswith(ignore_paths):
                if filename.lower().endswith(extensions):
                    song = Song(filepath)
                    song.check_rules()
                    song.append_errors_to_list(entries)

    # ----- Affichage des résultats -----
    for entry in entries:
        print(entry["filepath"])

        for error in entry["errors"]:
            print("  {}".format(error))

        print()

if __name__ == "__main__":
    main()
