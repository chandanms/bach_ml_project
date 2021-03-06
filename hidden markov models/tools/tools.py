from audiolazy import freq2midi
from midiutil.MidiFile import MIDIFile
import numpy as np
from itertools import groupby
from collections import defaultdict

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


def pdf_of_occurences_each_note():
	
	dataset_path = "dataset/"

	text_file_list = ["1.txt", "2.txt", "3.txt", "4.txt"]

	notes_list = []

	for text_file in text_file_list:

		note_text_file = open(dataset_path + text_file, "r")

		for note in note_text_file:
			notes_list.append(int(note))

	groups = groupby(notes_list)

	result = [(label, sum(1 for _ in group)) for label, group in groups]

	analysis_dict = defaultdict(list)


	for label, count in result:

		if label == 0:
			if count < 20:
				analysis_dict[label].append(count)
		else :
			analysis_dict[label].append(count)

	return analysis_dict



def get_occurence(note_pdf_dict, predicted_note):

    occurances = np.random.choice(note_pdf_dict[predicted_note])

    return occurances


def get_unique_note_list():

	note_text_file_name = "dataset/F.txt"

	line_list = []

	with open(note_text_file_name, "r") as f:
		lines = f.readlines()

		for col in range(0, 4) :
			for x in lines:
				line_list.append(int(x.rstrip("\n").split('\t')[col]))
	f.close()

	return (list(set(line_list)))