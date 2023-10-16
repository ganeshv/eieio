# Old MacDonald had a Mac - EIEIO

macOS menubar apps for monitoring CPU, network usage. Written in Python.

## Installation

  * Clone the repository
  * `pip install rumps psutil`

Use virtualenv or other solutions as per your taste.
TBD: Document setting up launchd to run this at login time

## And in that Mac he had some NICs

`python net-monitor.py`

will display a bar graph showing upload and download speeds over the last
couple of minutes on the en0 interface (most commonly the Wifi interface on
laptops). Click the menu to change the selected interface.

## And in that Mac he had some chips

`python cpu-monitor.py`

will display a bar graph showing CPU usage over the last couple of minutes.
The drop-down menu displays the current top 5 CPU-hogs.

(Yes, the multiline title is janky, but it looks just about OK on macOS Ventura)

## And in that Mac he had some disks

TBD

## Notes

Uses [rumps](https://github.com/jaredks/rumps) to do most of the heavy lifting
of putting up a menubar app. However, we need to break the abstraction here and
there to get monospace fonts, multiline titles, dynamic icons.

ChatGPT 4 and Github Copilot were heavily used.

## License
This extension is licensed under the MIT License. See the LICENSE file for more information.