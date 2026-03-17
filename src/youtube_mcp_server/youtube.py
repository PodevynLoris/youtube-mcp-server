"""YouTube data extraction using yt-dlp."""

from __future__ import annotations

import yt_dlp

from youtube_mcp_server.models import Channel, Chapter, Comment, Video


_BASE_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": False,
}


def search_videos(query: str, limit: int = 10) -> list[Video]:
    """Search YouTube for videos matching a query."""
    opts = {
        **_BASE_OPTS,
        "extract_flat": True,
        "playlist_items": f"1:{limit}",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)

    videos = []
    for entry in result.get("entries", []):
        if not entry:
            continue
        videos.append(_entry_to_video(entry))
    return videos


def get_video_info(video_url: str) -> Video:
    """Get detailed info about a single video."""
    opts = {**_BASE_OPTS, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    return _entry_to_video(info, full=True)


def get_channel_info(channel_url: str) -> Channel:
    """Get channel metadata."""
    url = _normalize_channel_url(channel_url)
    opts = {
        **_BASE_OPTS,
        "extract_flat": True,
        "playlist_items": "0:0",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"{url}/videos", download=False)

    return Channel(
        id=info.get("channel_id", info.get("id", "")),
        name=info.get("channel", info.get("uploader", "")),
        url=info.get("channel_url", url),
        subscribers=info.get("channel_follower_count"),
        description=info.get("description"),
        video_count=info.get("playlist_count"),
    )


def get_channel_videos(
    channel_url: str,
    limit: int = 20,
    sort: str = "date",
) -> list[Video]:
    """Get videos from a channel."""
    url = _normalize_channel_url(channel_url)
    opts = {
        **_BASE_OPTS,
        "extract_flat": True,
        "playlist_items": f"1:{limit}",
    }

    tab = "/videos"
    if sort == "popular":
        tab = "/videos?view=0&sort=p"

    with yt_dlp.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(f"{url}{tab}", download=False)

    videos = []
    for entry in result.get("entries", []):
        if not entry:
            continue
        videos.append(_entry_to_video(entry))
    return videos


def get_comments(video_url: str, limit: int = 20) -> list[Comment]:
    """Get comments from a video."""
    opts = {
        **_BASE_OPTS,
        "skip_download": True,
        "getcomments": True,
        "extractor_args": {"youtube": {"max_comments": [str(limit)]}},
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    comments = []
    for c in info.get("comments", [])[:limit]:
        comments.append(
            Comment(
                author=c.get("author", "Unknown"),
                text=c.get("text", ""),
                likes=c.get("like_count", 0),
                replies=c.get("reply_count", 0),
                published=c.get("timestamp") or c.get("time_text"),
            )
        )
    return comments


def get_playlist_videos(playlist_url: str, limit: int = 50) -> list[Video]:
    """Get videos from a playlist."""
    opts = {
        **_BASE_OPTS,
        "extract_flat": True,
        "playlist_items": f"1:{limit}",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)

    videos = []
    for entry in result.get("entries", []):
        if not entry:
            continue
        videos.append(_entry_to_video(entry))
    return videos


def _normalize_channel_url(url_or_name: str) -> str:
    """Normalize a channel URL or name to a full URL."""
    if url_or_name.startswith("http"):
        return url_or_name.rstrip("/")
    if url_or_name.startswith("@"):
        return f"https://www.youtube.com/{url_or_name}"
    return f"https://www.youtube.com/@{url_or_name}"


def _entry_to_video(entry: dict, full: bool = False) -> Video:
    """Convert a yt-dlp entry to a Video model."""
    video_id = entry.get("id", "")
    url = entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}"

    chapters = []
    if full and entry.get("chapters"):
        for ch in entry["chapters"]:
            chapters.append(
                Chapter(
                    title=ch.get("title", ""),
                    start_time=ch.get("start_time", 0),
                    end_time=ch.get("end_time"),
                )
            )

    return Video(
        id=video_id,
        title=entry.get("title", ""),
        url=url,
        channel=entry.get("channel", entry.get("uploader", "")),
        channel_url=entry.get("channel_url", entry.get("uploader_url", "")),
        duration=entry.get("duration"),
        views=entry.get("view_count"),
        likes=entry.get("like_count") if full else None,
        upload_date=entry.get("upload_date"),
        description=entry.get("description") if full else None,
        tags=entry.get("tags", []) if full else [],
        chapters=chapters,
    )
