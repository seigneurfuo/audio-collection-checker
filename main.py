import os

import eyed3

path = "/home/seigneurfuo/NAS/Fichiers/Musique"
extensions = (".mp3", "")


def check_file(filepath):
    audiofile = eyed3.load(filepath)

    if audiofile:
        if audiofile.tag is None:
            msg = "Pas de tags: {}:".format(filepath)
            print(msg)

        elif audiofile.tag.images is None or len(audiofile.tag.images) == 0:
            msg = "Pas d'image image: {}:".format(filepath)
            print(msg)


def main():
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(extensions):
                audio_file = os.path.join(root, filename)
                #print(audio_file)
                check_file(audio_file)


if __name__ == "__main__":
    main()
