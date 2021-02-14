from tools.notes_to_midi import convertNotesTomidifile
from regressions.predict_regression import predict_regression, predict_regression_with_notepdf


# name of each individual voices
note_text_file_name = "dataset/4.txt"

note_text_file = open(note_text_file_name, "r")
notes_list = []

for note in note_text_file:
    notes_list.append(int(note))


# Make sure here to select the right part of the notes list data, you will get different values #
#notes_list = notes_list[248:3797]

print(len(notes_list))
tick_length = 0.25



predicted_notes_list, score = predict_regression_with_notepdf(window_size=10, notes=notes_list, number_predictions=200)

print(len(predicted_notes_list))

# predict notes and store
convertNotesTomidifile(predicted_notes_list, "linear_prediction_4")
