**MonopoLOL**
Simple auction-style timer in python

*Dependencies*:
	- Linux, directions assume Debian or derivatives (Ubuntu)
		* python3-dev
		* libevent2-dev
		* libstreamer1.0-dev
	- Python 3, with the following libraries:
		* evdev
		* simpleaudio
	```shell
	$ sudo apt install -y python3-pip python3-dev libevent2 linux-headers-$(uname -r)
	$ sudo -H pip3 install evdev simpleaudio
	```

*Running*
By default, the script waits for a 'b' keypress, which starts the auction.
Bidders have 3 seconds to top the highest bid.
The game has enough assets for 30 bids.

*Nota Bene*
Functions are commented out that will accept input from a device on a path you choose,
for use with evdev, so that custom controllers can be used to accept multiple bids
from multiple remotes or handsets.

While using stdin, 'q' at any time will quit.
