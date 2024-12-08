import numpy as np
from tensorflow.keras.models import load_model
from music21 import note, chord, stream

# Load the model
model = load_model('LSTM_Model.h5')
# Load your mappings
reverse_mapping = {i: c for i, c in enumerate(sorted(set(Corpus)))}  # You need to have this array available
L_symb = len(reverse_mapping)  # Total number of unique notes

def generate_music(note_count, X_seed, length):
    seed = X_seed[np.random.randint(0, len(X_seed)-1)]
    Notes_Generated = []
    for i in range(note_count):
        seed = seed.reshape(1, length, 1)
        prediction = model.predict(seed, verbose=0)[0]
        index = np.argmax(np.log(prediction) / 1.0 - np.exp(prediction))
        Notes_Generated.append(index)
        index_N = index / float(L_symb)
        seed = np.insert(seed[0], len(seed[0]), index_N)
        seed = seed[1:]
    Music = [reverse_mapping[char] for char in Notes_Generated]
    Melody = chords_n_notes(Music)
    return Melody

def chords_n_notes(snippet):
    melody = []
    offset = 0
    for i in snippet:
        if "." in i or i.isdigit():
            notes = [note.Note(int(n)) for n in i.split('.')]
            chord_note = chord.Chord(notes)
            chord_note.offset = offset
            melody.append(chord_note)
        else:
            single_note = note.Note(i)
            single_note.offset = offset
            melody.append(single_note)
        offset += 1
    return stream.Stream(melody)
