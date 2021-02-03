

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
    print(len(notes_list))

    output_length = 1 + (max_p - min_p + 1) + 1

    output = []
    stored_note = None
    idx = -1

    for midi_note in notes_list:
        vector = [0] * output_length
        # When a rest, make the first entry equal to 1
        # If midi_note is repeated add duration by 1
        # New midi_note add a new row to the vector
        if midi_note == 0:
            idx += 1
            vector[0] = 1
            output.append(vector)
        elif stored_note is None or stored_note is not midi_note:
            print(midi_note)
            stored_note = midi_note
            idx += 1
            vector[(midi_note - min_p + 1)] = 1
            vector[output_length - 1] = 1
            output.append(vector)
        else:
            # Increment note by one
            output[idx][output_length - 1] += 1

    print(len(output))
    return output




