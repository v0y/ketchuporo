#!/usr/bin/env bash

export VERSION=0.1.0

mkdir -p build/usr/share/python
virtualenv build/usr/share/python/ketchuporo
build/usr/share/python/ketchuporo/bin/pip install -U pip distribute
build/usr/share/python/ketchuporo/bin/pip uninstall -y distribute

cd build/usr/share/python/ketchuporo
virtualenv-tools --update-path /usr/share/python/ketchuporo
cd -

find build -iname *.pyc -exec rm {} \;
find build -iname *.pyo -exec rm {} \;

fpm \
  -t deb -s dir -n Ketchuporo -v $VERSION \
  --iteration `date +%s` \
  -d python3 \
  -d 'cython > 0.20' \
  -d 'kivy > 1.8.0' \
  -d 'plyer > 1.2.3' \
  --url https://github.com/v0y/ketchuporo \
  --description 'Simple Pomodoro timer.' \
  --license 'MIT'
