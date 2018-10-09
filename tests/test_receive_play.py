""" Bitwig OSC Python3 by Jeremy Carter <Jeremy@JeremyCarter.ca> 2018

    To prepare Bitwig for this test suite, you'll need to make a MIDI 
    Synth track for track 1 with a synth that has all the keys available, 
    and a MIDI Drum track for track 2 with a drumkit that has at least 
    two drums. All tracks should be record disarmed initially. There is
    an example Bitwig project in the bitwig-projects/ folder which fits 
    this criteria. """

# Add one directory level up to the Python module search path.
# Only needed if your Python file is in a subdirectory.
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# Import the Moss Bitwig OSC API client library, and some other stuff.
from bitwig_osc import BitwigOSC
import unittest
import time


class Note(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Instantiate the Moss Bitwig OSC client library.
        cls.bw = BitwigOSC()

        # Record disarm the tracks to get a good initial state.
        cls.bw.record_disarm_first_eight_tracks()

    def test_play(self):
        """ A medium-velocity rising sweep, using play_note() and 
            stop_note(). You'll need a synth with all the keys mapped,
            in track 1, to be able to hear this test. """
        # Record arm the appropriate track so we can hear it.
        self.bw.record_arm_track()

        # Loop over the range 0-128 exclusive. This is because
        # there are 127 MIDI notes available, and we want to play
        # ALL OF THEM!
        for i in range(128):
            # Turn the note on at velocity 50.
            self.bw.play_note(i, 50)

            # Sustain the note for 5 hundredths of a second.
            time.sleep(0.05)

            # Turn the note off. This function is a shortcut for
            # calling play_note(i, 0).
            self.bw.stop_note(i)

        # Record disarm the appropriate track so we can't hear it anymore.
        self.bw.record_disarm_track()

    def test_play_drum(self):
        """ Play the first two drums in a drumkit, using play_note() and 
            stop_note(). You'll need a record armed MIDI drumkit with at 
            least two drums loaded in track 2, to be able to hear this 
            test. """
        # Record arm the appropriate track so we can hear it.
        self.bw.record_arm_track(2)

        # Loop over the range 0-2 exclusive. This is because
        # we want to play 2 drums.
        for i in range(20):
            # Choose drum 1 or 2, based on the iteration counter.
            # Most drumkits in Bitwig start at C1 (Note 36).
            first_drum = 36
            drum = i % 2 + first_drum

            # Turn the note on at velocity 127.
            self.bw.play_note(drum, 127, "drum")

            # Sustain the note for 5 hundredths of a second.
            time.sleep(0.2)

            # Turn the note off. This function is a shortcut for
            # calling play_note(i, 0).
            self.bw.stop_note(drum, "drum")

        # Record disarm the appropriate track so we can't hear it anymore.
        self.bw.record_disarm_track(2)

    def test_octave(self):
        """ Play the same note a few times, switching octaves with 
            octave_up() and octave_down(). You'll need a synth with
            sound on C2 and C1, record armed, to be able to hear this 
            test."""
        # Record arm the appropriate track so we can hear it.
        self.bw.record_arm_track()

        # Middle C.
        self.bw.play_note()
        time.sleep(0.5)

        # Stop the note before shifting octaves, because the change
        # won't take effect for notes that are currently playing.
        self.bw.stop_note()

        # Shift down by one octave.
        self.bw.octave_down()

        # Play C1 even though we are sending the MIDI note for C2.
        self.bw.play_note()
        time.sleep(0.5)
        self.bw.stop_note()

        # Set the octave back to what it should be, since this
        # change is permanent.
        self.bw.octave_up()
        self.bw.play_note()
        time.sleep(0.5)
        self.bw.stop_note()

        # Record disarm the appropriate track so we can't hear it anymore.
        self.bw.record_disarm_track()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
