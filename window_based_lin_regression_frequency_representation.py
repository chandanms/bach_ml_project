import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from audiolazy import freq2midi



def noteToFreq(note):
    a = 440 #frequency of A (coomon value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))




def noteToRepresentation(note_text_file_name):	

	note_text_file = open(note_text_file_name, "r")

	frequency_list = []

	notes_list = []

	for note in note_text_file:

		notes_list.append(int(note))


	representation_list = []

	for i, note in enumerate(notes_list):

		note_in_freq = noteToFreq(int(note))

		zeroth_octave_note = noteToFreq((int(note)%12))

		distance_from_zeroth_octave = (noteToFreq(int(note)) - noteToFreq((int(note)%12)))

		representation_list.append([note_in_freq, zeroth_octave_note, distance_from_zeroth_octave])

	return representation_list


def window_based_linear_regression(window_size, notes_list, predictions) :	

	X_dataset = []
	y_dataset = []

	for i, note in enumerate(notes_list) :

		if (i == (len(notes_list) - (window_size))) :
			break
		else :
			window_list =[]
			for size in range(0, window_size) :
				window_list.append(notes_list[i+size])
			X_dataset.append(window_list)
			y_dataset.append(notes_list[i+(window_size)][0])

	X_dataset = np.array(X_dataset)

	nsamples, nx, ny = X_dataset.shape

	X_dataset = X_dataset.reshape((nsamples,nx*ny))

	model = LinearRegression().fit(X_dataset, y_dataset)

	cross_val_score(model, X_dataset, y_dataset, cv=10).mean()

	predicted_frequency = model.predict([X_dataset[-1]])

	if predicted_frequency[0] < 0 :
		predicted_frequency[0] = 0

	predicted_note = int(freq2midi(predicted_frequency[0]))

	notes_list.append(predicted_note)

	# print (len(notes_list))

	# with open("results/" + "predicted_freqency_representation_linear_" + note_text_file_name.split('/')[1].split('.')[0] + ".txt", "w") as filehandle:
	# 	filehandle.write("\n".join(str(note) for note in notes_list))
	
	return notes_list



note_text_file_name = "dataset/2.txt"

representation_list = noteToRepresentation(note_text_file_name)

window_based_linear_regression(5, representation_list, 5)



