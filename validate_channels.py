#!/usr/bin/env python3
"""
Validation script for testing channels with Apify
This script prepares test cases for Apify RAG Web Browser
and shows how to validate extracted data
"""

import json
from pathlib import Path
from typing import List, Dict


class ChannelValidator:
    def __init__(self, test_channels_path: str):
        with open(test_channels_path, 'r', encoding='utf-8') as f:
            self.test_data = json.load(f)
        self.channels = self.test_data['channels']

    def generate_apify_queries(self) -> List[Dict]:
        """Generate Apify RAG Web Browser queries for each channel"""
        queries = []

        for channel in self.channels:
            # Query 1: Direct URL fetch
            queries.append({
                'type': 'direct_url',
                'channel_name': channel['name'],
                'query': channel['url'],
                'method': 'Fetch channel page directly',
                'expected_data': [
                    'Channel description',
                    'Subscriber count',
                    'Video count',
                    'Channel name',
                    'Latest video titles'
                ]
            })

            # Query 2: Search-based discovery
            queries.append({
                'type': 'search',
                'channel_name': channel['name'],
                'query': f"YouTube channel {channel['name']} subscribers views",
                'method': 'Search for channel information',
                'expected_data': [
                    'Channel statistics',
                    'Channel URL',
                    'Description snippet',
                    'Verification info'
                ]
            })

        return queries

    def create_test_report(self) -> str:
        """Generate a test report template"""
        report = """# Channel Validation Report

## Test Summary

**Total Channels to Test:** 10
**Test Date:** TBD
**Apify Tool:** RAG Web Browser

## Test Cases

"""
        for idx, channel in enumerate(self.channels, 1):
            report += f"""
### Test Case {idx}: {channel['name']}

**Channel Details:**
- Name: {channel['name']}
- URL: {channel['url']}
- Category: {channel['category']}
- Language: {channel['language']}
- Channel ID: {channel['channel_id']}

**Validation Points:**
- [ ] Channel page loads successfully
- [ ] Subscriber count visible
- [ ] Video count visible
- [ ] Channel description present
- [ ] Latest videos listed
- [ ] Custom URL matches (if applicable)

**Apify Queries:**
1. Direct URL: `{channel['url']}`
2. Search: `YouTube channel {channel['name']}`

**Expected Data Points to Extract:**
- Channel title
- Description
- Subscriber count
- Total views
- Video count
- Latest upload date
- Channel image/thumbnail

**Validation Results:**
```
Status: PENDING
Extracted Data:
- Title: [To be filled]
- Subs: [To be filled]
- Videos: [To be filled]
- Views: [To be filled]
```

---
"""
        return report

    def create_apify_instructions(self) -> str:
        """Create step-by-step instructions for Apify testing"""
        instructions = """# Apify Testing Instructions

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
"""
        return instructions

    def save_all(self, output_dir: Path):
        """Save all validation materials"""
        output_dir.mkdir(exist_ok=True)

        # Save test report template
        report = self.create_test_report()
        (output_dir / 'TEST_REPORT.md').write_text(report, encoding='utf-8')
        print("✅ Saved: TEST_REPORT.md")

        # Save Apify instructions
        instructions = self.create_apify_instructions()
        (output_dir / 'APIFY_TESTING_GUIDE.md').write_text(instructions, encoding='utf-8')
        print("✅ Saved: APIFY_TESTING_GUIDE.md")

        # Save API queries
        queries = self.generate_apify_queries()
        queries_file = output_dir / 'apify_queries.json'
        with open(queries_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_queries': len(queries),
                'queries': queries
            }, f, indent=2, ensure_ascii=False)
        print("✅ Saved: apify_queries.json")


def main():
    test_file = Path(__file__).parent / 'test_channels.json'

    if not test_file.exists():
        print(f"❌ {test_file} not found!")
        print("   Run: python3 test_with_apify.py")
        return

    validator = ChannelValidator(str(test_file))

    output_dir = Path(__file__).parent / 'apify_tests'
    validator.save_all(output_dir)

    print(f"\n{'='*70}")
    print("✅ Apify Testing Materials Generated")
    print(f"{'='*70}\n")

    print(f"📁 Output Directory: {output_dir}\n")

    print("📋 Generated Files:")
    print("   1. TEST_REPORT.md - Validation checklist for all 10 channels")
    print("   2. APIFY_TESTING_GUIDE.md - Complete testing instructions")
    print("   3. apify_queries.json - Query specifications for Apify\n")

    print("🚀 Next Steps:")
    print("   1. Read APIFY_TESTING_GUIDE.md for detailed instructions")
    print("   2. Set up Apify account and API key")
    print("   3. Run RAG Web Browser on each channel")
    print("   4. Fill in TEST_REPORT.md with results")
    print("   5. Validate and compare data\n")

    print("📊 Channels Being Tested:")
    for idx, channel in enumerate(validator.channels, 1):
        print(f"   {idx}. {channel['name']} ({channel['category']}) - {channel['language']}")


if __name__ == '__main__':
    main()
