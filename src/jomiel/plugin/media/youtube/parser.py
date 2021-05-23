#
# jomiel
#
# Copyright
#  2019-2021 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from json import loads
from re import match as re_match
from urllib.parse import parse_qs
from urllib.parse import urlencode

from jomiel.error import ParseError
from jomiel.hypertext import http_get
from jomiel.hypertext import http_post
from jomiel.log import lg
from jomiel.plugin.media.parser import PluginMediaParser
from requests.exceptions import HTTPError

# from jomiel_kore.formatter import json_pprint


class Parser(PluginMediaParser):
    """Media metadata parser implementation for YouTube.

    - Retrieve data from the /get_video_info endpoint
    - If that fails, try the /youtubei/player endpoint, instead.

    """

    __slots__ = []

    def __init__(self, uri_components):
        """Initializes the object.

        Args:
            uri_components (dict): The input URI components

        """
        super().__init__(uri_components)
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

            def _value_from(d, key_name):
                """Return value from a dictionary, or raise an error."""
                if key_name in d:
                    return d.get(key_name)
                raise ParseError(f"'{key_name}' not found")

            def _check_playability_status():
                """Check the 'playability status' of the video."""
                playability_status = _value_from(
                    video_info,
                    "playabilityStatus",
                )
                if playability_status["status"] == "ERROR":
                    raise ParseError(playability_status["reason"])

            def parse_video_details():
                """Parse videoDetails of player_response."""
                vd = _value_from(video_info, "videoDetails")

                self.media.statistics.average_rating = float(
                    _value_from(vd, "averageRating"),
                )
                self.media.statistics.view_count = int(
                    _value_from(vd, "viewCount"),
                )
                self.media.description = _value_from(vd, "shortDescription")
                self.media.length_seconds = int(
                    _value_from(vd, "lengthSeconds"),
                )
                self.media.author.channel_id = _value_from(vd, "channelId")
                self.media.author.name = _value_from(vd, "author")
                self.media.title = _value_from(vd, "title")

                thumbs = _value_from(vd, "thumbnail")["thumbnails"]
                for t in thumbs:
                    thumb = self.media.thumbnail.add()
                    thumb.width = int(t["width"])
                    thumb.height = int(t["height"])
                    thumb.uri = t["url"]

            def parse_streaming_data():
                """Parse streaming data."""

                def parse(key):
                    """parse

                    Args:
                        key (str): the key name

                    """

                    def parse_format(fmt):
                        """parse_format

                        Args:
                            fmt (dict): the format dict to parse

                        """
                        s = self.media.stream.add()

                        s.quality.profile = "{} (itag={})".format(
                            fmt["qualityLabel"]
                            if "qualityLabel" in fmt
                            else fmt["quality"],
                            fmt["itag"],
                        )

                        if "width" in fmt and "height" in fmt:
                            s.quality.width = int(fmt["width"])
                            s.quality.height = int(fmt["height"])

                        s.quality.bitrate = int(fmt["bitrate"])
                        if "contentLength" in fmt:
                            s.content_length = int(fmt["contentLength"])

                        s.mime_type = fmt["mimeType"]
                        s.uri = fmt["url"]

                    formats = sd[key]

                    for fmt in formats:
                        parse_format(fmt)

                sd = _value_from(video_info, "streamingData")
                parse("adaptiveFormats")
                parse("formats")

            # json_pprint(video_info)
            _check_playability_status()
            parse_video_details()
            parse_streaming_data()

        def parse_player_response():
            """Check that "player_response" exists and return it.

            Returns:
                dict: the player response parsed from json

            """
            if "player_response" not in video_info:
                raise ParseError('"player_response" not found')
            return video_info["player_response"][0]

        def parse_video_id():
            """Parse video ID from the components of the input URI."""
            result = re_match(
                r"v=([\w\-_]{11})",
                uri_components.query,
            )
            if result:
                self.media.identifier = result.group(1)
            else:
                raise ParseError("unable to match video ID")

        def video_info_request():
            """Make a GET request to the /get_video_info endpoint."""
            v_id = self.media.identifier
            data = urlencode(
                {
                    "video_id": v_id,
                    "eurl": f"https://youtube.googleapis.com/v/{v_id}",
                    "html5": 1,
                },
            )
            uri = f"https://www.youtube.com/get_video_info?{data}"
            return http_get(uri).text

        def youtubei_request():
            """Make a POST request to the /youtubei/player endpoint."""
            uri = "https://www.youtube.com/youtubei/v1/player"
            params = {"key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"}
            payload = {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": "2.20201021.03.00",
                    },
                },
            }
            payload.update({"videoId": self.media.identifier})
            return http_post(uri, payload, params=params).text

        parse_video_id()
        try:
            video_info = video_info_request()
            video_info = parse_qs(video_info)
            video_info = parse_player_response()
        except HTTPError:
            # /get_video_info endpoint failed. Try /youtubei/player.
            lg().debug("http<get>: /get_video_info failed")
            video_info = youtubei_request()
        json = loads(video_info)
        parse_metadata(json)


# vim: set ts=4 sw=4 tw=72 expandtab:
