from new_results.representation_input import representation_input
from new_results.representation_output import representation_output
from new_results.window_matrix import window_matrix
from new_results.representation_output import output_note_list
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from new_results.pick_note import unity_based_normalization
from new_results.pick_note import pick_note
from sklearn.metrics import mean_squared_error, r2_score


def predict_regression(window_size, notes, number_predictions, p):
    # Represent the notes list as a matrix input #
    x_input = representation_input(notes)

    # Create a matrix that is suitable for a linear regression such that window size is transformed
    x_matrix = window_matrix(window_size, x_input)

    y_matrix = representation_output(notes)
    # Make sure that y_matrix and x_matrix are of the same size #
    del y_matrix[0:window_size]

    # Output notes contains all the notes that are represented by the output vector y #
    output_notes = output_note_list(notes)

    trained_model = LinearRegression().fit(x_matrix, y_matrix)
    # What does this function do ? #
    cross_score = cross_val_score(trained_model, x_matrix, y_matrix, cv=10).mean()
    print(cross_score)
    y_predicted = trained_model.predict(x_matrix)
    rmse = mean_squared_error(y_matrix, y_predicted)
    print(rmse)
    r2 = r2_score(y_matrix, y_predicted)
    print(r2)

    # In this part we predict values for the number of predictions we want #
    for number_predictions in range(0, number_predictions):
        # Predict a new value for y #
        predicted_y = trained_model.predict([x_matrix[-1]])

        # Normalize the vector accordingly #

        normalized_y = unity_based_normalization(predicted_y)

        predict_note = pick_note(normalized_y, p, output_notes)

        # Select the note based on the highest probability #
        # highest_probability_index = np.argmax(predicted_y)
        # predict_note = output_notes[highest_probability_index]

        # Add the new note to the old list
        notes.append(predict_note)

        # Represent the notes list as a matrix input #
        x_input = representation_input(notes)

        # Create a matrix that is suitable for a linear regression
        x_matrix = window_matrix(window_size, x_input)

    return notes
