# packages
import numpy as np
import pandas as pd
from tools import convertNotesTomidifile
import trimesh.voxel as tv
import collections
from fractions import Fraction
import random

F = pd.read_csv("F.txt", sep = "\t")
F.columns = ['Soprano', 'Alto', 'Tenor', 'Bass']
F.insert(loc=0, column='Time', value=range(0, len(F)))

def predict_next_state(sequence):
    """Predict next note based on distributions."""
    # predict next note based on normal distribution
    seq = sequence[sequence > 0]
    mu = seq.mean()
    sigma = seq.std()
    note = int(np.random.normal(mu, sigma))
    # obtain Bernouilli distribution 0 vs. not 0
    length = tv.runlength.dense_to_rle(np.array(sequence))
    notes_with_length = []
    i = 0
    while i < len(length):
        l = tuple([length[i], length[i + 1]])
        notes_with_length.append(l)
        i += 2
    count_appearance = dict(collections.Counter(notes_with_length))
    k = 0
    for ngram in count_appearance.keys():
        if ngram[0] == 0:
            k = k + count_appearance[ngram]
    p = float(Fraction(k, len(count_appearance)))
    options = [note, 0]
    probabilities = [(1-p), p]
    # return the note chosen with probabilities as weight
    return np.random.choice(options, p=probabilities)

def predict_duration(sequence):
    """Predict duration of predicted note"""
    note = predict_next_state(sequence)
    if note != 0:
        seq = sequence[sequence > 0]
        length = tv.runlength.dense_to_rle(np.array(seq))
        length_values = []
        k = 1
        while k <= len(length):
            length_values.append(length[k])
            k = k + 2
        lamda = np.array(length_values).mean()
        duration = int(np.random.poisson(lamda, 1))
    if note == 0:
        length = tv.runlength.dense_to_rle(np.array(F.Soprano))
        notes_with_length = []
        i = 0
        while i < len(length):
            l = tuple([length[i], length[i + 1]])
            notes_with_length.append(l)
            i += 2
        durations_zero = []
        for i in range(0, len(notes_with_length)):
            if notes_with_length[i][0] == 0:
                durations_zero.append(notes_with_length[i][1])
        duration = int(np.random.choice(durations_zero))
    return duration

def generate_sequence(sequence, length):
    """Generate sequence of defined length."""
    # create list to store future chords
    notes = []
    for n in range(length):
        # predict next chord
        next_chord = predict_next_state(sequence)
        # predict duration of the note
        duration = predict_duration(sequence)
        # append next chord for the list
        notes.append([next_chord]*duration)
        # use last chord in sequence to predict next chord
        note = notes[-1][-1]
    notes = [item for sublist in notes for item in sublist]
    return notes

# create output
random.seed(10)
n = 10 # number of notes predicted
pred_Bass = generate_sequence(F.Bass, n)
convertNotesTomidifile(pred_Bass, 'Bass_output_distr')
pred_Tenor = generate_sequence(F.Tenor, n)
convertNotesTomidifile(pred_Tenor, 'Tenor_output_distr')
pred_Alto = generate_sequence(F.Alto, n)
convertNotesTomidifile(pred_Alto, 'Alto_output_distr')
pred_Soprano = generate_sequence(F.Soprano, n)
convertNotesTomidifile(pred_Soprano, 'Soprano_output_distr')
