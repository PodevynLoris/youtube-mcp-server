"""Tests for youtube.py helper functions — no network calls."""

from youtube_mcp_server.youtube import _normalize_channel_url, _entry_to_video


class TestNormalizeChannelUrl:
    def test_handle(self):
        assert _normalize_channel_url("@mkbhd") == "https://www.youtube.com/@mkbhd"

    def test_name_without_at(self):
        assert _normalize_channel_url("mkbhd") == "https://www.youtube.com/@mkbhd"

    def test_full_url(self):
        assert _normalize_channel_url("https://www.youtube.com/@mkbhd") == "https://www.youtube.com/@mkbhd"

    def test_trailing_slash(self):
        assert _normalize_channel_url("https://www.youtube.com/@mkbhd/") == "https://www.youtube.com/@mkbhd"


class TestEntryToVideo:
    def test_minimal_entry(self):
        entry = {
            "id": "abc123",
            "title": "Test Video",
            "channel": "TestChannel",
            "channel_url": "https://youtube.com/@test",
        }
        video = _entry_to_video(entry)
        assert video.id == "abc123"
        assert video.title == "Test Video"
        assert video.url == "https://www.youtube.com/watch?v=abc123"

    def test_full_entry(self):
        entry = {
            "id": "abc123",
            "title": "Test Video",
            "webpage_url": "https://youtube.com/watch?v=abc123",
            "channel": "TestChannel",
            "channel_url": "https://youtube.com/@test",
            "duration": 300,
            "view_count": 10000,
            "like_count": 500,
            "upload_date": "20260315",
            "description": "A test video",
            "tags": ["test", "video"],
            "chapters": [
                {"title": "Intro", "start_time": 0, "end_time": 30},
                {"title": "Main", "start_time": 30, "end_time": 270},
            ],
        }
        video = _entry_to_video(entry, full=True)
        assert video.views == 10000
        assert video.likes == 500
        assert video.description == "A test video"
        assert len(video.chapters) == 2
        assert video.chapters[0].title == "Intro"
