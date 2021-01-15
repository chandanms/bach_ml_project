import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

from sklearn.linear_model import Ridge
from audiolazy import freq2midi
from midiutil.MidiFile import MIDIFile

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


def noteToFreq(note):
    a = 440 #frequency of A (coomon value is 440Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

def representationToNote(representation_list):

	notes_list = []
	
	for i, representation in enumerate(representation_list):

		note_in_freq = representation[0]

		note_in_midi = int(freq2midi(note_in_freq))

		if note_in_midi < 0:
			note_in_midi = 0

		notes_list.append(note_in_midi)

	return notes_list


def convertNotesTomidifile(notes_list, outputfile_name):

	## converts and stores the midi file in the folder results

	# create your MIDI object
	mf = MIDIFile(1)     # 4 tracks

	time = 0    # start at the beginning
	beats_per_minute = 120

	mf.addTrackName(0, time, "Track 1")
	mf.addTempo(0, time, beats_per_minute)

	#initialize a list which stores notes, and only adds them to the midi after the full duration is known
	note_storage = Note()

	max_iter = 1000
	i = 0
	for note in notes_list:
		i += 1
		track_pitch = int(note)
		current_note = note_storage
		if track_pitch == current_note.pitch:
			current_note.add_dur()
			note_storage = current_note
		else:
			add_note_to_track(0, current_note, mf)
			note_storage = Note(time, track_pitch)
		time += tick_length #move 1/4 beat into the future

	#After text file ends, add the remaining notes
	add_note_to_track(0, note_storage, mf)

	# write it to disk
	with open("results/" + outputfile_name + ".mid", 'wb') as outf:
		mf.writeFile(outf)


def convertNotestoTextfile(notes_list, outputfile_name):

	# converts and stores text file in the folder results

	with open("results/" + outputfile_name + ".txt", "w") as filehandle:
		filehandle.write("\n".join(str(note) for note in notes_list))




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

representation_list = noteToRepresentation(note_text_file_name)

predicted_representation_list = window_based_ridge_regression(20, representation_list, 100)

predicted_notes_list = representationToNote(predicted_representation_list)

convertNotesTomidifile(predicted_notes_list, "ridge_prediction_2")

convertNotestoTextfile(predicted_notes_list, "ridge_prediction_2")







