import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections

F = pd.read_csv("F.csv", sep = "\t")
F.columns = ['Bass', 'Tenor', 'Alto', 'Soprano']
F.insert(loc=0, column='Time', value=range(0, len(F)))
F_diff = F.diff().dropna()

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

def generate_sequence(bigram, note, length):
    """Generate sequence of defined length."""
    # create list to store future chords
    notes = []
    for n in range(length):
        # append next chord for the list
        notes.append(predict_next_state(bigram, note))
        # use last chord in sequence to predict next chord
        note = notes[-1]
    return notes

# examples
last_note_Bass = bigram_Bass[-1][0]
generate_sequence(bigram_Bass, last_note_Bass, 30)
last_note_Tenor = bigram_Tenor[-1][0]
generate_sequence(bigram_Tenor, last_note_Tenor, 30)
last_note_Alto = bigram_Alto[-1][0]
generate_sequence(bigram_Alto, last_note_Alto, 30)
last_note_Soprano = bigram_Soprano[-1][0]
generate_sequence(bigram_Soprano, last_note_Soprano, 30)




