# Apify Testing Instructions

## Overview

This document explains how to test the 10 YouTube channels using Apify's RAG Web Browser.

## Setup

1. **Prepare Apify Account**
   - Sign up at https://apify.com
   - Get your API token

2. **Install Apify SDK** (Optional)
   ```bash
   npm install -g apify-cli
   apify login
   ```

## Testing Process

### Method 1: Direct URL Fetching

For each channel, use the RAG Web Browser with the direct YouTube URL:

```bash
# Example: freeCodeCamp.org
Query: https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ
Max Results: 1
Output: Markdown
```

**What to Extract:**
- Channel name from page title
- Subscriber count (usually visible in About section)
- "Join" button text if available
- Video count from "Videos" tab
- Channel description
- Recent video titles

### Method 2: Search-Based Discovery

Use search queries to find and verify channels:

```bash
Query: "YouTube channel [Channel Name] subscribers"
Max Results: 3
Output: Markdown
```

**What to Look For:**
- Official channel link
- Subscriber count in results
- Channel description preview
- Verification badges

### Method 3: Cross-Validation

Compare data from multiple sources:

1. **Direct URL Data** → RAG Web Browser
2. **Search Results** → RAG Web Browser
3. **Our JSON Data** → channels_data.json or enriched_channels.json
4. **Validate Matches**

## Channel Test List

| # | Channel | Type | URL |
|---|---------|------|-----|
| 1 | freeCodeCamp.org | Tutorial | https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ |
| 2 | Academind | Tutorial | https://www.youtube.com/channel/UCSJbGtTlrDami-tDGPUV9-w |
| 3 | Hitesh Choudhary | Tutorial | https://www.youtube.com/user/hiteshitube |
| 4 | Chris Coyier | Tutorial | https://www.youtube.com/user/realcsstricks |
| 5 | Chris Courses | Tutorial | https://www.youtube.com/channel/UC9Yp2yz6-pwhQuPlIDV_mjA |
| 6 | Harry Wolff | Tutorial | https://www.youtube.com/c/hswolff |
| 7 | Benjamin N. Spak | Informational | https://www.youtube.com/user/bnspak |
| 8 | ThinMatrix | Game Dev | https://www.youtube.com/user/ThinMatrix |
| 9 | TheDevWay | Up and Coming | https://www.youtube.com/channel/UC76ftuGpHJnEtsEBefT4YUQ |
| 10 | Emrah Yuksel | Tutorial | https://www.youtube.com/channel/UC2u9Gc37Rq44dB3mW4Kdi-w |

## Expected Data to Collect

For each channel, Apify should extract:

1. **Channel Metadata**
   - Official name
   - Custom URL (if any)
   - Creation date
   - Location/Country

2. **Statistics**
   - Total subscribers
   - Total channel views
   - Total videos
   - Verification status

3. **Content**
   - Channel description
   - Category tags
   - Featured content
   - Latest videos (title, date, view count)

4. **Media**
   - Channel banner
   - Profile picture
   - Thumbnail images

## Data Validation Checklist

- [ ] All 10 channels successfully fetched
- [ ] Subscriber counts extracted
- [ ] Video counts extracted
- [ ] Channel descriptions obtained
- [ ] No data discrepancies found
- [ ] Cross-validation passed
- [ ] Data formatted correctly
- [ ] Report generated
- [ ] Results logged

## Integration with Pipeline

### Step 1: Run Apify Tests
```bash
# Use RAG Web Browser for each channel
# Save results to apify_results.json
```

### Step 2: Validate Results
```bash
python3 validate_apify_results.py
```

### Step 3: Enrich Database
```bash
# Merge Apify data with existing channels_data.json
python3 merge_apify_data.py
```

## Example: Manual Testing

### Test Channel: freeCodeCamp.org

1. **Direct URL Test**
   - URL: https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ
   - Expected: Channel page with stats
   - Apify Query: Direct fetch of channel URL

2. **Search Test**
   - Query: "freeCodeCamp YouTube channel subscribers"
   - Expected: Multiple results with channel stats
   - Apify Query: Search and analyze results

3. **Validation**
   - Subscriber count should be ~8.5M
   - Video count should be ~1500+
   - Channel created: ~2014
   - Description: Educational coding content

## Troubleshooting

### Common Issues

1. **Page Not Loading**
   - Try with different user-agent
   - Check if channel is public
   - Verify URL format

2. **Statistics Not Visible**
   - May need to click "About" tab
   - Some stats are dynamic (JavaScript)
   - Try mobile vs desktop view

3. **Rate Limiting**
   - Space out requests (1-2 sec apart)
   - Use Apify queue for batching
   - Check API quota

## Results Storage

Save Apify results as:
```json
{
  "test_date": "2024-01-08",
  "total_channels": 10,
  "results": [
    {
      "channel": "freeCodeCamp.org",
      "status": "success",
      "data": {
        "subscribers": "8500000",
        "videos": "1500",
        "description": "...",
        "verified": true
      }
    }
  ]
}
```

## Next Steps

After testing:
1. Compare Apify results with YouTube API data
2. Document discrepancies
3. Update validation rules
4. Generate final report
5. Integrate validated data into pipeline

---

**Created:** 2024-01-08
**Purpose:** Testing and validation of 10 YouTube channels
**Status:** Ready for testing
