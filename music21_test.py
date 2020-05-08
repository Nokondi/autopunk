from music21 import *

song = midi.translate.midiFilePathToStream('E:/hailn/Documents/Programming/autopunk/output/hierdec-trio_16bar_sample_2020-05-07_150336-000-of-001.mid')
for part in song.parts:
    part.removeByClass('Rest')
song.show('text')
song.show('lily.pdf')