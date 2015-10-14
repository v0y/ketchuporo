[![Code Health](https://landscape.io/github/v0y/ketchuporo/master/landscape.svg?style=flat)](https://landscape.io/github/v0y/ketchuporo/master)

Ketchuporo
==========

Pomodoro timer written in kivy


Kivy installation
-----------------

http://kivy.org/docs/installation/installation-linux.html

```sh
mkvirtualenv ketchuporo
workon ketchuporo
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python setup.py build
sudo python setup.py install
cd ..
sudo rm -rf pygame
```


Install and run
---------------

Prepare environment first - https://github.com/v0y/ketchuporo#kivy-installation

```sh
git clone git@github.com:v0y/ketchuporo.git
workon ketchuporo  # or activate venv like an animal (source ~/.virtualenvs/ketchuporo/bin/activate)
pip install cython==0.23
cd ketchuporo
python setup.py install  # or python setup.py develop
python ketchuporo/main.py
```


Create atlas
------------

```sh
python -m kivy.atlas ketchuporo/lib/graphics/ketchuporo 256 ketchuporo/lib/graphics/*.png
```
