import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='comap',
    url='https://github.com/EquallyWolf/COMAP',
    author='Illias Shaieb',
    author_email='shaiebilly@gmail.com',
    packages=['comap'],
    install_requires=required,
    version='1.0',
    license='GNU GPLv3',
    description='This script sends an email of the latest COVID19 data for your chosen country and saves the data to a csv.',
)