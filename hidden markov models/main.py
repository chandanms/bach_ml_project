import pandas as pd
import numpy as np
import collections
from tools.tools import convertNotesTomidifile, get_unique_note_list
from collections import defaultdict

import matplotlib.pyplot as plt
import seaborn as sns

def remove_zeroes(note_list):

    edited_list = []
    for i, note in enumerate(note_list):
        if note == 0:
            if (np.random.choice([0, 1], p=(0.7, 0.3)) == 1):
                pass
            else:
                edited_list.append(note)
        else:
            edited_list.append(note)

    return edited_list



def get_transition_matrix(note_list):
    """Predict next note based on current state."""


    note_list = pd.Series(note_list)

    bigram = []
    for i in range(0,len(note_list)):
        d = tuple([ note_list[i],note_list.shift(-1)[i]])
        bigram.append(d)

    unique_notes = list(set(note_list))

    note_dict = defaultdict(list)

    prob_dict = defaultdict(list)

    for note in unique_notes:

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

        prob_dict[note] = probabilities

        note_dict[note] = options



    trans_matrix = []

    '''transistion matrix from a to b'''
    for a_note in unique_notes:
        a_note_trans_list = []
        for b_note in unique_notes:

            try :
                b_note_index = note_dict[a_note].index(b_note)
                b_note_prob = prob_dict[a_note][b_note_index]
            except:
                b_note_prob = 0
            a_note_trans_list.append(b_note_prob)
        trans_matrix.append(a_note_trans_list)

    return trans_matrix

def get_emission_matrix(x_list, y_list):

    '''get emission matrix'''

    note_dict = defaultdict(list)

    prob_dict = defaultdict(list)


    unique_notes_x = set(x_list)
    unique_notes_y = set(y_list)

    bigrams_xy = list(zip(y_list, x_list))

    for y_note in unique_notes_y:

        bigrams_with_y_note = [bigrams_xy[i] for i in range(0, len(bigrams_xy)) if bigrams_xy[i][0] == y_note]

        count_appearance = dict(collections.Counter(bigrams_with_y_note))

        for ngram in count_appearance.keys():
            count_appearance[ngram] = float(count_appearance[ngram]) / len(bigrams_with_y_note)

        options = []
        for i in range(0, len(count_appearance)):
            d = list(count_appearance.keys())[i][1]
            options.append(d)

        # create  list of probability distribution
        probabilities = list(count_appearance.values())

        prob_dict[y_note] = probabilities

        note_dict[y_note] = options

    e_matrix = []

    for a_note in unique_notes_y:
        a_note_trans_list = []
        for b_note in unique_notes_x:

            try :
                b_note_index = note_dict[a_note].index(b_note)
                b_note_prob = prob_dict[a_note][b_note_index]
            except:
                b_note_prob = 0
            a_note_trans_list.append(b_note_prob)
        e_matrix.append(a_note_trans_list)

    return e_matrix


def predict_next_notes(predictions):

    bass_list = (F.Bass).tolist()
    tenor_list = (F.Tenor).tolist()
    alto_list = (F.Alto).tolist()
    soprano_list = (F.Soprano).tolist()

    bass_list_edited = remove_zeroes(bass_list)
    tenor_list_edited = remove_zeroes(tenor_list)
    alto_list_edited = remove_zeroes(alto_list)
    soprano_list_edited = remove_zeroes(soprano_list)

    voice_list_original = [bass_list, tenor_list, alto_list, soprano_list]


    voice_list = [bass_list_edited, tenor_list_edited, alto_list_edited, soprano_list_edited]


    for pred in range(0, predictions):

        for i, voice in enumerate(voice_list) :

            x_list = voice_list[i%len(voice_list)]
            y1_list = voice_list[(i+1)%len(voice_list)]
            y2_list = voice_list[(i+2)%len(voice_list)]
            y3_list = voice_list[(i+3)%len(voice_list)]

            x_unique_notes = list(set(x_list))
            y1_unique_notes = list(set(y1_list))
            y2_unique_notes = list(set(y2_list))
            y3_unique_notes = list(set(y3_list))

            X_t0 = x_list[-1]
            y1_t0 = y1_list[-1]
            y2_t0 = y2_list[-1]
            y3_t0 = y3_list[-1]

            trans_matrix = get_transition_matrix(x_list)

            ax = sns.heatmap(trans_matrix, linewidth=0.5)
            plt.show()


            trans_p = trans_matrix[x_unique_notes.index(X_t0)]

            e_matrix_y1 = get_emission_matrix(x_list, y1_list)
            emission_p_y1 = e_matrix_y1[y1_unique_notes.index(y1_t0)]

            #print (e_matrix_y1)
            ax = sns.heatmap(e_matrix_y1, linewidth=0.5)
            plt.show()


            e_matrix_y2 = get_emission_matrix(x_list, y2_list)
            emission_p_y2 = e_matrix_y2[y2_unique_notes.index(y2_t0)]

            #print (e_matrix_y2)
            ax = sns.heatmap(e_matrix_y2, linewidth=0.5)
            plt.show()

            e_matrix_y3 = get_emission_matrix(x_list, y3_list)
            emission_p_y3 = e_matrix_y3[y3_unique_notes.index(y3_t0)]


            ax = sns.heatmap(e_matrix_y3, linewidth=0.5)
            plt.show()

            ax = sns.heatmap(np.dot(np.transpose(np.dot(np.array(trans_matrix), np.transpose(np.array(e_matrix_y1)))), np.transpose(np.array(e_matrix_y2))), linewidth=0.5)
            plt.show()

            p = [a*b for a,b in zip(trans_p, emission_p_y1)]

            p = [a*b for a,b in zip(p, emission_p_y2)]

            p = [a*b for a,b in zip(p, emission_p_y3)]

            p = np.asarray(p).astype('float')

            p = p / sum(p)

            note_choice = np.random.choice(x_unique_notes, p=p)

            voice_list[i%len(voice_list)].append(note_choice)
            voice_list_original[i%len(voice_list)].append(note_choice)

    return voice_list_original


F = pd.read_csv("dataset/F.txt", sep = "\t")
F.columns = ['Bass', 'Tenor', 'Alto', 'Soprano']
F.insert(loc=0, column='Time', value=range(0, len(F)))

# make different biagrams for the columns
bigrams = []


bigram_Bass = []
for i in range(0,len(F)):
    d = tuple([F.Bass[i],F.Bass.shift(-1)[i]])
    bigram_Bass.append(d)
    bigrams.append(d)

bigram_Tenor = []
for i in range(0,len(F)):
    d = tuple([F.Tenor[i],F.Tenor.shift(-1)[i]])
    bigram_Tenor.append(d)
    bigrams.append(d)

bigram_Alto = []
for i in range(0,len(F)):
    if F.Alto[i] != F.Alto.shift(-1)[i]:
        d = tuple([F.Alto[i],F.Alto.shift(-1)[i]])
        bigram_Alto.append(d)
        bigrams.append(d)
bigram_Soprano = []
for i in range(0,len(F)):
    if F.Soprano[i] != F.Soprano.shift(-1)[i]:
        d = tuple([F.Soprano[i],F.Soprano.shift(-1)[i]])
        bigram_Soprano.append(d)
        bigrams.append(d)

unique_notes = get_unique_note_list()

# print (unique_notes)

# trans_matrix = get_transition_matrix(bigrams, unique_notes)

# print(get_emission_matrix(F.Bass, F.Alto))

voice_list = predict_next_notes(100)

print (len(voice_list[0]))

print (voice_list[0][-100:], voice_list[1][-100:], voice_list[2][-100:], voice_list[3][-100:])