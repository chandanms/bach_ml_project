from represe


note_text_file_name = "dataset/2.txt"

note_text_file = open(note_text_file_name, "r")
notes_list = []

for note in note_text_file:
    notes_list.append(int(note))

train = int(round(0.7 * len(notes_list)))

train_data = representation_input(notes_list[:train])
test_data = representation_output(notes_list[train:])

alpha = 0.99

model = Ridge(alpha=alpha).fit(train_data, test_data)

