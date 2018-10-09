# Bitwig OSC Python3
A Python3 client library for the Moss OSC Bitwig extension API.

Bitwig ( https://www.bitwig.com ) is a commercial multi-platform digital audio workstation or DAW. Open Sound Control or OSC ( http://opensoundcontrol.org/introduction-osc ) is a protocol for controlling DAWs and other things. Bitwig doesn't currently support OSC, but a community member named Jürgen Moßgraber ( http://www.mossgrabers.de/Software/Bitwig/Bitwig.html ) has made a Bitwig extension which adds OSC support to Bitwig.

This library aims to provide a high-level abstraction for the Moss OSC Bitwig API, which can be used to control Bitwig with Python3.

Here is the current OSC API for Bitwig, it can do a lot!:
https://github.com/git-moss/DrivenByMoss/wiki/Open-Sound-Control-(OSC)
  
  
Getting Started:

Download Bitwig Studio and install it (there is a free demo version, or you can buy it):
https://www.bitwig.com/en/download.html

Download the Moss Bitwig extension from here:
http://www.mossgrabers.de/Software/Bitwig/Bitwig.html

These are the installation instructions for the Moss Bitwig extension, make sure to follow these before continuing:
https://github.com/git-moss/DrivenByMoss/wiki/Installation#basic-installation
and
https://github.com/git-moss/DrivenByMoss/wiki/Installation#open-sound-control-osc-specifics

Install Python3 from your distribution's package manager, or from here:
https://www.python.org/downloads/

Install the Python3 dependencies:
```
pip install python-osc
```

Install git if you don't have it yet, either from your distribution's package manager, or from here:
https://git-scm.com/downloads

Clone this git repository:
```
git clone https://github.com/defcronyke/bitwig-osc-python3.git
cd bitwig-osc-python3
```

Open Bitwig, activate the Moss OSC extension by adding it in the Controllers section and making sure it's turned on, then load the Bitwig project found in:
bitwig-projects/examples-and-tests/examples-and-tests.bwproject

With the Bitwig project running along with the Moss OSC extension, you can now try running some of the tests or examples with Python. You will want to turn on your speakers or headphones for this:

```
# Test the MIDI play features.
python tests/test_receive_play.py

# Run an example program which allows you to optionally specify a remote OSC 
# server IP and port, as well as an optional default MIDI channel to send all 
# notes on.
python examples/play_midi_notes.py --ip 127.0.0.1 --port 8000 --chan 1
```

Take a look in the tests/ folder if you are curious about various functions' intended uses, and check out the examples/ folder for some complete example programs which use this Python library to control Bitwig.

Later on, if you'd like to update to the newest version of this library, you can pull the latest changes:
```
git pull
```

Now let's all control Bitwig in interesting programmatic ways and see what comes of it! Enjoy, and feel free to leave a bug report if you have any issues with this library.

This project is not affiliated with Bitwig or Jürgen Moßgraber.
