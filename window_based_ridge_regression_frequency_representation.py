import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

from sklearn.linear_model import Ridge
from audiolazy import freq2midi
from midiutil.MidiFile import MIDIFile

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




def window_based_ridge_regression(window_size, representation_list, predictions) :

	for predictions in range(0, predictions):

		X_dataset = []
		y_dataset = []

		for i, note in enumerate(representation_list) :

			if (i == (len(representation_list) - (window_size))) :
				break
			else :
				window_list =[]
				for size in range(0, window_size) :
					window_list.append(representation_list[i+size])
				X_dataset.append(window_list)
				y_dataset.append(representation_list[i+(window_size)][0])

		print (X_dataset, y_dataset)

		X_dataset = np.array(X_dataset)
		
		nsamples, nx, ny = X_dataset.shape

		X_dataset = X_dataset.reshape((nsamples,nx*ny))

		alpha = 0.99
		
		model = Ridge(alpha=alpha).fit(X_dataset, y_dataset)

		print(cross_val_score(model, X_dataset, y_dataset, cv=10).mean())

		predicted_frequency = model.predict([X_dataset[-1]])

		if predicted_frequency[0] < 0 :
			predicted_frequency[0] = 0

		predicted_note = int(freq2midi(predicted_frequency[0]))

		predicted_note_in_freq = noteToFreq(predicted_note)

		zeroth_octave_predicted_note = noteToFreq((int(predicted_note)%12))

		distance_from_zeroth_octave = noteToFreq(int(predicted_note)) - noteToFreq((int(predicted_note)%12))

		representation_list.append([predicted_note_in_freq, zeroth_octave_predicted_note, distance_from_zeroth_octave])
	
	return representation_list



note_text_file_name = "dataset/2.txt"

# Changes the notes to representation
representation_list = noteToRepresentation(note_text_file_name)

# window based regression with size of the window, representation and number of predictions

predicted_representation_list = window_based_ridge_regression(3, representation_list, 100)

predicted_notes_list = representationToNote(predicted_representation_list)

convertNotesTomidifile(predicted_notes_list, "ridge_prediction_2")

convertNotestoTextfile(predicted_notes_list, "ridge_prediction_2")







