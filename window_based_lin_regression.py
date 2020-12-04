
file_name = "dataset/4.txt"


f = open(file_name)

lines = f.readlines()

notes = []

for line in lines:
	notes.append(int(line.rstrip("\n")))

def window_based_linear_regression(window_size, notes_list) :

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


window_based_linear_regression(2, notes)