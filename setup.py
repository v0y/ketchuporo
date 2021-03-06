# -*- coding: utf-8 -*-

from setuptools import setup

requires = [
    'kivy==1.9.0',
    'plyer==1.2.3',
    'pillow==3.0.0',
]


setup(
    name='Ketchuporo',
    version='0.1',
    description='Pomodoro timer',
    author='Rafał Mirończyk',
    author_email='voy@lolwtf.pl',
    url='https://github.com/v0y/ketchuporo',
    license='MIT',
    install_requires=requires,
    packages=['ketchuporo'],
)
