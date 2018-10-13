""" Bitwig OSC Python3 by Jeremy Carter <Jeremy@JeremyCarter.ca> 2018.

    Based on the Bitwig 2.4 OSC API by Moss. """

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
        self.ip = ip              # The OSC server IP.
        self.port = port          # The OSC server port.
        self.chan = chan          # The default MIDI channel to send on.
        self.synth_notes_on = {}  # The notes that are currently on.
        self.drum_notes_on = {}   # The notes that are currently on.
        self.last_note = 0        # The last note that was played.

        # Instantiate an OSC UDP client.
        self.client = udp_client.SimpleUDPClient(ip, port)

    def __del__(self):
        """ Cleanup when object is destroyed. """

        # Stop all the notes that are currently playing.
        self.stop_all_playing_notes()
        self.stop_all_playing_notes("drum")

    # --- Receive - Global ---
    # API route: /
    # https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)#receive---global

    def preroll(self, bars=0):
        """ Set the preroll, which is the number of bars to wait before 
            recording when recording is triggered. The bars param can be
            0, 1, 2, or 4.

            API route: /preroll {0, 1, 2, 4} """

        # Send the preroll message to the OSC server.
        self.client.send_message("/preroll", bars)

    def undo(self):
        """ Undo the last action.

            API route: /undo - """

        # Send the undo message to the OSC server.
        self.client.send_message("/undo", None)

    def redo(self):
        """ Redo the last action that was undone. 

            API route: /redo - """

        # Send the redo message to the OSC server.
        self.client.send_message("/redo", None)

    # --- End Receive - Global ---

    # --- Receive - Project ---
    # API route: /project
    # https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)#receive---project

    def next_project(self):
        """ Switch to the next opened project. 

            API route: /project/+ - """

        # Send the next project message to the OSC server.
        self.client.send_message("/project/+", None)

    def previous_project(self):
        """ Switch to the previous opened project.

            API route: /project/- - """

        # Send the previous project message to the OSC server.
        self.client.send_message("/project/-", None)

    def activate_audio_engine(self):
        """ Activate the audio engine.

            API route: /project/engine 1 """

        # Send the activate engine message to the OSC server.
        self.client.send_message("/project/engine", 1)

    def deactivate_audio_engine(self):
        """ Deactivate the audio engine.

            API route: /project/engine 0 """

        # Send the deactivate engine message to the OSC server.
        self.client.send_message("/project/engine", 0)

    def toggle_audio_engine(self):
        """ Toggle the audio engine between active and inactive.

            API route: /project/engine - """

        # Send the toggle engine message to the OSC server.
        self.client.send_message("/project/engine", None)

    def save(self):
        """ Save the current project. 

            API route: /project/save - """

        # Send the save message to the OSC server.
        self.client.send_message("/project/save", None)

    # --- End Receive - Project ---

    # --- Receive - Transport ---

    def stop(self):
        """ Stop the transport.

            API route: /stop {1,-} """

        # Send the stop message to the OSC server.
        self.client.send_message("/stop", 1)

    def play(self):
        """ Play.

            API route: /play {1,-} """

        # Send the play message to the OSC server.
        self.client.send_message("/play", 1)

    def restart(self):
        """ Restart.

            API route: /restart {1,-} """

        # Send the restart message to the OSC server.
        self.client.send_message("/restart", 1)

    def repeat(self):
        """ Repeat.

            API route: /repeat {1,-} """

        # Send the repeat message to the OSC server.
        self.client.send_message("/repeat", 1)

    def click(self):
        """ Enable click.

            API route: /click 1 """

        # Send the enable click message to the OSC server.
        self.client.send_message("/click", 1)

    def toggle_click(self):
        """ Toggle click.

            API route: /click - """

        # Send the toggle click message to the OSC server.
        self.client.send_message("/click", None)

    def click_volume(self):
        """ Click volume.

            API route: /click/volume - """

        # Send the click volume message to the OSC server.
        self.client.send_message("/click/volume", None)

    def toggle_click_preroll(self):
        """ Toggle click in preroll.

            API route: /click/preroll {1, -} """

        # Send the toggle click preroll message to the OSC server.
        self.client.send_message("/click/preroll", 1)

    def punch_in(self):
        """ Punch in.

            API route: /punchIn {1, -} """

        # Send the punch in message to the OSC server.
        self.client.send_message("/punchIn", 1)

    def punch_out(self):
        """ Punch out.

            API route: /punchOut {1, -} """

        # Send the punch out message to the OSC server.
        self.client.send_message("/punchOut", 1)

    def record(self):
        """ Record.

            API route: /record {1, -} """

        # Send the record message to the OSC server.
        self.client.send_message("/record", 1)

    def overdub(self):
        """ Overdub.

            API route: /overdub {1, -} """

        # Send the overdub message to the OSC server.
        self.client.send_message("/overdub", 1)

    def overdub_launcher(self):
        """ Overdub launcher.

            API route: /overdub/launcher {1, -} """

        # Send the overdub launcher message to the OSC server.
        self.client.send_message("/overdub/launcher", 1)

    def crossfade(self, n):
        """ Crossfade with the value from the n param.

            API route: /crossfade {0-127} """

        # Send the crossfade message to the OSC server.
        self.client.send_message("/crossfade", n)

    def autowrite(self, enable=1):
        """ Autowrite. Pass 0 as the enable param to disable.

            API route: /autowrite {0, 1} """

        # Send the autowrite message to the OSC server.
        self.client.send_message("/autowrite", enable)

    def autowrite_launcher(self, enable=1):
        """ Autowrite launcher. Pass 0 as the enable param to disable.

            API route: /autowrite/launcher {0, 1} """

        # Send the autowrite launcher message to the OSC server.
        self.client.send_message("/autowrite/launcher", enable)

    def automation_write_mode(self, mode="latch"):
        """ Automation write mode. The mode param can be "latch", "touch",
            or "write".

            API route: /automationWriteMode {latch, touch, write} """

        # Send the automation write mode message to the OSC server.
        self.client.send_message("/automationWriteMode", mode)

    def raw_tempo(self, n=0):
        """ Set raw tempo with the n param.

            API route: /tempo/raw {0-666} """

        # Send the raw tempo message to the OSC server.
        self.client.send_message("/tempo/raw", n)

    def tap_tempo(self):
        """ Tap the tempo.

            API route: /tempo/tap - """

        # Send the tap tempo message to the OSC server.
        self.client.send_message("/tempo/tap", None)

    def increase_position_small(self):
        """ Increase the play position a bit.

            API route: /position/+ - """

        # Send the increase position small message to the OSC server.
        self.client.send_message("/position/+", None)

    def decrease_position_small(self):
        """ Decrease the play position a bit.

            API route: /position/- - """

        # Send the decrease position small message to the OSC server.
        self.client.send_message("/position/-", None)

    def increase_position_large(self):
        """ Increase the play position a lot.

            API route: /position/++ - """

        # Send the increase position large message to the OSC server.
        self.client.send_message("/position/++", None)

    def decrease_position_large(self):
        """ Decrease the play position a lot.

            API route: /position/-- - """

        # Send the decrease position large message to the OSC server.
        self.client.send_message("/position/--", None)

    def move_position(self, n=1):
        """ Move the play position by the n param.
            If n is -1, or 1, move by a small amount.
            Move by a large amount for any other values.

            API route: /position {-2, -1, 1, 2} """

        # Send the move position large message to the OSC server.
        self.client.send_message("/position", n)

    # --- End Receive - Transport ---

    # --- Receive - Track ---
    # API route: /{track|master}
    # https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)#receive---track

    def record_arm_track(self, track=1, arm=1):
        """ Arm a track for recording. This also affects which MIDI tracks 
            are used for real-time playback. Set arm to 0 to disarm a 
            track, or None to toggle the armed status.

            API route: /track/{1-8}/recarm {0, 1} """

        # Send the record arm message to the OSC server.
        self.client.send_message(
            "/track/" + str(track) + "/recarm", arm)

    def record_disarm_track(self, track=1):
        """ Disarm a track for recording. This also affects which MIDI tracks 
            are used for real-time playback. This is a shortcut for calling 
            record_arm_track(track, 0). 

            API route: /track/{1-8}/recarm 0 """

        # Send the record arm message to the OSC server.
        self.record_arm_track(track, 0)

    def record_disarm_first_eight_tracks(self):
        """ Disarm the first eight tracks for recording. """

        for i in range(8):
            self.record_disarm_track(i+1)

    def toggle_record_arm_track(self, track=1):
        """ Toggle the armed status of a track for recording. This also 
            affects which MIDI tracks are used for real-time playback. 
            This is a shortcut for calling record_arm_track(track, None).

            API route: /track/{1-8}/recarm - """

        # Send the record arm message to the OSC server.
        self.record_arm_track(track, None)

    # --- End Receive - Track ---

    # --- Receive - Play ---
    # API route: /vkb_midi
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
            if typ == "note":
                self.synth_notes_on[note] = True
            else:
                self.drum_notes_on[note] = True

        # Otherwise set the note as off in our records.
        else:
            if typ == "note":
                self.synth_notes_on.pop(note, None)
            else:
                self.drum_notes_on.pop(note, None)

        # Save this note so we can keep track of the most recent note played.
        self.last_note = note

        # Send the note message to the OSC server.
        self.client.send_message(
            "/vkb_midi/" + str(chan) + "/" + typ + "/" + str(note), vel)

    def stop_note(self, note=60, typ="note", chan=None):
        """ Stop a note by setting its velocity to zero. This is a shortcut 
            for calling play_note(note, 0). Pass in "drum" for the typ
            param if you want to stop a drum note, and "both" if you want
            to stop any kind of note.

            API route: /vkb_midi/{Channel:0-16}/{note|drum}/{Note:0-127} 0 """

        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Set the note as off in our records.
        if typ == "note" or typ == "both":
            self.synth_notes_on.pop(note, None)
            # Send the note message to the OSC server to turn off the note.
            self.client.send_message("/vkb_midi/" + str(chan) +
                                     "/note/" + str(note), 0)
        if typ == "drum" or typ == "both":
            self.drum_notes_on.pop(note, None)
            # Send the note message to the OSC server to turn off the note.
            self.client.send_message("/vkb_midi/" + str(chan) +
                                     "/drum/" + str(note), 0)

    def stop_all_playing_notes(self, typ="note", chan=None):
        """ Send velocity 0 to all notes that are currently playing, to turn 
            them off. Pass in "drum" as the typ param if you want to stop all 
            the drum notes that are currently playing, pass "both" to stop 
            all types of notes. This is being used as a trap function that 
            runs when you press ctrl-c, so there aren't any lingering notes 
            when the program exits. """

        # Use default MIDI channel if chan argument not specified.
        if chan == None:
            chan = self.chan

        # Stop all the notes that are currently playing.
        if typ == "note" or typ == "both":
            for note in list(self.synth_notes_on):
                self.stop_note(note, typ, chan)
        if typ == "drum" or typ == "both":
            for note in list(self.drum_notes_on):
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

            API route: /vkb_midi/{Channel:0-16}/{note|drum}/+ 1 """

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

            API route: /vkb_midi/{Channel:0-16}/{note|drum}/- 1 """

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
