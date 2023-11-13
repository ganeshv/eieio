# Old MacDonald had a Mac - EIEIO

macOS menubar apps for monitoring CPU, network usage. Written in Python.

## Installation

### Basic

  * Clone the repository
  * `pip install rumps psutil`

Use virtualenv or other solutions as per your taste. Run individual monitor
programs after activating the virtual environment using
`python xyz-monitor.py`

### Advanced

This will set things up so that the monitor programs will run on login.

  * Clone the repository
  * Ensure that `virtualenv` is installed; `pip install virtualenv` or
    `brew install virtualenv`
  * Edit the Makefile to choose which monitors you want to run
  * `make install`

Note that the virtualenv is created in the project directory itself.
Use `make uninstall` and `make clean` to reverse the above steps.

## And in that Mac he had some NICs

`python net-monitor.py`

will display a bar graph showing upload and download speeds over the last
couple of minutes on the en0 interface (most commonly the Wifi interface on
laptops). Click the menu to change the selected interface.

Given the range of possible network speeds, a log scale is used, with the
lowest level being 16K/sec, and the tallest bar for 1024K/sec and above. Uploads
are shaded gray and rise from the bottom, downloads are black and grow downwards
from the top.

(The multiline title is janky, but it looks just about OK on macOS Ventura)

## And in that Mac he had some chips

`python cpu-monitor.py`

will display a bar graph showing CPU usage over the last couple of minutes.
The drop-down menu displays the current top 5 CPU-hogs. This graph uses a
linear scale.

## And in that Mac he had some disks

TBD

## Notes

Uses [rumps](https://github.com/jaredks/rumps) to do most of the heavy lifting
of putting up a menubar app. However, we need to break the abstraction here and
there to get monospace fonts, multiline titles, dynamic icons.

ChatGPT 4 and Github Copilot were heavily used.

## License
MIT License. See the LICENSE file for more information.
