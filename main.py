import os
import re

from pymediainfo import MediaInfo

path = "/home/seigneurfuo/NAS/Fichiers/Musique"
extensions = (".mp3")

def is_japanese_in_string(text):
    # https://gist.github.com/ryanmcgrath/982242
    regex = re.compile("[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B")
    return regex.match(text)

def check_file_mediainfo(filepath):
    msg = ""

    media_info = MediaInfo.parse(filepath)
    for track in media_info.tracks:
        if track.track_type == "General":
            if is_japanese_in_string(track.performer):
                msg += "\n\t- Nom de l'artiste en Japonais"

            # Si le nom de l'artiste n'est pas en majuscule
            if not "&" or ";" in track.performer:
                splitted = track.performer.split(" ")

                if len(splitted) >= 2:
                    name = splitted[-1]
                    if name.upper() != name:
                        msg += "\n\t- L'artiste n'a pas son nom de famille Majuscule"

            if "&" or ";" in track.performer:
                msg += "\n\t- Multiples artistes"

            if is_japanese_in_string(track.album):
                msg += "\n\t- Nom de l'album en Japonais"

            if is_japanese_in_string(track.title):
                msg += "\n\t- Nom du morceau en Japonais"

            if not track.year:
                msg += "\n\t- Année manquante"

            if not track.cover:
                msg += "\n\t- Image manquante"

            # TODO: Artiste de l'album

        elif track.track_type == "Audio":
            # ---- 320 kpbs ----
            if track.bit_rate is None:
                msg += "\n\t- Pas de tags"

            elif track.bit_rate < 320000:
                msg += "\n\t- Le bitrate est inférieur à 320kbps: {}".format(track.bit_rate)

    if msg:
        print(filepath, msg, "\n")

def main():
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                audio_file = os.path.join(root, filename)
                #print(audio_file)
                check_file_mediainfo(audio_file)


if __name__ == "__main__":
    main()
