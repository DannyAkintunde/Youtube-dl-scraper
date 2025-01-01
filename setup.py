#!/usr/bin/env python
"""This module contains setup instructions for pytube."""
import os
from setuptools import setup, find_packages
from youtube_dl_scraper import __version__
from youtube_dl_scraper import __author__

__dirname = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(__dirname, "README.md"), encoding="utf-8") as file:
    long_description = "\n" + file.read()


setup(
    name="youtube_dl_scraper",
    version=__version__,
    author=__author__,
    author_email="dan29july@gmail.com",
    packages=find_packages(),
    package_data={"": ["LICENSE"],},
    license="MIT",
    url="https://github.com/DannyAkintunde/Youtube-dl-scraper/tree/dev",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    description=("Python 3 library for downloading YouTube Videos."),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
    zip_safe=True,
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "fake-useragent",
        "ffmpeg-python",
        "fleep",
        "langcodes",
        "tqdm",
        "Unidecode",
    ],
    project_urls={"Bug Reports": ""},
    keywords=[
        "youtube",
        "download",
        "video",
        "stream",
    ],
)
