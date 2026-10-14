#!/bin/sh
# notify2 needs the system D-Bus bindings; everything else installs into a virtualenv.
sudo apt-get install -y python3-venv python3-dbus
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
