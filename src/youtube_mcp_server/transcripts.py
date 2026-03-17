"""Transcript extraction and search using youtube-transcript-api."""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from youtube_transcript_api import YouTubeTranscriptApi

from youtube_mcp_server.models import TranscriptMatch, TranscriptSegment

_api = YouTubeTranscriptApi()


def get_transcript(
    video_url: str,
    language: str = "en",
) -> list[TranscriptSegment]:
    """Get the transcript of a YouTube video."""
    video_id = _extract_video_id(video_url)
    try:
        transcript = _api.fetch(video_id, languages=[language, "en"])
    except Exception:
        # Fallback: try to get any available transcript
        transcript_list = _api.list(video_id)
        transcript = transcript_list.find_generated_transcript(
            [language, "en"]
        ).fetch()

    return [
        TranscriptSegment(
            text=entry.text,
            start=entry.start,
            duration=entry.duration,
        )
        for entry in transcript
    ]


def search_transcript(
    video_url: str,
    query: str,
    language: str = "en",
    context_segments: int = 2,
) -> list[TranscriptMatch]:
    """Search for a query within a video's transcript.

    Returns matching segments with surrounding context.
    """
    segments = get_transcript(video_url, language)
    query_lower = query.lower()
    matches = []
    used_indices: set[int] = set()

    for i, segment in enumerate(segments):
        if query_lower in segment.text.lower() and i not in used_indices:
            start_idx = max(0, i - context_segments)
            end_idx = min(len(segments), i + context_segments + 1)

            context_text_parts = []
            for j in range(start_idx, end_idx):
                context_text_parts.append(segments[j].text)
                used_indices.add(j)

            combined_text = " ".join(context_text_parts)
            matches.append(
                TranscriptMatch(
                    text=combined_text,
                    start=segments[start_idx].start,
                )
            )

    return matches


def search_channel_transcripts(
    video_urls: list[dict],
    query: str,
    language: str = "en",
    max_videos: int = 20,
) -> list[TranscriptMatch]:
    """Search for a query across multiple video transcripts.

    video_urls should be a list of dicts with 'url' and 'title' keys.
    """
    all_matches = []

    def _search_one(video: dict) -> list[TranscriptMatch]:
        url = video["url"]
        title = video.get("title", "")
        try:
            matches = search_transcript(url, query, language)
            for match in matches:
                match.video_title = title
                match.video_url = url
            return matches
        except Exception:
            return []

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(_search_one, v): v for v in video_urls[:max_videos]}
        for future in as_completed(futures):
            all_matches.extend(future.result())

    return all_matches


def _extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")
