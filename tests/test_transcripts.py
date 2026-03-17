"""Tests for transcript logic — no network calls, uses mocking."""

from unittest.mock import patch

from youtube_mcp_server.models import TranscriptSegment
from youtube_mcp_server.transcripts import (
    _extract_video_id,
    search_transcript,
)


class TestExtractVideoId:
    def test_standard_url(self):
        assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_short_url(self):
        assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_bare_id(self):
        assert _extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_url_with_params(self):
        assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120s") == "dQw4w9WgXcQ"

    def test_invalid_url(self):
        try:
            _extract_video_id("not-a-valid-url")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestSearchTranscript:
    @patch("youtube_mcp_server.transcripts.get_transcript")
    def test_finds_matches(self, mock_get):
        mock_get.return_value = [
            TranscriptSegment(text="welcome to the video", start=0.0, duration=3.0),
            TranscriptSegment(text="today we talk about pricing", start=3.0, duration=3.0),
            TranscriptSegment(text="pricing is very important", start=6.0, duration=3.0),
            TranscriptSegment(text="let me explain why", start=9.0, duration=3.0),
            TranscriptSegment(text="the end", start=12.0, duration=3.0),
        ]
        matches = search_transcript("https://youtube.com/watch?v=abc", "pricing", context_segments=1)
        assert len(matches) == 1
        assert "pricing" in matches[0].text.lower()
        # Should include context
        assert "welcome" in matches[0].text.lower()

    @patch("youtube_mcp_server.transcripts.get_transcript")
    def test_no_matches(self, mock_get):
        mock_get.return_value = [
            TranscriptSegment(text="hello world", start=0.0, duration=3.0),
        ]
        matches = search_transcript("https://youtube.com/watch?v=abc", "pricing")
        assert len(matches) == 0

    @patch("youtube_mcp_server.transcripts.get_transcript")
    def test_case_insensitive(self, mock_get):
        mock_get.return_value = [
            TranscriptSegment(text="PRICING is KEY", start=0.0, duration=3.0),
        ]
        matches = search_transcript("https://youtube.com/watch?v=abc", "pricing")
        assert len(matches) == 1
