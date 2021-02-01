from new_results.notes_to_midi import convertNotesTomidifile
from new_results.regression import predict_regression

note_text_file_name = "dataset/2.txt"

note_text_file = open(note_text_file_name, "r")
notes_list = []

for note in note_text_file:
    notes_list.append(int(note))


# Make sure here to select the right part of the notes list data, you will get different values #
notes_list = notes_list[2484:3812]
print(len(notes_list))
tick_length = 0.25

predicted_notes_list = predict_regression(window_size=8, notes=notes_list, number_predictions=200, p=0.075)

print(len(predicted_notes_list))

convertNotesTomidifile(predicted_notes_list, "linear_prediction_2")
