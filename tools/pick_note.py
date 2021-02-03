import numpy as np
from audiolazy import freq2midi

def unity_based_normalization(prob_vector):
    # In this function we perform a unity based normalization, where afterwards we normalized that vector normally #
    unity_normalization = (prob_vector - prob_vector.min()) / (prob_vector.max() - prob_vector.min())

    # Normalize the output in a normal way
    normalized_output = unity_normalization / unity_normalization.sum()

    # Flatten the array to a 1D, this is need for later picking random numbers #
    normalized_output = normalized_output.flatten()

    return normalized_output


def pick_note(prob_vector, p, output_notes):
    # In this function we have a picking algorithm p should be between 0 and 1 #
    # And will be added to the random choice output #

    random_note = np.random.choice(output_notes, size=1, p=prob_vector)
    random_note = np.asscalar(random_note)

    # Get the index of the vector and p #
    index = output_notes.index(random_note)
    prob_vector[index] += p

    # Normalize again the vector #
    prob_vector = prob_vector / prob_vector.sum()

    highest_prob_index = np.argmax(prob_vector)
    predict_note = output_notes[highest_prob_index]

    return predict_note


def pick_top5_note(prob_vector, output_notes):
    
    # In this function we pick a frequency from top 5 predictions
    random_note = np.random.choice(sorted(prob_vector, reverse=True)[:5])


    # Get index of the chosen note
    index = list(prob_vector).index(random_note)

    predict_note = output_notes[index]

    return predict_note