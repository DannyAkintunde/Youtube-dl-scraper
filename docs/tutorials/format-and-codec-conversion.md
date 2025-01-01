# Format and Codec Conversion

In this tutorial we'll deal with convertion of codecs[^1] and formats. Lets start with this [Youtube video](https://youtu.be/0DWx7VQHkRY?si=2dGCBJowS_JCgEn2) by [Arjan Codes](https://youtube.com/@arjancodes?si=AE13i-zCd4N6Yaef).

```py title="codec_demo.py" linenums="1"
from youtube_dl_scraper import YouTube
youtube = YouTube()
video = youtube.scrape_video("https://youtu.be/0DWx7VQHkRY?si=2dGCBJowS_JCgEn2")
video_file = video.streams.filter(resolution_value=360).first().download()
```

!!! info

    **YouTube DL Scraper** allows for converting codecs[^1] and formats using the `Converter` module at `#!python youtube_dl_scraper.converter`.

Now that we've downloaded our video, we can now convert it or change the format.

## Changing Codec of video

To change the codec[^1] of a video is pretty simple, to do that well use our [`#!python VideoConverter`][youtube_dl_scraper.converter.video_converter.VideoConverter] class from our converter module.

!!! example

    ```py linenums="5" title="converting video codec"
    from youtube_dl_scraper.converter import VideoConverter
    converter = VideoConverter(
        input_path=video_file,
        output_path=".", # (1)!
        video_codec="h264"
    )
    print(converter.convert()) # returns path to output_file
    ```

    1. if the `output_path` argument is set to `#!python '.'` the `output_file` will be saved at the `input_file` directory.

    Output:
    ```sh
    downloads/this-is-way-more-dangerous-than-ai-360p-30fps-converted.mp4
    ```
    if you'd like to change the video format(ext) all you'll have to do is set the `output_path` to a new path with the preffered extention for example `#!python 'downloads/converted.m4a'`.

You can also change the video audio codec[^1] because some videos contaons audio :smile:.

!!! example

    ```py linenums="12"
    converter = VideoConverter(
        input_path=video_file,
        output_path="downloads/video_with_opus_audio_codec.mp4",
        video_codec="h264",
        audio_codec="opus"
    )
    print(converter.convert())
    ```
    Output:
    ```sh
    downloads/video_with_opus_audio_codec.mp4
    ```

## Changing Codec of Audio

Changing the codec[^1] of an audio file is simillar to that of a video file, the only diffrence is the fact that we use the [`#!python AudioConverter`][youtube_dl_scraper.converter.audio_converter.AudioConverter] class instead.

```py linenums="19"
audio_file = video.streams.get_highest_bitrate().download()
```

!!! example

    ```py linenums="20" title="converting video codec"
    from youtube_dl_scraper.converter import AudioConverter
    converter = AudioConverter(
        input_path=audio_file,
        output_path=".", # (1)!
        audio_codec="opus" # or libopus
    )
    print(converter.convert()) # returns path to output_file
    ```

    1. if the `output_path` argument is set to `#!python '.'` the `output_file` will be saved at the `input_file` directory.

    Output:
    ```sh
    downloads/this-is-way-more-dangerous-than-ai-320kbps-audio-converted.m4a
    ```

But the [`#!python AudioConverter`][youtube_dl_scraper.converter.audio_converter.AudioConverter] allows us to adjust the audio bitrate.

!!! example

    ```py linenums="27"
    converter = AudioConverter(
        input_path=audio_file,
        output_path="downloads/audio_at_320kbps.mp3",
        audio_codec="opus", # or libopus
        bitrate="320k"
    )
    print(converter.convert())
    ```
    Output:
    ```sh
    downloads/audio_at_320kbps.mp3
    ```

!!! tip

    You can also use the [AudioConverter][youtube_dl_scraper.converter.audio_converter.AudioConverter] to convert a video to an _audio file_.
    ```py title="video to audio"
    converter = AudioConverter(
        input_path=video_file,
        output_path="downloads/video_to_audio.m4a"
        audio_codec="aac"
    )
    print(converter.convert())
    ```
    Output:
    ```sh
    downloads/video_to_audio.m4a
    ```

For more info about the [AudioConverter][youtube_dl_scraper.converter.audio_converter.AudioConverter] visit the api refrence of [youtube_dl_scraper.converter.video_converter.VideoConverter][].

[^1]: A codec is a tool that compresses and decompresses video or audio files. It reduces file size while maintaining quality. Common video codecs include H.264 and VP9, and audio codecs like AAC and MP3. Codecs help ensure media compatibility across devices.
