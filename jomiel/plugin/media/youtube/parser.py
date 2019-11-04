# -*- coding: utf-8 -*-
#
# jomiel
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""

from urllib.parse import parse_qs

from jomiel.error import ParseError
from jomiel.plugin.media.parser import PluginMediaParser


class Parser(PluginMediaParser):
    """Media metadata parser implementation for YouTube."""

    __slots__ = []

    def __init__(self, uri_components):
        """Initializes the object.

        Args:
            uri_components (dict): The input URI components

        """
        super(Parser, self).__init__(uri_components)
        self.parse(uri_components)

    def parse(self, uri_components):
        """Parses the relevant metadata for the media.

        Args:
            uri_components (dict): The input URI components

        Raises:
            jomiel.error.ParseError if a parsing error occurred
        """

        def parse_metadata(video_info):
            """Parse meta data from the video info."""
            video_info = parse_qs(video_info)

            def check_token():
                """Confirm that one of the tokens are present in video info."""
                keys = [
                    "token",
                    "account_playback_token",
                    "accountPlaybackToken",
                ]
                for key in keys:
                    if key in video_info:
                        return
                if "reason" in video_info:
                    raise ParseError(video_info("reason")[0])
                raise ParseError("none of the token value found")

            check_token()

            def check_if_rental():
                """Check if this is a 'rental' video."""
                if "ypc_video_rental_bar_text" in video_info:
                    if "author" not in video_info:
                        raise ParseError(
                            '"rental" videos not supported'
                        )

            check_if_rental()

            def parse_video_title():
                """Return video title from the video info."""
                try:
                    self.media.title = video_info["title"][0]
                except KeyError:
                    player_response = video_info["player_response"][0]
                    from json import loads

                    json_pr = loads(player_response)
                    try:
                        self.media.title = json_pr["videoDetails"][
                            "title"
                        ]
                    except KeyError:
                        raise ParseError(
                            json_pr["playabilityStatus"]["reason"]
                        )

            parse_video_title()
            self.add_streams(video_info)

        def parse_video_id():
            """Return the video ID from the input URI (components)."""
            from re import compile as rxc

            regex = rxc(r"v=([\w\-_]{11})")
            result = regex.match(uri_components.query)
            if result:
                self.media.identifier = result.group(1)
            else:
                raise ParseError("unable to determine video ID")
            return self.media.identifier

        video_id = parse_video_id()

        def video_info_uri():
            """Return the URI to query the info for the video."""
            from urllib.parse import urlencode

            data = urlencode(
                {
                    "video_id": video_id,
                    "eurl": "https://youtube.googleapis.com/v/"
                    + video_id,
                }
            )
            return "https://www.youtube.com/get_video_info?" + data

        info_uri = video_info_uri()

        from jomiel.hypertext import http_get

        video_info = http_get(info_uri).text
        parse_metadata(video_info)

    def add_streams(self, video_info):
        """Go through the returned video streams and return them."""

        def get_value(keyname, index=0):
            """Return a value for the keyname from the video info."""
            return video_info.get(keyname, [""])[index]

        from collections import namedtuple

        video_spec = namedtuple(
            "video_spec", "resolution, height, width"
        )

        def fail_if_rtmp():
            """Raise an error if this is an RTMP stream."""
            if "conn" in video_info and get_value("conn").startswith(
                "rtmp"
            ):
                raise ParseError('"rtmp" protocol not supported')

        fail_if_rtmp()

        stream_map = get_value("url_encoded_fmt_stream_map")
        adaptive_fmts = get_value("adaptive_fmts")

        def fail_if_no_streams():
            """Raise an error if could not find any (supported) streams."""
            if not stream_map and not adaptive_fmts:
                raise ParseError("unable to find any streams")

        fail_if_no_streams()
        encoded_stream_map = "{},{}".format(stream_map, adaptive_fmts)

        def fail_if_rtmpe():
            """Raise an error if this is an RTMPE stream."""
            if "rtmpe%3Dyes" in encoded_stream_map:
                raise ParseError('"rtmpe" protocol not supported')

        fail_if_rtmpe()

        def parse_fmt_list():
            """Parse items from the returned fmt_list."""

            def add_spec():
                """Add a new spec to the formats dict."""
                result = spec[1].split("x")
                if len(result) == 2:
                    fmt_type = int(spec[0])
                    formats[fmt_type] = video_spec(
                        resolution=spec[1],
                        height=int(result[1]),
                        width=int(result[0]),
                    )

            fmt_list = get_value("fmt_list")

            if not fmt_list:
                return {}

            formats = {}

            for fmt in fmt_list.split(","):
                spec = fmt.split("/")
                if len(spec) >= 1:
                    add_spec()

            return formats

        formats = parse_fmt_list()

        def stream_get(keyname, index=0):
            """Return stream data for the keyname."""
            return stream_data[keyname][index]

        for stream in encoded_stream_map.split(","):
            stream_data = parse_qs(stream)

            if "itag" not in stream_data or "url" not in stream_data:
                continue

            itag = int(stream_get("itag"))
            url = stream_get("url")

            if "sig" in stream_data:
                url += "&signature" + stream_get("sig")
            elif "s" in stream_data:
                raise ParseError("encrypted stream sigs not supported")

            if "ratebypass" not in url:
                url += "&ratebypass=yes"

            # Skip anything that is NOT included in the fmt_list.
            # These are typically DASH, etc.
            #
            if itag in formats:
                stream = self.media.stream.add()
                stream.quality.profile = str(itag)
                stream.quality.width = formats[itag].width
                stream.quality.height = formats[itag].height
                stream.uri = url


# vim: set ts=4 sw=4 tw=72 expandtab:
