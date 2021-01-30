

def unity_based_normalization(prob_vector):
    # In this function we perform a unity based normalization, where afterwards we normalized that vector normally #
    unity_normalization = (prob_vector - prob_vector.min()) / (prob_vector.max() - prob_vector.min())

    # Normalize the output in a normal way
    normalized_output = unity_normalization / unity_normalization.sum()

    # Flatten the array to a 1D, this is need for later picking random numbers #
    normalized_output = normalized_output.flatten()

    return normalized_output


