"""Tests for data models — no network calls, no tokens."""

from youtube_mcp_server.models import (
    Chapter,
    Channel,
    Comment,
    TranscriptMatch,
    TranscriptSegment,
    Video,
    _format_duration,
    _format_timestamp,
)


class TestFormatDuration:
    def test_seconds_only(self):
        assert _format_duration(45) == "0:45"

    def test_minutes_and_seconds(self):
        assert _format_duration(125) == "2:05"

    def test_hours(self):
        assert _format_duration(3661) == "1:01:01"

    def test_zero(self):
        assert _format_duration(0) == "0:00"


class TestFormatTimestamp:
    def test_basic(self):
        assert _format_timestamp(65.5) == "1:05"

    def test_with_hours(self):
        assert _format_timestamp(3723.0) == "1:02:03"


class TestVideo:
    def test_to_dict_minimal(self):
        v = Video(id="abc", title="Test", url="https://youtube.com/watch?v=abc", channel="Ch", channel_url="https://youtube.com/@ch")
        d = v.to_dict()
        assert d["id"] == "abc"
        assert d["title"] == "Test"
        assert "duration" not in d
        assert "views" not in d

    def test_to_dict_full(self):
        v = Video(
            id="abc", title="Test", url="https://youtube.com/watch?v=abc",
            channel="Ch", channel_url="https://youtube.com/@ch",
            duration=120, views=1000, likes=50, upload_date="20260101",
            description="Desc", tags=["tag1"],
            chapters=[Chapter(title="Intro", start_time=0, end_time=30)],
        )
        d = v.to_dict()
        assert d["duration"] == "2:00"
        assert d["duration_seconds"] == 120
        assert d["views"] == 1000
        assert d["tags"] == ["tag1"]
        assert len(d["chapters"]) == 1


class TestChannel:
    def test_to_dict(self):
        c = Channel(id="ch1", name="Test Channel", url="https://youtube.com/@test", subscribers=5000)
        d = c.to_dict()
        assert d["name"] == "Test Channel"
        assert d["subscribers"] == 5000


class TestComment:
    def test_to_dict(self):
        c = Comment(author="User1", text="Great video!", likes=10)
        d = c.to_dict()
        assert d["author"] == "User1"
        assert d["likes"] == 10
        assert "replies" not in d  # 0 replies omitted


class TestTranscriptSegment:
    def test_to_dict(self):
        s = TranscriptSegment(text="hello world", start=65.3, duration=4.0)
        d = s.to_dict()
        assert d["timestamp"] == "1:05"
        assert d["text"] == "hello world"


class TestTranscriptMatch:
    def test_to_dict_with_video(self):
        m = TranscriptMatch(
            text="pricing is key",
            start=120.0,
            video_title="How to Price",
            video_url="https://youtube.com/watch?v=abc",
        )
        d = m.to_dict()
        assert d["timestamp"] == "2:00"
        assert d["direct_link"] == "https://youtube.com/watch?v=abc&t=120s"
        assert d["video_title"] == "How to Price"
