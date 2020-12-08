import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score


from midiutil.MidiFile import MIDIFile


file_name = "dataset/4.txt"


f = open(file_name)

lines = f.readlines()

notes = []

for line in lines:
	notes.append(int(line.rstrip("\n")))

def predicted_text_to_midi(predicted_notes_list):

	tick_length = 0.25

	###Class Definitions
	class Note:
		def __init__(self, time = 0, pitch = 0):
			self.duration = tick_length
			self.time = time
			self.pitch = pitch
		def add_dur(self):
			self.duration += tick_length

	###Function Definitions
	def add_note_to_track(track, note, mf):
		if not note.pitch == 0:	#pitch of 0 means no note is being played
			volume = 100
			channel = 0
			mf.addNote(track, channel, note.pitch, note.time, note.duration, volume)


	# create your MIDI object
	mf = MIDIFile(1)     # 4 tracks

	time = 0    # start at the beginning
	beats_per_minute = 120

	mf.addTrackName(0, time, "Track 1")
	mf.addTempo(0, time, beats_per_minute)

	#initialize a list which stores notes, and only adds them to the midi after the full duration is known
	note_storage = Note()

	i = 0
	for line in predicted_notes_list:
		i += 1
		track_pitch = int(line)
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
	with open("results/" + "predicted_" + file_name.split('/')[1].split('.')[0] + ".mid", 'wb') as outf:
		mf.writeFile(outf)
		outf.close()



def window_based_linear_regression(window_size, notes_list, predictions) :
	print (len(notes_list))

	for predictions in range(0, predictions):

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
				y_dataset.append(notes_list[i+(window_size)])
	
	
		model = LinearRegression().fit(X_dataset, y_dataset)

		print(cross_val_score(model, X_dataset, y_dataset, cv=10).mean())

		predicted_note = int(model.predict([X_dataset[-1]]))

		if predicted_note < 0 :
			predicted_note = 0

		print (predicted_note)

		notes_list.append(predicted_note)

	print (len(notes_list))

	with open("results/" + "predicted_" + file_name.split('/')[1].split('.')[0] + ".txt", "w") as filehandle:
		filehandle.write("\n".join(str(note) for note in notes_list))
	
	return notes_list



predicted_notes_list = window_based_linear_regression(20, notes, 100)

predicted_text_to_midi(predicted_notes_list)

