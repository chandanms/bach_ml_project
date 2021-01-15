import numpy as np
from sklearn.linear_model import LinearRegression

from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedKFold



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


def window_based_ridge_regression(window_size, notes_list, predictions) :

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
				y_dataset.append(notes_list[i+(window_size)][0])

	X_dataset = np.array(X_dataset)
	
	nsamples, nx, ny = X_dataset.shape

	X_dataset = X_dataset.reshape((nsamples,nx*ny))

	model = Ridge()

	cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

	grid = dict()
	
	grid['alpha'] = np.arange(0, 1, 0.01)
	
	# define search
	search = GridSearchCV(model, grid, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)

	results = search.fit(X_dataset, y_dataset)

	# summarize
	print('MAE: %.3f' % results.best_score_)
	print('Config: %s' % results.best_params_)





note_text_file_name = "dataset/2.txt"

representation_list = noteToRepresentation(note_text_file_name)

window_based_ridge_regression(5, representation_list, 5)



