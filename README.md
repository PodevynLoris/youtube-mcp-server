# YouTube MCP Server

A zero-config MCP server for YouTube. Search videos, get transcripts, browse channels, and **search within video content**. No API keys needed.

## Quick Start

```bash
uvx youtube-mcp-server
```

### Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["youtube-mcp-server"]
    }
  }
}
```

## Features

| Tool | What it does |
|---|---|
| `search_videos` | Search YouTube for videos |
| `get_video_info` | Get video details (title, description, stats, chapters) |
| `get_channel_info` | Get channel info (subscribers, description, video count) |
| `get_channel_videos` | List videos from a channel (sort by date or popularity) |
| `get_transcript` | Get full transcript with timestamps |
| `get_comments` | Get video comments |
| `search_transcript` | Search for specific content within a video's transcript |
| `search_channel_transcripts` | Search across all videos of a channel — find what a creator said about any topic |

## Examples

```
"Find YouTube videos about cold calling techniques"
→ search_videos

"What are the latest videos from @hormozi?"
→ get_channel_videos

"Get me the transcript of this video"
→ get_transcript

"What does Hormozi say about pricing?"
→ search_channel_transcripts — searches across all his videos, returns matching passages with timestamps and direct links

"Compare what YC and Hormozi say about product-market fit"
→ search_channel_transcripts on both channels
```

## HTTP Transport

```bash
youtube-mcp-server --transport streamable-http --port 8000
```

## License

MIT
