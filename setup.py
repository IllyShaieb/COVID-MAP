import os
from setuptools import setup

setup(
    name='comap',
    url='https://github.com/EquallyWolf/COMAP',
    author='Illias Shaieb',
    author_email='shaiebilly@gmail.com',
    packages=['comap'],
    install_requires=['BeautifulSoup4', 'requests'],
    version='1.0',
    license='GNU GPLv3',
    description='This script sends an email of the latest COVID19 data for your chosen country and saves the data to a csv.',
)