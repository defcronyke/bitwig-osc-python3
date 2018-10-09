# Bitwig OSC Python3
A Python3 client library for the Moss OSC Bitwig extension API.

Bitwig ( https://www.bitwig.com ) is a commercial multi-platform digital audio workstation or DAW. OSC or Open Sound Control ( http://opensoundcontrol.org/introduction-osc ) is a protocol for controlling DAWs and other things. Bitwig doesn't currently support OSC, but a community member has made a Bitwig extension which adds OSC support to Bitwig.

This library aims to provide a high-level abstraction for the Moss OSC Bitwig API, which can be used to control Bitwig with Python3.

Here is the current OSC API for Bitwig, it can do a lot!: https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)

Download the Moss Bitwig extension from here: http://www.mossgrabers.de/Software/Bitwig/Bitwig.html

These are the installation instructions for the Moss Bitwig extension: https://github.com/git-moss/DrivenByMoss/wiki/Installation#basic-installation

Python3 dependencies:
```
pip install python-osc
```

To get started, clone this git repo:
```
git clone https://github.com/defcronyke/bitwig-osc-python3.git
cd bitwig-osc-python3
```

Next open Bitwig, activate the Moss OSC extension by adding it in the Controllers section and making sure it's turned on, then load the Bitwig project found in: projects/examples-and-tests/examples-and-tests.bwproject

With that running, you can now try running some of the tests or examples with Python:

```
# Test the MIDI play features.
python tests/test_receive_play.py

# Run an example program which allows you to optionally specify a remote OSC 
# server IP and port, as well as an optional default MIDI channel to send all 
# notes on.
python examples/play_midi_notes.py --ip 127.0.0.1 --port 8000 --chan 1
```

This project is not affiliated with Bitwig or Moss.
