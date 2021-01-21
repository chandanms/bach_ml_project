import math


def representation_input(notes_list):

    # Remove all zero values, i.e. rests
    notes_list = list(filter(lambda a: a != 0, notes_list))

    # min and max note that are trained in the network
    min_p = 2 * math.log(2 ** (min(notes_list) - 69) / 12 * 440, 2)
    max_p = 2 * math.log(2 ** (max(notes_list) - 69) / 12 * 440, 2)

    # chroma contains the position of each note in the chroma circle
    # 1 indicates the first note in the chroma circle, in this case G
    chroma = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    radius_chroma = 1

    # c5 contains the position of each note in the circle of fifths
    c5 = [1, 8, 3, 10, 5, 12, 7, 2, 9, 4, 11, 6]
    radius_c5 = 1

    representation = []
    stored_note = None
    idx = -1

    for midi_note in notes_list:

        # if note has not been stored or midi note is not identical to stored note
        if stored_note is None or stored_note is not midi_note:
            # Change the stored note to the current midi note
            stored_note = midi_note
            idx += 1

            # Perform calculations
            note = (midi_note - 55) % 12
            # find the angle in the chroma circle and circle of fifths
            chroma_angle = (chroma[note] - 1) * (360 / 12)
            c5_angle = (c5[note] - 1) * (360 / 12)

            # compute the (x,y) coordinates for the chroma circle and circle of fifths
            # sin stands for sin in degrees
            chroma_x = radius_chroma * math.sin(chroma_angle)
            chroma_y = radius_chroma * math.cos(chroma_angle)
            c5_x = radius_c5 * math.sin(c5_angle)
            c5_y = radius_c5 * math.cos(c5_angle)

            # n is the distance (in semitones) of midi_note from A4 (69 in MIDI),
            # whose frequency os 440 Hz. fx is the frequency of the note
            n = midi_note - 69
            fx = 2 ** (n / 12) * 440

            # the representation of pitch is scaled in such a way that a pitch
            # distance of 1 octave in the first dimension, is equal to the distance of
            # notes on the opposite sides on the chroma circle or the circle of fifths
            pitch = 2 * math.log(fx, 2) - max_p + (max_p - min_p) / 2

            # y is the 5-dimensional representation of midi_note with duration 1
            y = [pitch, chroma_x, chroma_y, c5_x, c5_y, 1]
            # Add y vector to representation
            representation.append(y)

        # if we the same note
        else:
            # Increment the duration of the note
            representation[idx][5] += 1

    return representation
