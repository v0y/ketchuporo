#!/usr/bin/env bash

export VERSION=0.1.0

mkdir -p build/usr/share/python
virtualenv build/usr/share/python/ketchuporo
which pip
. build/usr/share/python/ketchuporo/bin/activate
pip install -U pip distribute
pip install kivy==1.9.0
pip install plyer==1.2.3

cd build/usr/share/python/ketchuporo
virtualenv-tools --update-path /usr/share/python/ketchuporo
cd -

find build -iname *.pyc -exec rm {} \;
find build -iname *.pyo -exec rm {} \;

fpm \
  -t deb \
  -n ketchuporo \
  -v $VERSION \
  --iteration `date +%s` \
  -d python3 \
  -d 'cython >= 0.20' \
  --url https://github.com/v0y/ketchuporo \
  --description 'Simple Pomodoro timer.' \
  --license 'MIT' \
  --maintainer 'Rafał Mirończyk <voy@lolwtf.pl>' \
  --category 'accessories' \
  -s dir ketchuporo,build
