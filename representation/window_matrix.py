import numpy as np


def window_matrix(window_size, x_input):
    # This function makes the input data ready for a linear regression by creating a matrix #
    x_data = []

    for i, note in enumerate(x_input):
        # convert the training data X into window based data
        if i == (len(x_input) - window_size):
            break
        else:
            window_list = []
            for size in range(0, window_size):
                window_list.append(x_input[i + size])
            x_data.append(window_list)
    # Returns a number rows(input) x window size #

    # Reshape the dataset x for the linear regression #
    x_data = np.array(x_data)
    number_samples, nx, ny = x_data.shape
    x_matrix = x_data.reshape((number_samples, nx * ny))

    return x_matrix
