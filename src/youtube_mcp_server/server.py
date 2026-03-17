"""YouTube MCP Server — main entry point."""

from __future__ import annotations

import json
import sys

from fastmcp import FastMCP

from youtube_mcp_server import youtube, transcripts

mcp = FastMCP("YouTube MCP Server")


@mcp.tool()
def search_videos(query: str, limit: int = 10) -> str:
    """Search YouTube for videos.

    Args:
        query: Search query (e.g. "how to price a SaaS")
        limit: Maximum number of results (default 10, max 30)
    """
    limit = min(limit, 30)
    videos = youtube.search_videos(query, limit)
    return json.dumps([v.to_dict() for v in videos], ensure_ascii=False, indent=2)


@mcp.tool()
def get_video_info(video_url: str) -> str:
    """Get detailed information about a YouTube video including title, description, stats, tags, and chapters.

    Args:
        video_url: YouTube video URL (e.g. "https://youtube.com/watch?v=xxx")
    """
    video = youtube.get_video_info(video_url)
    return json.dumps(video.to_dict(), ensure_ascii=False, indent=2)


@mcp.tool()
def get_channel_info(channel: str) -> str:
    """Get information about a YouTube channel.

    Args:
        channel: Channel URL or @handle (e.g. "@mkbhd" or "https://youtube.com/@mkbhd")
    """
    info = youtube.get_channel_info(channel)
    return json.dumps(info.to_dict(), ensure_ascii=False, indent=2)


@mcp.tool()
def get_channel_videos(channel: str, limit: int = 20, sort: str = "date") -> str:
    """Get videos from a YouTube channel.

    Args:
        channel: Channel URL or @handle (e.g. "@mkbhd")
        limit: Maximum number of videos (default 20, max 100)
        sort: Sort order — "date" (newest first) or "popular" (most viewed)
    """
    limit = min(limit, 100)
    videos = youtube.get_channel_videos(channel, limit, sort)
    return json.dumps([v.to_dict() for v in videos], ensure_ascii=False, indent=2)


@mcp.tool()
def get_transcript(video_url: str, language: str = "en") -> str:
    """Get the full transcript of a YouTube video with timestamps.

    Args:
        video_url: YouTube video URL
        language: Preferred language code (default "en", tries auto-generated fallback)
    """
    segments = transcripts.get_transcript(video_url, language)
    return json.dumps([s.to_dict() for s in segments], ensure_ascii=False, indent=2)


@mcp.tool()
def get_comments(video_url: str, limit: int = 20) -> str:
    """Get comments from a YouTube video.

    Args:
        video_url: YouTube video URL
        limit: Maximum number of comments (default 20, max 100)
    """
    limit = min(limit, 100)
    comments = youtube.get_comments(video_url, limit)
    return json.dumps([c.to_dict() for c in comments], ensure_ascii=False, indent=2)


@mcp.tool()
def search_transcript(video_url: str, query: str, language: str = "en") -> str:
    """Search for specific content within a video's transcript.
    Returns matching passages with timestamps and direct links.

    Args:
        video_url: YouTube video URL
        query: Text to search for in the transcript
        language: Preferred language code (default "en")
    """
    matches = transcripts.search_transcript(video_url, query, language)
    if not matches:
        return json.dumps({"message": f"No matches found for '{query}' in this video."})
    return json.dumps([m.to_dict() for m in matches], ensure_ascii=False, indent=2)


@mcp.tool()
def search_channel_transcripts(
    channel: str,
    query: str,
    language: str = "en",
    max_videos: int = 20,
) -> str:
    """Search for specific content across all videos of a YouTube channel.
    This is the power feature: find what a creator said about any topic.

    Args:
        channel: Channel URL or @handle (e.g. "@hormozi")
        query: Text to search for across all transcripts
        language: Preferred language code (default "en")
        max_videos: Maximum number of recent videos to search (default 20, max 50)
    """
    max_videos = min(max_videos, 50)
    videos = youtube.get_channel_videos(channel, max_videos, "date")
    video_list = [{"url": v.url, "title": v.title} for v in videos]
    matches = transcripts.search_channel_transcripts(video_list, query, language, max_videos)
    if not matches:
        return json.dumps({"message": f"No matches found for '{query}' across this channel's videos."})
    return json.dumps([m.to_dict() for m in matches], ensure_ascii=False, indent=2)


def main():
    """Run the MCP server."""
    transport = "stdio"
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        host = "0.0.0.0"
        port = 8000
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                port = int(sys.argv[idx + 1])
        mcp.run(transport="streamable-http", host=host, port=port)


if __name__ == "__main__":
    main()
