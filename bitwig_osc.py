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
        """ Set the OSC server's IP and port while instantiating the OSC 
            client, and set the default MIDI channel to use. """
        signal.signal(signal.SIGINT, self.signal_handler)

        # Save some vars for later.
        self.ip = ip        # The OSC server IP.
        self.port = port    # The OSC server port.
        self.chan = chan    # The default MIDI channel to send on.
        self.notes_on = {}  # The notes that are currently on.
        self.last_note = 0  # The last note that was played.

        # Instantiate an OSC UDP client.
        self.client = udp_client.SimpleUDPClient(ip, port)

    def __del__(self):
        """ Cleanup when object is destroyed. """
        # Stop all the notes that are currently playing.
        self.stop_all_playing_notes()
        self.stop_all_playing_notes("drum")

    # --- Receive - Track ---
    # API Route: /{track|master}
    # https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)#receive---track

    def record_arm_track(self, track=1, arm=1):
        """ Arm a track for recording. This also affects which MIDI tracks 
            are used for real-time playback. Set arm to 0 to disarm a 
            track, or None to toggle the armed status.
            API route: /track/{1-8}/recarm {1,0,-} """
        # Send the record arm message to the OSC server.
        self.client.send_message(
            "/track/" + str(track) + "/recarm", arm)

    def record_disarm_track(self, track=1):
        """ Disarm a track for recording. This also affects which MIDI tracks 
            are used for real-time playback. This is a shortcut for calling 
            record_arm_track(track, 0). """
        # Send the record arm message to the OSC server.
        self.record_arm_track(track, 0)

    def record_disarm_first_eight_tracks(self):
        """ Disarm the first eight tracks for recording. """
        for i in range(8):
            self.record_disarm_track(i+1)

    def record_arm_toggle_track(self, track=1):
        """ Toggle the armed status of a track for recording. This also 
            affects which MIDI tracks are used for real-time playback. 
            This is a shortcut for calling record_arm_track(track, None). """
        # Send the record arm message to the OSC server.
        self.record_arm_track(track, None)

    # --- End Receive - Track ---

    # --- Receive - Play ---
    # API Route: /vkb_midi
    # https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)#receive---play

    def play_note(self, note=60, vel=127, typ="note", chan=None):
        """ Play Bitwig virtual MIDI keyboard using OSC. Defaults to playing 
            Middle C (C2) at full velocity. Pass in "drum" for the typ param if
            you want to play drums.
            API route: /vkb_midi/{Channel:0-16}/{note|drum}/{Note:0-127} {Velocity:0-127} """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # If we are sending a note velocity larger than 0, set the note as on
        # in our records.
        if vel > 0:
            self.notes_on[note] = True

        # Otherwise set the note as off in our records.
        else:
            self.notes_on.pop(note, None)

        # Save this note so we can keep track of the most recent note played.
        self.last_note = note

        # Send the note message to the OSC server.
        self.client.send_message(
            "/vkb_midi/" + str(chan) + "/" + typ + "/" + str(note), vel)

    def stop_note(self, note=60, typ="note", chan=None):
        """ Stop a note by setting its velocity to zero. This is a shortcut 
            for calling play_note(note, 0). Pass in "drum" for the typ
            param if you want to stop a drum note. """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Set the note as off in our records.
        self.notes_on.pop(note, None)

        # Send the note message to the OSC server to turn off the note.
        self.client.send_message("/vkb_midi/" + str(chan) +
                                 "/" + typ + "/" + str(note), 0)

    def stop_all_playing_notes(self, typ="note", chan=None):
        """ Send velocity 0 to all notes that are currently playing, to turn 
            them off. Pass in "drum" as the typ param if you want to stop all 
            the drum notes that are currently playing. This is being used as 
            a trap function that runs when you press ctrl-c, so there aren't 
            any lingering notes when the program exits. """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Stop all the notes that are currently playing.
        for note in list(self.notes_on):
            self.stop_note(note, typ, chan)

    def stop_all_notes(self, typ="note", chan=None):
        """ Send velocity 0 to all notes, to turn them off. Pass in "drum"
            as the typ param if you want to turn off drum notes. """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        for note in range(128):
            self.stop_note(note, typ, chan)

    def octave_up(self, typ="note", chan=None):
        """ Permanently shift all notes up by eight. Pass in "drum" for the
            typ param if you want to shift the octave of the drums.
            API route: /vkb_midi/{Channel:0-16}/{note|drum}/+ """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Send the note message to the OSC server to make all future note
        # plays be an octave higher than they should be.
        self.client.send_message(
            "/vkb_midi/" + str(chan) + "/" + typ + "/+", 1)

    def octave_down(self, typ="note", chan=None):
        """ Permanently shift all notes down by eight. Pass in "drum" for the
            typ param if you want to shift the octave of the drums.
            API route: /vkb_midi/{Channel:0-16}/{note|drum}/- """
        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Send the note message to the OSC server to make all future note
        # plays be an octave lower than they should be.
        self.client.send_message(
            "/vkb_midi/" + str(chan) + "/" + typ + "/-", 1)

    # --- End Receive - Play ---

    def signal_handler(self, sig, frame):
        """ This runs when you press ctrl-c to stop the program. """
        print('You pressed ctrl-c. Turning off all notes and quitting...')

        # Stop all the notes that are currently playing.
        self.stop_all_playing_notes()
        self.stop_all_playing_notes("drum")

        # Exit the program indicating no error.
        sys.exit(0)
