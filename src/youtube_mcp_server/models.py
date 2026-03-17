"""Data models for YouTube MCP Server."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Video:
    id: str
    title: str
    url: str
    channel: str
    channel_url: str
    duration: int | None = None
    views: int | None = None
    likes: int | None = None
    upload_date: str | None = None
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    chapters: list[Chapter] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "channel": self.channel,
            "channel_url": self.channel_url,
        }
        if self.duration is not None:
            data["duration_seconds"] = self.duration
            data["duration"] = _format_duration(self.duration)
        if self.views is not None:
            data["views"] = self.views
        if self.likes is not None:
            data["likes"] = self.likes
        if self.upload_date:
            data["upload_date"] = self.upload_date
        if self.description:
            data["description"] = self.description
        if self.tags:
            data["tags"] = self.tags
        if self.chapters:
            data["chapters"] = [c.to_dict() for c in self.chapters]
        return data


@dataclass
class Chapter:
    title: str
    start_time: float
    end_time: float | None = None

    def to_dict(self) -> dict:
        data = {
            "title": self.title,
            "start_time": _format_timestamp(self.start_time),
            "start_seconds": self.start_time,
        }
        if self.end_time is not None:
            data["end_time"] = _format_timestamp(self.end_time)
        return data


@dataclass
class Channel:
    id: str
    name: str
    url: str
    subscribers: int | None = None
    description: str | None = None
    video_count: int | None = None

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
        }
        if self.subscribers is not None:
            data["subscribers"] = self.subscribers
        if self.description:
            data["description"] = self.description
        if self.video_count is not None:
            data["video_count"] = self.video_count
        return data


@dataclass
class Comment:
    author: str
    text: str
    likes: int = 0
    replies: int = 0
    published: str | None = None

    def to_dict(self) -> dict:
        data = {
            "author": self.author,
            "text": self.text,
            "likes": self.likes,
        }
        if self.replies:
            data["replies"] = self.replies
        if self.published:
            data["published"] = self.published
        return data


@dataclass
class TranscriptSegment:
    text: str
    start: float
    duration: float

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "timestamp": _format_timestamp(self.start),
            "start_seconds": round(self.start, 2),
        }


@dataclass
class TranscriptMatch:
    text: str
    start: float
    video_title: str | None = None
    video_url: str | None = None

    def to_dict(self) -> dict:
        data = {
            "text": self.text,
            "timestamp": _format_timestamp(self.start),
            "start_seconds": round(self.start, 2),
        }
        if self.video_title:
            data["video_title"] = self.video_title
        if self.video_url:
            data["video_url"] = self.video_url
            data["direct_link"] = f"{self.video_url}&t={int(self.start)}s"
        return data


def _format_duration(seconds: int) -> str:
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"
