# Autopunk: An automated music generation app

Autopunk uses a modified, version of Google Magenta's MusicVAE algorithm to generate unique guitar, bass, and drum tracks in the punk genre. The algorithm has been trained on a dataset of midi files drawn from 40 years worth of punk history (see the midi folder for the list of tracks).

Because the training checkpoint is about 2.7Gb, it will need to be downloaded separately. Contact me for more info.

For sheet music generation, Autopunk uses Lilypond, an open-source music enscription application. Lilypond must be installed on the server running Autopunk for the sheet music feature to function.
