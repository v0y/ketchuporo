[![Code Health](https://landscape.io/github/v0y/ketchuporo/master/landscape.svg?style=flat)](https://landscape.io/github/v0y/ketchuporo/master)

Ketchuporo
==========

Pomodoro timer written in kivy


Kivy installation
-----------------

```sh
venv_name="ketchuporo"
venv_loc="~/.virtualenvs"

mkvirtualenv -p /usr/bin/python3 $venv_name

sudo apt-get install -y --force-yes build-essential mercurial git \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev \
    libavcodec-dev zlib1g-dev

hg clone https://bitbucket.org/pygame/pygame
cd pygame
$venv_loc/$venv_name/bin/python setup.py build
sudo $venv_loc/$venv_name/bin/python setup.py install
cd ..
sudo rm -rf pygame
```


Install and run
---------------

Prepare environment first - https://github.com/v0y/ketchuporo#kivy-installation

```sh
git clone git@github.com:v0y/ketchuporo.git
workon ketchuporo  # or activate venv like an animal (source ~/.virtualenvs/ketchuporo/bin/activate)
pip install cython==0.20
cd ketchuporo
python setup.py install  # or python setup.py develop
python ketchuporo/main.py
```


Create atlas
------------

```sh
python -m kivy.atlas lib/graphics/ketchuporo 128 lib/graphics/*.png
```
