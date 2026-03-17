# YouTube MCP Server

[![PyPI version](https://img.shields.io/pypi/v/yt-mcp-server)](https://pypi.org/project/yt-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A **zero-config** MCP server for YouTube. Search videos, get transcripts, browse channels, and **search across a creator's entire content**. No API keys needed.

## Quick Start

```bash
uvx yt-mcp-server
```

Or install with pip:

```bash
pip install yt-mcp-server
```

## Setup

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["yt-mcp-server"]
    }
  }
}
```

### Claude Code

```bash
claude mcp add youtube -- uvx yt-mcp-server
```

### Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["yt-mcp-server"]
    }
  }
}
```

## Tools

| Tool | Description |
|---|---|
| **`search_channel_transcripts`** | **Search across ALL videos of a channel — find what any creator said about any topic** |
| `search_transcript` | Search within a single video's transcript |
| `get_transcript` | Get full transcript with timestamps |
| `search_videos` | Search YouTube for videos |
| `get_video_info` | Get video details — title, description, stats, chapters |
| `get_channel_info` | Get channel info — subscribers, description, video count |
| `get_channel_videos` | List videos from a channel, sorted by date or popularity |
| `get_comments` | Get video comments sorted by relevance |

## Example Prompts

```
"Search YouTube for videos about cold outreach strategies"
→ search_videos

"What are the latest videos from @hormozi?"
→ get_channel_videos

"Get me the full transcript of this video: https://youtube.com/watch?v=..."
→ get_transcript

"What does Hormozi say about pricing?"
→ search_channel_transcripts — searches all his videos, returns passages with timestamps

"Compare what YC and Hormozi say about product-market fit"
→ search_channel_transcripts on both channels
```

## HTTP Transport

Run as a standalone HTTP server:

```bash
yt-mcp-server --transport streamable-http --port 8000
```

## Requirements

- Python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (installed automatically)
- No API keys or authentication required

## Acknowledgments

Built with the assistance of [Claude](https://claude.ai) by Anthropic.

## License

MIT
