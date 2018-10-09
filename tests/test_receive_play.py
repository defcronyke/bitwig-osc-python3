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
        cls.bw = BitwigOSC()

    def test_play(self):
        """ A medium-velocity rising sweep, using play_note() and 
            stop_note(). """
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

    def test_octave(self):
        """ Play the same note a few times, switching octaves with 
            octave_up() and octave_down(). """
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


def main():
    unittest.main()


if __name__ == "__main__":
    main()
