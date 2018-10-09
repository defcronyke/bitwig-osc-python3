""" Bitwig OSC Python3 by Jeremy Carter <Jeremy@JeremyCarter.ca> 2018 """
from pythonosc import osc_message_builder
from pythonosc import udp_client
import signal
import sys


class BitwigOSC:
    """ A client library for the Moss Bitwig OSC API, to control Bitwig with 
        the Open Sound Control protocol.

        API: https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC) """

    def __init__(self, ip="127.0.0.1", port=8000, chan=1):
        """ Set the OSC server's IP and port while instantiating the OSC client, 
            and set the default MIDI channel to use. """
        signal.signal(signal.SIGINT, self.signal_handler)

        # Save some vars for later.
        self.ip = ip        # The OSC server IP.
        self.port = port    # The OSC server port.
        self.chan = chan    # The default MIDI channel to send on.
        self.notes_on = {}  # The notes that are currently on.

        # Instantiate an OSC UDP client.
        self.client = udp_client.SimpleUDPClient(ip, port)

    def __del__(self):
        """ Cleanup when object is destroyed. """
        # Stop all the notes that are currently playing.
        self.stop_all_notes()

    def play_note(self, note, vel, chan=None):
        """ Play Bitwig virtual MIDI keyboard using OSC
            API route: /vkb_midi/{Channel:0-16}/note/{Note:0-127} {Velocity:0-127} """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # If we are sending a note velocity larger than 0, set the note as on
        # in our records.
        if vel > 0:
            self.notes_on[note] = True

        # Otherwise set the note as off in our records.
        else:
            del self.notes_on[note]

        # Send the note message to the OSC server.
        self.client.send_message("/vkb_midi/" + str(chan) +
                                 "/note/" + str(note), vel)

    def stop_note(self, note, chan=None):
        """ Stop a note by setting its velocity to zero. """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Set the note as off in our records.
        del self.notes_on[note]

        # Send the note message to the OSC server to turn off the note.
        self.client.send_message("/vkb_midi/" + str(chan) +
                                 "/note/" + str(note), 0)

    def stop_all_notes(self, chan=None):
        """ Send velocity 0 to all notes that are currently playing, to turn them off. 
            This is being used as a trap function that runs when you press ctrl-c, 
            so there aren't any lingering notes when the program exits. """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Stop all the notes that are currently playing.
        for note in list(self.notes_on):
            self.stop_note(note, chan)

    def signal_handler(self, sig, frame):
        """ This runs when you press ctrl-c to stop the program. """
        print('You pressed ctrl-c. Turning off all notes and quitting...')

        # Stop all the notes that are currently playing.
        self.stop_all_notes()

        # Exit the program indicating no error.
        sys.exit(0)
