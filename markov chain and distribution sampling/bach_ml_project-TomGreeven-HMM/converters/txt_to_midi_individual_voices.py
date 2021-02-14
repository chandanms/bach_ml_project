from midiutil.MidiFile import MIDIFile

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

###Main file##################################################################################



text_file_list = ["1.txt", "2.txt", "3.txt", "4.txt"]

for audio_file_name, text_file_name in enumerate(text_file_list):

	# create your MIDI object
	mf = MIDIFile(1)     # 4 tracks

	time = 0    # start at the beginning
	beats_per_minute = 120

	mf.addTrackName(0, time, "Track 1")
	mf.addTempo(0, time, beats_per_minute)

	#initialize a list which stores notes, and only adds them to the midi after the full duration is known
	note_storage = Note()

	text_file = open("../dataset/" + text_file_name, "r")
	max_iter = 1000
	i = 0
	for line in text_file:
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
		if i >= max_iter:
			break

	#After text file ends, add the remaining notes
	add_note_to_track(0, note_storage, mf)

	# write it to disk
	with open(str(audio_file_name + 1) + ".mid", 'wb') as outf:
		mf.writeFile(outf)

