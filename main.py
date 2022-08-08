import os
import re
import sys

from pymediainfo import MediaInfo

def is_japanese_in_string(text):
    # https://gist.github.com/ryanmcgrath/982242
    regex = re.compile("[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B")
    return regex.match(text)

def check_file_mediainfo(filepath):
    msg = ""

    media_info = MediaInfo.parse(filepath)
    for track in media_info.tracks:
        if track.track_type == "General":
            if not track.performer:
                msg += "\n\t👉 Artiste manquant"
            else:
                if is_japanese_in_string(track.performer):
                    msg += "\n\t👉 🇯🇵 Nom de l'artiste en Japonais".format(track.performer)

                # Si le nom de l'artiste n'est pas en majuscule
                if "&" in track.performer or ";" in track.performer:
                    msg += "\n\t👉 Multiples artistes: {}".format(track.performer)

                else:
                    splitted = track.performer.split(" ")

                    if len(splitted) >= 2:
                        name = splitted[-1]
                        if name.upper() != name:
                            msg += "\n\t👉 L'artiste n'a pas son nom de famille Majuscule"



            if not track.album:
                msg += "\n\t👉 Nom d'albulm manquant"
            else:
                if is_japanese_in_string(track.album):
                    msg += "\n\t👉 🇯🇵 Nom de l'album en Japonais".format(track.album)

            if not track.title:
                msg += "\n\t👉 Nom de piste manquant"
            else:
                if is_japanese_in_string(track.title):
                    msg += "\n\t👉 🇯🇵 Nom du morceau en Japonais".format(track.title)

            if not track.recorded_date: # track.year
                msg += "\n\t👉 Année manquante: (track.year: {})".format(track.year, track.recorded_date)

            if not track.cover:
                msg += "\n\t👉 Image manquante"

            # TODO: Artiste de l'album

        elif track.track_type == "Audio":
            # ---- 320 kpbs ----
            if not track.bit_rate:
                msg += "\n\t👉 Pas de tags audio"

            elif track.bit_rate < 320000:
                msg += "\n\t👉 Le bitrate est inférieur à 320kbps: {}".format(track.bit_rate)

    if msg:
        print(filepath, msg, "\n")

def main():
    path = sys.argv[1]
    extensions = (".mp3")

    for root, directories, filenames in os.walk(path):
        msg = "\n----- 📁 {} -----".format(root)
        print(msg)

        for filename in filenames:
            if filename.lower().endswith(extensions):
                audio_file = os.path.join(root, filename)
                check_file_mediainfo(audio_file)


if __name__ == "__main__":
    main()
