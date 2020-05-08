from music21 import *
from pretty_midi import *

midi_data = PrettyMIDI('E:/hailn/Documents/Programming/autopunk/output/hierdec-trio_16bar_sample_2020-05-07_150336-000-of-001.mid')
for instrument in midi_data.instruments:
    if instrument.program == 0 and instrument.is_drum == False:
        instrument.program = 29
midi_data.write('E:/hailn/Documents/Programming/autopunk/output/hierdec-trio_16bar_sample_2020-05-07_150336-000-of-001-2.mid')
song = midi.translate.midiFilePathToStream('E:/hailn/Documents/Programming/autopunk/output/hierdec-trio_16bar_sample_2020-05-07_150336-000-of-001-2.mid')
for part in song.parts:
    part.removeByClass('Rest')
song.show('text')
