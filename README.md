# Vejeeo TechVids

A comprehensive YouTube Tech Video Data Pipeline for extracting, enriching, and documenting developer YouTube channels.

## Overview

This project provides a complete pipeline to:

- **Parse YouTube channel lists** - Extract 650+ developer YouTube channels from curated lists
- **Fetch detailed metadata** - Channel info, subscribers, views, descriptions, categories
- **Enrich with analytics** - Growth tracking, engagement metrics, upload frequency, latest videos
- **Generate documentation** - Comprehensive markdown files organized by category, language, and rankings
- **Export in multiple formats** - JSON for APIs, Markdown for documentation

## Features

- 🎯 **652 Developer Channels** - Curated list across multiple languages and categories
- 📊 **Rich Analytics** - Subscriber counts, view counts, video counts, and more
- 🌍 **Multi-language Support** - Channels in 21+ languages
- 📁 **Multiple Categorization** - Tutorial, Informational, Live Coding, AI/ML, Game Dev, etc.
- 🚀 **Easy to Use** - Simple Python scripts with clear documentation

## Project Structure

```
vejeeo-techvids/
├── parse_channels.py          # Parse channel names/URLs from README
├── fetch_youtube_data.py      # Fetch detailed data from YouTube API
├── generate_markdown.py       # Generate comprehensive markdown docs
├── requirements.txt           # Python dependencies
├── channels_data.json         # Parsed channel data (652 channels)
├── enriched_channels.json     # Enriched with YouTube API data
└── docs/                      # Generated markdown documentation
    ├── CHANNELS_BY_CATEGORY.md
    ├── CHANNELS_BY_LANGUAGE.md
    ├── TOP_100_CHANNELS.md
    └── STATISTICS.md
```

## Getting Started

### Prerequisites

- **Python 3.8+**
- **YouTube Data API v3 key** ([Get one here](https://console.cloud.google.com/))

### Installation

1. Clone this repository:
```bash
cd vejeeo-techvids
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your YouTube API Key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable **YouTube Data API v3**
   - Create credentials (API Key)
   - Set environment variable:
   ```bash
   export YOUTUBE_API_KEY='your-api-key-here'
   ```

### Usage

#### Step 1: Parse Channel Data

Extract channel names and URLs from the DevYouTubeList repository:

```bash
python3 parse_channels.py
```

**Output:** `channels_data.json` - Contains 652 channels with names, URLs, categories, and languages

#### Step 2: Fetch YouTube Data (Optional)

Enrich channels with detailed YouTube API data:

```bash
python3 fetch_youtube_data.py
```

**Note:** This requires a YouTube API key and may take 5-10 minutes due to API rate limits.

**Output:** `enriched_channels.json` - Contains full channel details including:
- Subscriber counts
- Total view counts
- Video counts
- Channel descriptions
- Latest videos
- Creation dates
- And more...

#### Step 3: Generate Documentation

Create comprehensive markdown documentation:

```bash
python3 generate_markdown.py
```

**Output:** Multiple markdown files in `docs/` directory:
- `CHANNELS_BY_CATEGORY.md` - Channels organized by category
- `CHANNELS_BY_LANGUAGE.md` - Channels organized by language
- `TOP_100_CHANNELS.md` - Top 100 channels by subscribers
- `STATISTICS.md` - Overall statistics and breakdowns

## Data Insights

### Channel Distribution

- **Total Channels:** 652
- **Languages:** 21+ (English, Hindi, Spanish, Portuguese, Arabic, Korean, etc.)
- **Categories:** Tutorial, Informational, Live Coding, AI/ML, Game Development, and more

### Top Categories

1. **Tutorial** - 326 channels (50%)
2. **Informational** - 59 channels
3. **Up And Coming** - 50 channels
4. **Web Development** - 47 channels
5. **Live Coding** - 34 channels

### Top Languages

1. **English** - 354 channels (54%)
2. **Brazilian Portuguese** - 72 channels
3. **Arabic** - 30 channels
4. **Bengali** - 29 channels
5. **Turkish** - 27 channels

## API Rate Limits

YouTube Data API has the following limits:
- **10,000 units per day** (default quota)
- Each API call uses 1-4 units
- The fetch script includes automatic rate limiting and checkpoints

**Pro Tip:** The script saves progress every 50 channels, so you can stop and resume anytime!

## Contributing

Contributions are welcome! Areas for improvement:

- Add more data sources
- Implement video-level analytics
- Add trending/growth metrics
- Create web interface
- Add export to CSV/OPML formats

## Data Source

Channel list sourced from [DevYouTubeList](https://github.com/myblackbeanca/DevYouTubeList) - A curated list of amazing development channels on YouTube.

## License

MIT

## Acknowledgments

- All the amazing YouTube creators who make developer education accessible
- The DevYouTubeList community for curating the channel list
