import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from audiolazy import freq2midi

from tools import noteToFreq, representationToNote, convertNotesTomidifile, convertNotestoTextfile, noteToRepresentation


tick_length = 0.25

class Note:

	def __init__(self, time = 0, pitch = 0):
		self.duration = tick_length
		self.time = time
		self.pitch = pitch
	def add_dur(self):
		self.duration += tick_length


def add_note_to_track(track, note, mf):
	if not note.pitch == 0:	#pitch of 0 means no note is being played
		volume = 100
		channel = 0
		mf.addNote(track, channel, note.pitch, note.time, note.duration, volume)


def get_unique_note_list():

	note_text_file_name = "dataset/F.txt"

	line_list = []

	with open(note_text_file_name, "r") as f:
		lines = f.readlines()

		for col in range(0, 4) :
			line_list=[]
			for x in lines:
				line_list.append(int(x.rstrip("\n").split('\t')[col]))
	f.close()

	return (list(set(line_list)))

def get_unique_note_list_in_frequency():

	line_list = []

	with open(note_text_file_name, "r") as f:
		lines = f.readlines()

		for line in lines:
			line_list.append(int(line.rstrip("\n")))
	f.close()

	unique_note_list = list(set(line_list))

	unique_note_frequency_list = []

	for note in unique_note_list :

		unique_note_frequency_list.append(noteToFreq(note))

	return unique_note_frequency_list



def window_based_linear_regression(window_size, notes_list, predictions) :

	for predictions in range(0, predictions):

		X_dataset = []
		y_dataset = []

		for i, note in enumerate(notes_list) :

			## convert the training data X into window based data
			if (i == (len(notes_list) - (window_size))) :
				break
			else :
				window_list =[]
				for size in range(0, window_size) :
					window_list.append(notes_list[i+size])
				X_dataset.append(window_list)

				## get binary vector for the corresponding Y, where the index of Y is 1, rest is zero

				y = notes_list[i+(window_size)][0]

				'''predictions might not be in current unique notes which us used to get index, 
				if that's the case, add the preicted note to unique note list 
				and then proceed with vectorization'''

				if y not in unique_note_frequency_list:
					unique_note_frequency_list.append(y)
				
				y_index = unique_note_frequency_list.index(y)

				y_binary_vector = np.zeros(len(unique_note_frequency_list))

				y_binary_vector[y_index] = 1

				print (y_binary_vector)

				y_dataset.append(y_binary_vector)

		## Linear regression

		X_dataset = np.array(X_dataset)

		nsamples, nx, ny = X_dataset.shape

		# reshape the dataset for the LR

		X_dataset = X_dataset.reshape((nsamples,nx*ny))

		model = LinearRegression().fit(X_dataset, y_dataset)

		cross_val_score(model, X_dataset, y_dataset, cv=10).mean()


		# predict the frequency of next note based on the last note or representation and store it as array

		predicted_probability_frequency = model.predict([X_dataset[-1]])[0]


		# get highest probability from predicted probabilities and convert it into known frequency
		highest_probability_index = np.argmax(predicted_probability_frequency)
		predicted_frequency = unique_note_frequency_list[highest_probability_index]


		# get frequency representation of the predicted frequency and add it to the dataset for next iteration

		predicted_note = int(freq2midi(predicted_frequency))

		predicted_note_in_freq = noteToFreq(predicted_note)

		zeroth_octave_predicted_note = noteToFreq((int(predicted_note)%12))

		distance_from_zeroth_octave = noteToFreq(int(predicted_note)) - noteToFreq((int(predicted_note)%12))

		notes_list.append([predicted_note_in_freq, zeroth_octave_predicted_note, distance_from_zeroth_octave])
	
	return notes_list


note_text_file_name = "dataset/2.txt"

unique_note_frequency_list = get_unique_note_list_in_frequency()

print (unique_note_frequency_list)

# Changes the notes to representation
representation_list = noteToRepresentation(note_text_file_name)

# window based regression with size of the window, representation and number of predictions

predicted_representation_list = window_based_linear_regression(3, representation_list, 100)

predicted_notes_list = representationToNote(predicted_representation_list)

convertNotesTomidifile(predicted_notes_list, "linear_prediction_2")

convertNotestoTextfile(predicted_notes_list, "linear_prediction_2")






