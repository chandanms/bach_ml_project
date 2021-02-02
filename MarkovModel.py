import pandas as pd
import numpy as np
import collections

F = pd.read_csv("F.txt", sep = "\t")
F.columns = ['Bass', 'Tenor', 'Alto', 'Soprano']
F.insert(loc=0, column='Time', value=range(0, len(F)))

# make different biagrams for the columns
bigram_Bass = []
for i in range(0,len(F)):
    if F.Soprano[i] != F.Bass.shift(-1)[i]:
        d = tuple([F.Bass[i],F.Bass.shift(-1)[i]])
        bigram_Bass.append(d)
bigram_Tenor = []
for i in range(0,len(F)):
    if F.Tenor[i] != F.Tenor.shift(-1)[i]:
        d = tuple([F.Tenor[i],F.Tenor.shift(-1)[i]])
        bigram_Tenor.append(d)
bigram_Alto = []
for i in range(0,len(F)):
    if F.Alto[i] != F.Alto.shift(-1)[i]:
        d = tuple([F.Alto[i],F.Alto.shift(-1)[i]])
        bigram_Alto.append(d)
bigram_Soprano = []
for i in range(0,len(F)):
    if F.Soprano[i] != F.Soprano.shift(-1)[i]:
        d = tuple([F.Soprano[i],F.Soprano.shift(-1)[i]])
        bigram_Soprano.append(d)

# obtain the different note lengths
import trimesh.voxel as tv
# first we compute the rle of all voices
bass_length = tv.runlength.dense_to_rle(np.array(F.Bass))
tenor_length = tv.runlength.dense_to_rle(np.array(F.Tenor))
alto_length = tv.runlength.dense_to_rle(np.array(F.Alto))
soprano_length = tv.runlength.dense_to_rle(np.array(F.Soprano))

notes_with_length_bass = []
i = 0
while i < len(bass_length):
    l = tuple([bass_length[i], bass_length[i+1]])
    notes_with_length_bass.append(l)
    i += 2
notes_with_length_alto = []
i = 0
while i < len(alto_length):
    l = tuple([alto_length[i], alto_length[i+1]])
    notes_with_length_alto.append(l)
    i += 2
notes_with_length_tenor = []
i = 0
while i < len(tenor_length):
    l = tuple([tenor_length[i], tenor_length[i+1]])
    notes_with_length_tenor.append(l)
    i += 2
notes_with_length_soprano = []
i = 0
while i < len(soprano_length):
    l = tuple([soprano_length[i], soprano_length[i+1]])
    notes_with_length_soprano.append(l)
    i += 2

def predict_next_state(bigram, note):
    """Predict next chord based on current state."""
    # create list of bigrams which stats with current note
    bigrams_with_current_note = [bigram[i] for i in range(0, len(bigram)) if bigram[i][0] == note]
    # count appearance of each bigram
    count_appearance = dict(collections.Counter(bigrams_with_current_note))
    # convert apperance into probabilities
    for ngram in count_appearance.keys():
        count_appearance[ngram] = float(count_appearance[ngram]) / len(bigrams_with_current_note)
    # create list of possible options for the next chord
    options = []
    for i in range(0, len(count_appearance)):
        d = list(count_appearance.keys())[i][1]
        options.append(d)
    # create  list of probability distribution
    probabilities = list(count_appearance.values())
    # return random prediction
    return np.random.choice(options, p=probabilities)

def predict_duration(notes_length, note):
    """Predict duration of predicted note"""
    # create a list of durations which stats with current note
    duration_with_current_note = [notes_length[i] for i in range(0, len(notes_length)) if notes_length[i][0] == note]
    # count appearance of each bigram
    count_appearance = dict(collections.Counter(duration_with_current_note))
    # convert appearance into probabilities
    for ngram in count_appearance.keys():
        count_appearance[ngram] = float(count_appearance[ngram]) / len(duration_with_current_note)
    # create list of possible options for the next duration
    options = []
    for i in range(0, len(count_appearance)):
        d = list(count_appearance.keys())[i][1]
        options.append(d)
    # create  list of probability distribution
    probabilities = list(count_appearance.values())
    # return random prediction
    return np.random.choice(options, p=probabilities)

def generate_sequence(bigram, note, notes_length, length):
    """Generate sequence of defined length."""
    # create list to store future chords
    notes = []
    for n in range(length):
        # predict next chord
        next_chord = predict_next_state(bigram, note)
        # predict duration of the note
        duration = predict_duration(notes_length, note)
        # append next chord for the list
        notes.append([next_chord]*duration)
        # use last chord in sequence to predict next chord
        note = notes[-1][-1]
    return notes

# output
n = 30 # number of notes predicted
last_note_Bass = bigram_Bass[-1][0]
print(generate_sequence(bigram_Bass, last_note_Bass, notes_with_length_bass, n))
last_note_Tenor = bigram_Tenor[-1][0]
print(generate_sequence(bigram_Tenor, last_note_Tenor, notes_with_length_tenor, n))
last_note_Alto = bigram_Alto[-1][0]
print(generate_sequence(bigram_Alto, last_note_Alto, notes_with_length_alto, n))
last_note_Soprano = bigram_Soprano[-1][0]
print(generate_sequence(bigram_Soprano, last_note_Soprano, notes_with_length_soprano, n))




