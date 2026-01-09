#!/usr/bin/env python3
"""
Fetch detailed YouTube data for the 10 test channels
Uses YouTube Data API v3
"""

import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional
import requests


class YouTubeTestFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.results = []

    def extract_channel_id_from_url(self, url: str, channel_id_hint: str) -> Optional[str]:
        """Extract actual channel ID from various YouTube URL formats"""
        # If it's already a channel ID (starts with UC)
        if channel_id_hint.startswith('UC') and len(channel_id_hint) == 24:
            return channel_id_hint

        # If it's a username (starts with @)
        if channel_id_hint.startswith('@'):
            username = channel_id_hint[1:]
            return self.get_channel_id_by_username(username)

        # Try to get from /channel/ URL
        if '/channel/' in url:
            return url.split('/channel/')[1].split('/')[0].split('?')[0]

        # Try username lookup
        if '/user/' in url:
            username = url.split('/user/')[1].split('/')[0].split('?')[0]
            return self.get_channel_id_by_username(username)

        # Try custom URL lookup
        if '/c/' in url:
            custom = url.split('/c/')[1].split('/')[0].split('?')[0]
            return self.get_channel_id_by_username(custom)

        return None

    def get_channel_id_by_username(self, username: str) -> Optional[str]:
        """Get channel ID from username or custom URL"""
        try:
            url = f"{self.base_url}/channels"

            # Try with forHandle (newest method)
            params = {
                'part': 'id',
                'forHandle': username if not username.startswith('@') else username[1:],
                'key': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    return data['items'][0]['id']

            # Try with forUsername (older method)
            params = {
                'part': 'id',
                'forUsername': username,
                'key': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    return data['items'][0]['id']

        except Exception as e:
            print(f"   ⚠️  Error: {e}")

        return None

    def fetch_channel_details(self, channel_id: str) -> Optional[Dict]:
        """Fetch detailed information for a single channel"""
        try:
            url = f"{self.base_url}/channels"
            params = {
                'part': 'snippet,statistics,contentDetails,brandingSettings',
                'id': channel_id,
                'key': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    item = data['items'][0]
                    return {
                        'channel_id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet'].get('description', '')[:300],
                        'custom_url': item['snippet'].get('customUrl', ''),
                        'published_at': item['snippet']['publishedAt'],
                        'country': item['snippet'].get('country', ''),
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
                        'video_count': int(item['statistics'].get('videoCount', 0)),
                        'uploads_playlist_id': item['contentDetails']['relatedPlaylists'].get('uploads', '')
                    }
            elif response.status_code == 403:
                print(f"   ⚠️  API quota exceeded")
                return None

        except Exception as e:
            print(f"   ⚠️  Error: {e}")

        return None

    def fetch_latest_videos(self, uploads_playlist_id: str, max_results: int = 3) -> List[Dict]:
        """Fetch latest videos from uploads playlist"""
        try:
            url = f"{self.base_url}/playlistItems"
            params = {
                'part': 'snippet,contentDetails',
                'playlistId': uploads_playlist_id,
                'maxResults': max_results,
                'key': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                videos = []

                for item in data.get('items', []):
                    videos.append({
                        'video_id': item['contentDetails']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt']
                    })

                return videos

        except Exception as e:
            print(f"   ⚠️  Error fetching videos: {e}")

        return []

    def format_number(self, num: int) -> str:
        """Format large numbers"""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return str(num)

    def test_channels(self, test_channels_path: str) -> Dict:
        """Test all channels from test_channels.json"""
        with open(test_channels_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)

        channels = test_data['channels']
        print(f"🚀 Testing {len(channels)} channels with YouTube API v3\n")

        results = {
            'total_channels': len(channels),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'channels': [],
            'statistics': {
                'success': 0,
                'failed': 0,
                'total_subscribers': 0,
                'total_views': 0,
                'total_videos': 0
            }
        }

        for idx, channel in enumerate(channels, 1):
            print(f"[{idx}/{len(channels)}] {channel['name']}")

            # Resolve channel ID
            channel_id = self.extract_channel_id_from_url(
                channel['url'],
                channel['channel_id']
            )

            if not channel_id:
                print(f"   ❌ Could not resolve channel ID")
                results['statistics']['failed'] += 1
                continue

            # Fetch channel details
            details = self.fetch_channel_details(channel_id)

            if details:
                # Fetch latest videos
                videos = []
                if details.get('uploads_playlist_id'):
                    videos = self.fetch_latest_videos(details['uploads_playlist_id'], max_results=3)
                    details['latest_videos'] = videos

                # Merge data
                result = {
                    **channel,
                    **details
                }

                # Format for display
                subs = self.format_number(details['subscriber_count'])
                views = self.format_number(details['view_count'])
                vids = details['video_count']

                print(f"   ✅ {subs} subs | {views} views | {vids} videos")

                results['channels'].append(result)
                results['statistics']['success'] += 1
                results['statistics']['total_subscribers'] += details['subscriber_count']
                results['statistics']['total_views'] += details['view_count']
                results['statistics']['total_videos'] += details['video_count']
            else:
                print(f"   ❌ Failed to fetch details")
                results['statistics']['failed'] += 1

            # Rate limiting
            time.sleep(0.5)

        return results

    def save_results(self, results: Dict, output_path: str):
        """Save test results to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    def print_summary(self, results: Dict):
        """Print summary statistics"""
        stats = results['statistics']
        print(f"\n{'='*70}")
        print(f"TEST RESULTS SUMMARY")
        print(f"{'='*70}\n")
        print(f"✅ Successfully fetched: {stats['success']}/{results['total_channels']}")
        print(f"❌ Failed: {stats['failed']}/{results['total_channels']}\n")

        if stats['success'] > 0:
            print(f"📊 AGGREGATE STATISTICS:")
            print(f"   Total Subscribers: {self.format_number(stats['total_subscribers'])}")
            print(f"   Total Views: {self.format_number(stats['total_views'])}")
            print(f"   Total Videos: {stats['total_videos']:,}\n")

            print(f"   Average per Channel:")
            print(f"   - Subscribers: {self.format_number(stats['total_subscribers'] // stats['success'])}")
            print(f"   - Views: {self.format_number(stats['total_views'] // stats['success'])}")
            print(f"   - Videos: {stats['total_videos'] // stats['success']}\n")

        print(f"💾 Results saved to: test_results.json")


def main():
    # Get API key from environment
    api_key = os.getenv('YOUTUBE_API_KEY')

    if not api_key:
        print("❌ YOUTUBE_API_KEY environment variable not set!")
        print("\n📝 To set up:")
        print("   1. Get key from: https://console.cloud.google.com/")
        print("   2. Export it: export YOUTUBE_API_KEY='your-key-here'")
        print("   3. Run this script again\n")
        return

    test_file = Path(__file__).parent / 'test_channels.json'

    if not test_file.exists():
        print(f"❌ {test_file} not found!")
        return

    fetcher = YouTubeTestFetcher(api_key)
    results = fetcher.test_channels(str(test_file))

    output_file = Path(__file__).parent / 'test_results.json'
    fetcher.save_results(results, str(output_file))

    fetcher.print_summary(results)


if __name__ == '__main__':
    main()
