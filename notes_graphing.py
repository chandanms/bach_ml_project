import seaborn as sns
sns.set_theme()

import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt


def text_to_list(notes_text_file_name):

	note_text_file = open("dataset/" + note_text_file_name, "r")

	notes_list = []

	for i, note in enumerate(note_text_file):

		notes_list.append(int(note))

	return notes_list

note_text_files = ["1.txt", "2.txt", "3.txt", "4.txt"]


for i, note_text_file_name in enumerate(note_text_files) :

	notes_list = text_to_list(note_text_file_name)

	if i == 0:
		notes_list_1 = notes_list
	elif i == 1:
		notes_list_2 = notes_list
	elif i ==2 :
		notes_list_3 = notes_list
	else :
		notes_list_4 = notes_list


x_axis = np.arange(0, len(notes_list_1)+1, 0.25)

dataframe_list = [x_axis, notes_list_1, notes_list_2, notes_list_3, notes_list_4]

df = DataFrame(dataframe_list).transpose()

df.columns = ["time", "notes_1", "notes_2", "notes_3", "notes_4"]

df = df.set_index("time")


sns.lineplot(data=df)

plt.show()








