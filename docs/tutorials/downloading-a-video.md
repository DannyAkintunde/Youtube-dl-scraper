# Downloading a Video

The **YouTube DL Scraper** allows you to scrape and download videos from multiple YouTube downloader websites. This guide demonstrates how to download a video using the scraper.

Import the [YouTube][youtube_dl_scraper.core.youtube.YouTube] Classe

To begin, import the necessary classes from the package:

```py
from youtube_dl_scraper import YouTube
```

??? info "Alternatively"

    You cam import the [YouTube][youtube_dl_scraper.core.youtube.YouTube] class in other ways
    === "from core"

        ```py
        from youtube_dl_scraper.core import YouTube
        ```

    === "from the youtube moudle"
        ```py
        from youtube_dl_scraper.core.youtube import YouTube
        ```

Next intilize the [YouTube][youtube_dl_scraper.core.youtube.YouTube] [Object](https://docs.python.org/3/reference/datamodel.html)

```py
youtube = YouTube()
```

??? tip

    You can select the scrapers to use:
    === "video scraper"

        You can select the video `scraper` to use by using the `#!python video_scraper_name`[^1] argument
        ```py
        youtube = YouTube(video_scraper_name="y2save")
        ```
    === "caption scraper"

        You can select the caption `scraper` to use by using the `#!python caption_scraper_name`[^2] argument
        ```py
        youtube = YouTube(caption_scraper_name="downsub")
        ```

Now lets download a video for this example we'll download: [Coding levels explaind by thedevgeniusyt](https://youtu.be/dhlx4hGmgPY?si=3LOCbAqotNz3w0Ab) :fontawesome-brands-youtube:.

```py
video = youtube.scrape_video('https://youtu.be/dhlx4hGmgPY?si=3LOCbAqotNz3w0Ab')
```

Now we have a [Video][youtube_dl_scraper.core.video.Video] [Object](https://docs.python.org/3/reference/datamodel.html) which contains video data
This makes it easy for us to get the video infomation like title, duration e.t.c

```py
print(video.title) # (1)!
print(video.duration) # (2)!
print(video.fduration) # (3)!
print(video.thumbnail) # (4)!
```

1. Output: `#!python 'coding levels explained:what makes a beginner, intermediate and expert programmer?'`
2. Output: `#!python 185`
3. Output: `#!python '3.08 min'`
4. Output: `#! python 'https://i.ytimg.com/vi/dhlx4hGmgPY/sddefault.jpg'`

And to download the highest quality video

```py
# This returns the downloaded file path
print(video.get_highest_resolution().download()) # (1)!
```

1. Output: `#!python 'coding-levels-explained-what-makes-a-beginner-interm... .mp4'`

[^1]: The curretly avaliable video scrapers are [SaveTube](https://savetube.su) and [Y2Save](https://y2save.com).
[^2]: The only curretly avaliable caption scraper is [DownSub](https://downsub.com).
