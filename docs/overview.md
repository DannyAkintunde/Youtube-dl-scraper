# Overview

**YouTube DL Scraper** is a Python :material-language-python: library for scraping [YouTube](https://youtube.com) :fontawesome-brands-youtube: video/audio streams and metadata. It's lightweight, easy to use, and perfect for integrating YouTube data into your projects.
!!! warning

    This is the alpha version and the project is still in the testing phase.

---

## Features

-   Fetch video metadata such as title, description, and available streams.
-   Filter video/audio streams by resolution, bitrate, or format.
-   Download video/audio streams effortlessly.
-   Modular and extensible for advanced use cases.

---

## Installation

### Install via pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

YouTube DL Scraper is published as a [Python package] and can be installed with
`pip`, ideally by using a [virtual environment](https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment)[^1]. Open up a terminal and install
YouTube DL Scraper with:

=== "Latest"

    ``` sh
    pip install youtube-dl-scraper
    ```

---

??? example "Example Usage"

    Fetch `title` and download YouTube video:

    ```py title="example.py" linenums="1" hl_lines="6 8"
    from youtube_dl_scraper import YouTube # (1)!
    
    youtube = YouTube()
    
    # Scrape video data
    video = youtube.scrape_video("https://youtu.be/sF9xYtouZjY?si=z6ZWk4raQeHgQDz")

    print(video.title) # Print the video title (2)
    # Download video
    print(video.streams.get_highest_resolution().download()) # (3)!
    ```

    1. Importing [scraper][youtube_dl_scraper.core.youtube.YouTube] from package
    2. Output: `'Driving The New Fastest Car Ever Made!'`
    3. Output (file path): `'driving-the-new-fastest-car-ever-made-720p-30fps.mp4'`

[^1]: A [_virtual environment_](https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment) in programming (specifically in Python) is an isolated workspace that allows you to manage dependencies, libraries, and tools for a particular project without affecting the global system environment.
