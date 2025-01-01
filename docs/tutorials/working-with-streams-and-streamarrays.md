# Working With [Streams][youtube_dl_scraper.core.stream.Stream] and [StreamArrays][youtube_dl_scraper.core.stream_array.StreamArray]

The [Stream][youtube_dl_scraper.core.stream.Stream] and [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray] classes are core components of the `youtube_dl_scraper` package, enabling easy access and manipulation of video and audio streams. These classes provide a clean interface to work with individual streams or groups of streams.

## [Stream][youtube_dl_scraper.core.stream.Stream]

The [Stream][youtube_dl_scraper.core.stream.Stream] [class](https://docs.python.org/3/tutorial/classes.html) represents a single video or audio stream. It provides detailed information about the stream and includes methods for further interaction.

## [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray]

The [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray] [class](https://docs.python.org/3/tutorial/classes.html) represents a collection of Stream [objects](https://docs.python.org/3/reference/datamodel.html). It includes utility methods for filtering and selecting streams based on specific criteria.

## Key Features

-   Retrieve all streams matching a specific quality or format.
-   Iterate over all available streams.
-   And much more.

!!! abstract ""

    These classes streamline the process of managing [YouTube](https://youtube.com) :fontawesome-brands-youtube: video/audio streams, making it easy to access and utilize downloadable media. For more advanced use cases, explore the methods and attributes available within the [Stream][youtube_dl_scraper.core.stream.Stream] and [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray] classes.

# Working with Streams

We'll begin with the [video][youtube_dl_scraper.core.video.Video] object from the [previous example](../overview.md#installation) stored in the `#!python video` variable.

??? quote "Read more"

    From the previous example.

    ```py title="example.py" linenums="1"
    from youtube_dl_scraper import YouTube
    youtube = YouTube()
    video = youtube.scrape_video('https://youtu.be/sF9xYtouZjY?si=z6ZWk4raQeHgQDz')

    print(video.title) # print video title
    ```

We'll beging by running the following to list all [streams][youtube_dl_scraper.core.stream.Stream].

```py linenums="5"
# ...
print(video.streams) # (1)!
```

1. this returns the [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray] object containing the available [streams][youtube_dl_scraper.core.stream.Stream] in the [video][youtube_dl_scraper.core.video.Video].

??? quote "output"

    ```sh
    ((video 1080p 30fps is_hdr=False has_audio=True),
    (video 720p 30fps is_hdr=False has_audio=True),
    (video 360p 30fps is_hdr=False has_audio=True),
    (video 360p 30fps is_hdr=False has_audio=True),
    (audio 320), (audio 192),
    (video 144p 30fps is_hdr=False has_audio=True),
    (audio 128), (audio 64), (audio 32))
    ```

## Filtering Streams

**YouTube DL Scraper** provides built-in functionality to filter streams available in a [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray] object using the [`#!python filter()`][youtube_dl_scraper.core.stream_array.StreamArray.filter] method. This method supports various keyword arguments, allowing you to customize your search. Below, we’ll review some of the most commonly used options. For a complete list of filterable properties, refer to the API documentation for [youtube_dl_scraper.core.stream_array.StreamArray.filter][].

### Filtering [Video Streams][youtube_dl_scraper.core.stream.VideoStream]

To filter [video streams][youtube_dl_scraper.core.stream.VideoStream] we use the [`#!python get_video_streams()`][youtube_dl_scraper.core.stream_array.StreamArray.get_video_streams] method.

```py linenums="8"
print(video.streams.get_video_streams())
```

??? quote "output"

    ```sh
    ((video 1080p 30fps is_hdr=False has_audio=True),
    (video 720p 30fps is_hdr=False has_audio=True),
    (video 360p 30fps is_hdr=False has_audio=True),
    (video 360p 30fps is_hdr=False has_audio=True),
    (video 144p 30fps is_hdr=False has_audio=True))
    ```

??? abstract "more on video streams"

    Not all [streams][youtube_dl_scraper.core.stream.Stream] has audio, [streams][youtube_dl_scraper.core.stream.Stream] without audio are called <abbr title="Dynamic Adaptive Streaming over HTTP" >**DASH**</abbr> [streams][youtube_dl_scraper.core.stream.Stream] while ones with audio are **Progressive** [streams][youtube_dl_scraper.core.stream.Stream]. To filter [video streams][youtube_dl_scraper.core.stream.VideoStream] to ones with or without audio we use the [`#!python filter()`][youtube_dl_scraper.core.stream_array.StreamArray.filter] method.
    ```py
    print(video.streams.get_video_streams().filter(has_audio=True)) # with audio
    print(video.streams.get_video_streams().filter(has_audio=False)) # without audio
    ```
    Output:
    ```sh
    ((video 1080p 30fps is_hdr=False has_audio=True),
    (video 720p 30fps is_hdr=False has_audio=True),
    (video 360p 30fps is_hdr=False has_audio=True),
    (video 360p 30fps is_hdr=False has_audio=True),
    (video 144p 30fps is_hdr=False has_audio=True))
    ()
    ```

### Filtering [Audio Streams][youtube_dl_scraper.core.stream.AudioStream]

To filter [video streams][youtube_dl_scraper.core.stream.VideoStream] we use the [`#!python get_audio_streams()`][youtube_dl_scraper.core.stream_array.StreamArray.get_audio_streams] method.

```py linenums="9"
print(video.streams.get_audio_streams())
```

??? quote "output"

    ```sh
    ((audio 320), (audio 192), (audio 128),
    (audio 64), (audio 32))
    ```

## Ordering Streams

**YouTube DL Scraper** support the ability to order streams by any of it's attributes using the [`#!python order_by()`][youtube_dl_scraper.core.stream_array.StreamArray.order_by] method.

```py linenums="10"
print(video.streams.get_audio_streams().order_by("abr")) # (1)!
```

1. this returns a new [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray] object with streams ordered by <abbr title="Average Bitrate" >abr</abbr>

??? quote "output"

    ```sh
    ((audio 320), (audio 192), (audio 128), (audio 64), (audio 32))
    ```

# Downloading Streams

After you’ve selected the [Stream][youtube_dl_scraper.core.stream.Stream] you’re interested, you’re ready to interact with it. At this point, you can query information about the stream, such as its [size][youtube_dl_scraper.core.stream.Stream.size], whether the stream is audio/video, and more. You can also use the [download][youtube_dl_scraper.core.stream.Stream.download] method to save the file.

```py linenums="11"
print(video.streams.filter(resolution_value=720).download())
```

??? tip

    You can use [`#!python first()`][youtube_dl_scraper.core.stream_array.StreamArray.first] and [`#!python last()`][youtube_dl_scraper.core.stream_array.StreamArray.last] method to select the first or last [Stream][youtube_dl_scraper.core.stream.Stream] in the [StreamArray][youtube_dl_scraper.core.stream_array.StreamArray].
    ```py
    print(video.streams.first())
    print(video.streams.get_video_streams().last())
    ```
    And you can get the available qualities in a [stream array][youtube_dl_scraper.core.stream_array.StreamArray] using the [`#!python available_qualities`][youtube_dl_scraper.core.stream_array.StreamArray.available_qualities] property.
    ```py
    print(video.streams.available_qualities) # (1)!
    ```

    1. Output: `#!sh {'video': (1080, 720, 360, 360, 144), 'audio': (320, 192, 128, 64, 32)}`

    Lastly you can fetch streams using their index.
    ```py
    print(video.streams[0]) # getting first stream
    ```

    You can read more from the api docs for [youtube_dl_scraper.core.stream_array.StreamArray][]
