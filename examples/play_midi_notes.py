""" Example of how to play MIDI notes, by Daphne Volante 2018

    This example requires a MIDI synth loaded into Bitwig with all the keys 
    assigned, in track 1. There is an example Bitwig project in the 
    bitwig-projects/ folder which fits this criteria. """

# Add one directory level up to the Python module search path.
# Only needed if your Python file is in a subdirectory.
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# Import the Moss Bitwig OSC API client library, and some other stuff.
from bitwig_osc import BitwigOSC
import argparse
import time


def run(bw):
    """ This is where we use the BitwigOSC instance to send our OSC 
        messages. """
    # Record disarm the tracks to get a good initial state.
    bw.record_disarm_first_eight_tracks()

    # Record arm the first track.
    bw.record_arm_track()

    note = 15   # The note to start on.
    asc = True  # Start ascending.
    n = 100

    # Loop n times.
    for _ in range(n):
        note1 = 0   # The first note to play next.
        note2 = 0   # The second note to play next.

        # If we reach the top, start descending.
        if asc and note >= 88:
            asc = False

        # If we reach the bottom, start ascending.
        elif not asc and note <= 14:
            asc = True

        # If we are ascending.
        if asc:
            note += 5
            note1 = note
            note -= 3
            note2 = note

        # If we are descending.
        else:
            note -= 5
            note1 = note
            note += 3
            note2 = note

        # Play the first note.
        bw.play_note(note1)
        time.sleep(0.1)
        bw.stop_note(note1)
        time.sleep(0.1)

        # Play the second note.
        bw.play_note(note2)
        time.sleep(0.1)
        bw.stop_note(note2)
        time.sleep(0.1)

    bw.record_disarm_track()


# We want to accept some arguments from the command line.
parser = argparse.ArgumentParser()

# OSC Server IP.
parser.add_argument("--ip", default="127.0.0.1",
                    help="The IP of the OSC server.")

# OSC Server port.
parser.add_argument("--port", type=int, default=8000,
                    help="The port the OSC server is listening on.")

# Default MIDI channel to use.
parser.add_argument("--chan", type=int, default=1,
                    help="The default MIDI channel to send all commands to.")
args = parser.parse_args()

# Instantiate our Bitwig OSC client library with the command line arguments.
bw = BitwigOSC(args.ip, args.port, args.chan)

# Run the main routine.
run(bw)
