

def output_note_list(notes_list):
    # Get the max and min value without zero.
    min_p = min(list(filter(lambda a: a != 0, notes_list)))
    max_p = max(list(filter(lambda a: a != 0, notes_list)))

    # Generate a sequence which first element is zero note and the rest is the range of the notes like y is represented
    output_list = list(range(min_p, max_p + 1))
    output_list.insert(0, 0)

    return output_list


def representation_output(notes_list):
    # Get the max and min value without zero.
    min_p = min(list(filter(lambda a: a != 0, notes_list)))
    max_p = max(list(filter(lambda a: a != 0, notes_list)))

    # First element is rest, the rest is notes
    output_length = 1 + (max_p - min_p + 1)
    output = []

    for midi_note in notes_list:
        vector = [0] * output_length
        # When a rest, make the first entry equal to 1
        # New midi_note add a new row to the vector
        if midi_note == 0:
            vector[0] = 1
        else:
            vector[(midi_note - min_p + 1)] = 1

        output.append(vector)

    return output



