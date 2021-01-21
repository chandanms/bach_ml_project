

def representation_output(notes_list):

    # Get the max and min value without zero.
    min_p = min(list(filter(lambda a: a != 0, notes_list)))
    max_p = max(list(filter(lambda a: a != 0, notes_list)))

    output_length = 1 + (max_p - min_p + 1) + 1
    output = []
    stored_note = None

    for midi_note in notes_list:
        vector = [0] * output_length
        # When a rest, make the first entry equal to 1
        # If midi_note is repeated add duration by 1
        # New midi_note add a new row to the vector
        if midi_note == 0:
            vector[0] = 1
        elif stored_note is None or stored_note is not midi_note:
            vector[(midi_note - min_p + 1)] = 1
            vector[output_length - 1] = 1
            stored_note = midi_note
        else:
            vector[output_length - 1] += 1

        output.append(vector)

    return output



