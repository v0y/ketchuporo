Ketchuporo
==========

Pomodoro timer written in kivy


Kivy installation
-----------------

```sh
mkvirtualenv -p /usr/bin/python3 <venv_name>

pinstall cython==0.2

sudo apt-get install -y --force-yes build-essential mercurial git python3.3 \
    python3.3-dev ffmpeg libsdl-image1.2-dev libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev \
    libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

hg clone https://bitbucket.org/pygame/pygame
cd pygame
~/.virtualenvs/<venv_name>/bin/python setup.py build
sudo ~/.virtualenvs/<venv_name>/bin/python setup.py install
cd ..
sudo rm -rf pygame
```
