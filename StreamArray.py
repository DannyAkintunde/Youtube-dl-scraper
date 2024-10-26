from .Stream import Stream


class StreamArray:

    def __init__(self, *args):
        self._sorted_streams = None
        self._streams = list(args)
        #print(self._streams)

    @property
    def streams(self):
        if not getattr(self, '_sorted_streams'):
            self._sorted_streams = tuple(
                sorted(self._streams, key=(lambda stream: int(stream.resolution[:-1]) if stream.resolution else 0),
                       reverse=True))
        return self._sorted_streams

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.streams):
            # sorted_streams = sorted(self.streams, key=(lambda stream: stream.resolution[:-1]))
            item = self.streams[self.i]
            self.i += 1
            return item
        else:
            raise StopIteration

    def __getitem__(self, item):
        try:
            return self._streams[item]
        except KeyError:
            print("Not stream with index: {}".format(item))

    def __str__(self):
        return str(self.streams)
    
    def __len__(self):
        return len(self.streams)

    def get_highest_resolution(self) -> Stream:
        video_streams = filter((lambda stream: not stream.is_audio), self.streams)
        ordered_by_res = sorted(video_streams,
                                key=(lambda stream: int(stream.resolution[:-1]) if stream.resolution else 0),
                                reverse=True)
        if len(ordered_by_res) > 0:
            ordered_by_frame_rate = sorted(ordered_by_res, key=lambda stream: int(stream.frame_rate), reverse=True)
            ordered_by_hdr = sorted(ordered_by_frame_rate, key=(lambda stream: stream.is_hdr), reverse=True)
            return ordered_by_hdr[0]

    def get_audio_only(self) -> Stream:
        aud_streams = filter((lambda stream: stream.is_audio), self.streams)
        ordered_by_abr = sorted(aud_streams,
                                key=(lambda stream: int(stream.abr[:-4]) if stream.abr else 0),
                                reverse=True)
        if len(ordered_by_abr) > 0:
            return ordered_by_abr[0]

    def get_available_resolutions(self) -> tuple:
        resolutions = [stream.resolution for stream in self.streams if stream.is_video]
        return tuple(set(sorted(resolutions, key=(lambda key: int(key[:-1]) if key else 0), reverse=True)))
    
    def get_available_bit_rates(self) -> tuple:
        bit_rate = [stream.bit_rate for stream in self.streams if stream.is_video]
        return tuple(set(sorted(bit_rate, key=(lambda key: int(key[:-4]) if key else 0), reverse=True)))

    def get_avaliable_frame_rates():
        frame_rates = [stream.frame_rate for stream in self.streams if stream.is_video]
        return tuple(set(frame_rates))
      
    def get_audio(self) -> Stream:
        return list(filter(lambda stream: stream.is_audio, self.streams))

    def filter(self, **kwargs):
        reverse = kwargs.get('reverse')
        if reverse is not None and not isinstance(reverse, bool):
            raise ValueError("Reverse keyword argument must be of type bool")
        filtered = []
        for key, value in kwargs.items():
            # fake_stream_obj = Stream('')
            for stream in self.streams:
                if hasattr(stream, key):
                    attr = getattr(stream, key)
                    if attr == value:
                        filtered.append(stream)
                else:
                    raise KeyError(f'{key} not found in Stream Object')
        # print(filtered)
        return StreamArray(*filtered)
    
    def order_by(self, key):
        if not all([hasattr(stream, key) for stream in self.streams]): return
        return StreamArray(**sorted(self.streams, key=(lambda stream: getattr(stream, key)), reverse=True))
        
    def first(self):
        if len(self) > 0:
            return self[0]

    def _append(self, *args):
        if all([isinstance(stream, Stream) for stream in args]):
            self._streams.append(*args)
        else:
            raise TypeError("All args must be of type Stream")
