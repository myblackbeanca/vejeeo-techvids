# YouTube Data Specifications

This document outlines the data structures, API specifications, and implementation details for the Vejeeo TechVids pipeline.

## Data Models

### Channel Data Structure

```json
{
  "name": "string",           // Channel display name
  "url": "string",            // YouTube channel URL
  "channel_id": "string",     // YouTube channel ID (UC...)
  "language": "string",       // Primary language of content
  "category": "string",       // Content category

  // Extended data from YouTube API (when enriched)
  "title": "string",          // Official channel title
  "description": "string",    // Channel description
  "custom_url": "string",     // Custom channel URL
  "published_at": "datetime", // Channel creation date
  "thumbnails": {
    "default": {"url": "string", "width": int, "height": int},
    "medium": {"url": "string", "width": int, "height": int},
    "high": {"url": "string", "width": int, "height": int}
  },
  "country": "string",        // Country of origin
  "view_count": int,          // Total channel views
  "subscriber_count": int,    // Total subscribers
  "hidden_subscriber_count": boolean,
  "video_count": int,         // Total videos uploaded
  "keywords": "string",       // Channel keywords/tags
  "uploads_playlist_id": "string",  // Playlist ID for uploads
  "latest_videos": [
    {
      "video_id": "string",
      "title": "string",
      "published_at": "datetime",
      "thumbnail": "string"
    }
  ]
}
```

### Category Types

- **Tutorial** - Step-by-step coding tutorials and courses
- **Informational** - Software development news, career advice, tech talks
- **Live Coding** - Live programming sessions and streams
- **Game Development** - Game programming and Unity/Unreal content
- **Software Entertainment** - Tech comedy, experiments, fun projects
- **Competitive Programming** - Algorithm challenges, interview prep
- **Artificial Intelligence and Machine Learning** - AI/ML tutorials and research
- **Up And Coming** - Emerging channels (< 10K subscribers)
- **Retired** - Channels inactive for 6+ months
- **Web Development** - Frontend, backend, full-stack web dev

### Language Codes

- `English` - English language content
- `Hindi` - Hindi language content
- `Spanish` - Spanish language content
- `Brazilian Portuguese` - Portuguese (Brazilian) content
- `Russian` - Russian language content
- `Turkish` - Turkish language content
- `Korean` - Korean language content
- `Arabic` - Arabic language content
- `Chinese` - Chinese language content
- `French` - French language content
- `German` - German language content
- `Polish` - Polish language content
- `Italian` - Italian language content
- `Indonesian` - Indonesian language content
- `Bengali` - Bengali language content
- `Hebrew` - Hebrew language content
- `Vietnamese` - Vietnamese language content
- `Farsi` - Farsi language content
- `Catalan` - Catalan language content
- `Uzbek` - Uzbek language content
- `Somali` - Somali language content

## YouTube Data API v3

### Authentication

```bash
export YOUTUBE_API_KEY='your-api-key-here'
```

### API Endpoints Used

#### 1. Channels Endpoint

**Endpoint:** `GET https://www.googleapis.com/youtube/v3/channels`

**Parameters:**
- `part` - `snippet,statistics,contentDetails,brandingSettings`
- `id` - Channel ID
- `key` - API key

**Quota Cost:** 1 unit

**Response:**
```json
{
  "items": [{
    "id": "UCxxxxx",
    "snippet": {
      "title": "Channel Name",
      "description": "Channel description",
      "customUrl": "@channelname",
      "publishedAt": "2010-01-01T00:00:00Z",
      "thumbnails": {...},
      "country": "US"
    },
    "statistics": {
      "viewCount": "1000000",
      "subscriberCount": "100000",
      "videoCount": "500",
      "hiddenSubscriberCount": false
    },
    "contentDetails": {
      "relatedPlaylists": {
        "uploads": "UUxxxxx"
      }
    },
    "brandingSettings": {
      "channel": {
        "keywords": "programming tutorial coding"
      }
    }
  }]
}
```

#### 2. PlaylistItems Endpoint

**Endpoint:** `GET https://www.googleapis.com/youtube/v3/playlistItems`

**Parameters:**
- `part` - `snippet,contentDetails`
- `playlistId` - Uploads playlist ID
- `maxResults` - Max number of results (1-50)
- `key` - API key

**Quota Cost:** 1 unit

**Response:**
```json
{
  "items": [{
    "snippet": {
      "title": "Video Title",
      "publishedAt": "2024-01-01T00:00:00Z",
      "thumbnails": {...}
    },
    "contentDetails": {
      "videoId": "xxxxxxxxxxx"
    }
  }]
}
```

### Rate Limits & Quotas

- **Default Quota:** 10,000 units per day
- **Per-Request Cost:**
  - Channel details: 1 unit
  - Playlist items: 1 unit
  - Channel search (by username): 1 unit

- **Estimated Capacity:**
  - ~2,500 full channel enrichments per day
  - Our pipeline: 652 channels = ~2,000 units total

### Error Handling

**Common HTTP Status Codes:**

- `200 OK` - Success
- `400 Bad Request` - Invalid parameter
- `403 Forbidden` - Quota exceeded or invalid API key
- `404 Not Found` - Channel not found

## Data Pipeline Architecture

### Stage 1: Parsing

**Input:** DevYouTubeList/README.md

**Process:**
1. Read markdown file line by line
2. Track current language and category sections
3. Extract markdown links: `[Name](URL)`
4. Parse URL to extract channel identifier
5. Build structured JSON

**Output:** `channels_data.json`

```json
{
  "total_channels": 652,
  "channels": [...]
}
```

### Stage 2: Enrichment (Optional)

**Input:** `channels_data.json`

**Process:**
1. For each channel:
   - Resolve channel ID from URL/username
   - Fetch channel details from YouTube API
   - Fetch latest 5 videos
   - Add 0.5s delay between requests
   - Save checkpoint every 50 channels
2. Handle errors gracefully
3. Save failed channels for retry

**Output:** `enriched_channels.json`

```json
{
  "total_channels": 652,
  "fetched_at": "2024-01-08 20:00:00",
  "channels": [...]
}
```

### Stage 3: Documentation Generation

**Input:** `enriched_channels.json` (or `channels_data.json`)

**Process:**
1. Generate multiple markdown views:
   - By Category (alphabetical within each category)
   - By Language (subscriber count desc within each language)
   - Top 100 Rankings (subscriber count desc)
   - Statistics and breakdowns
2. Format numbers (K, M, B suffixes)
3. Create detailed channel cards

**Output:** `docs/` directory

```
docs/
├── CHANNELS_BY_CATEGORY.md    # Organized by content type
├── CHANNELS_BY_LANGUAGE.md     # Organized by language
├── TOP_100_CHANNELS.md         # Leaderboard
└── STATISTICS.md               # Aggregated analytics
```

## Export Formats

### JSON Export

Standard JSON with all channel data:

```json
{
  "total_channels": 652,
  "fetched_at": "2024-01-08 20:00:00",
  "channels": [
    {
      "name": "freeCodeCamp.org",
      "url": "https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ",
      "channel_id": "UC8butISFwT-Wl7EV0hUK0BQ",
      "language": "English",
      "category": "Tutorial",
      "subscriber_count": 8500000,
      "view_count": 500000000,
      "video_count": 1500
    }
  ]
}
```

### Markdown Export

Rich formatted documentation with:
- Channel cards with stats
- Table of contents
- Anchor links
- Formatted numbers
- Categorized sections

## Search & Filter Capabilities

### Filter Parameters

- **By Category:** Tutorial, Informational, Live Coding, etc.
- **By Language:** English, Hindi, Spanish, etc.
- **By Subscriber Count:** > 1M, 100K-1M, 10K-100K, < 10K
- **By Video Count:** Active (> 100 videos), Moderate (10-100), Starting (< 10)
- **By Status:** Active, Up and Coming, Retired

### Sort Options

- Subscriber count (descending/ascending)
- View count (descending/ascending)
- Video count (descending/ascending)
- Channel age (newest/oldest)
- Alphabetical (A-Z/Z-A)

## Implementation Notes

### Channel ID Resolution

YouTube channels can be identified by:

1. **Channel ID** (UC...): Direct lookup
   ```
   https://www.youtube.com/channel/UCxxxxx
   ```

2. **Username** (/user/...): Requires API lookup
   ```
   https://www.youtube.com/user/username
   ```

3. **Custom URL** (/c/... or /@...): Requires API lookup
   ```
   https://www.youtube.com/c/customname
   https://www.youtube.com/@username
   ```

### Data Quality

- All subscriber counts are approximate (YouTube API limitation)
- Hidden subscriber counts show as 0
- Some channels may not have all fields populated
- Retired channels may have outdated stats

### Performance Optimization

1. **Batch Processing:** Process channels in groups of 50
2. **Checkpointing:** Save progress regularly
3. **Rate Limiting:** 0.5s delay between API calls
4. **Caching:** Store API responses to avoid re-fetching
5. **Error Recovery:** Continue on failures, log for retry

## Future Enhancements

- Video-level analytics
- Trending/growth metrics
- Collaborative filtering (similar channels)
- CSV/OPML export formats
- REST API for querying data
- Web interface for browsing
- Automated daily updates
- Email notifications for new channels
- Webhook integrations

## References

- [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3)
- [API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
- [DevYouTubeList Repository](https://github.com/myblackbeanca/DevYouTubeList)
