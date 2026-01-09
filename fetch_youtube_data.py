#!/usr/bin/env python3
"""
Fetch detailed YouTube channel information using YouTube Data API v3
"""

import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional
import requests


class YouTubeAPIFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.channels_fetched = 0
        self.failed_channels = []

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

            # Try with forUsername instead
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
            print(f"   ⚠️  Error fetching channel ID for {username}: {e}")

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
                        'description': item['snippet'].get('description', ''),
                        'custom_url': item['snippet'].get('customUrl', ''),
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnails': item['snippet']['thumbnails'],
                        'country': item['snippet'].get('country', ''),
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
                        'hidden_subscriber_count': item['statistics'].get('hiddenSubscriberCount', False),
                        'video_count': int(item['statistics'].get('videoCount', 0)),
                        'keywords': item['brandingSettings'].get('channel', {}).get('keywords', ''),
                        'uploads_playlist_id': item['contentDetails']['relatedPlaylists'].get('uploads', '')
                    }
            elif response.status_code == 403:
                print(f"   ⚠️  API quota exceeded or permission denied")
                return None
            else:
                print(f"   ⚠️  API returned status {response.status_code}")

        except Exception as e:
            print(f"   ⚠️  Error fetching channel {channel_id}: {e}")

        return None

    def fetch_latest_videos(self, uploads_playlist_id: str, max_results: int = 10) -> List[Dict]:
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
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail': item['snippet']['thumbnails'].get('default', {}).get('url', '')
                    })

                return videos

        except Exception as e:
            print(f"   ⚠️  Error fetching videos: {e}")

        return []

    def enrich_channels(self, channels_data_path: str, output_path: str):
        """Enrich channel data with YouTube API information"""
        with open(channels_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        enriched_channels = []
        total = len(data['channels'])

        print(f"🚀 Starting to fetch data for {total} channels...")
        print(f"⏰ This may take a while due to API rate limits\n")

        for idx, channel in enumerate(data['channels'], 1):
            print(f"[{idx}/{total}] Fetching: {channel['name']}")

            # Extract channel ID
            channel_id = self.extract_channel_id_from_url(channel['url'], channel['channel_id'])

            if not channel_id:
                print(f"   ❌ Could not determine channel ID")
                self.failed_channels.append(channel)
                continue

            # Fetch channel details
            details = self.fetch_channel_details(channel_id)

            if details:
                # Fetch latest videos
                if details.get('uploads_playlist_id'):
                    latest_videos = self.fetch_latest_videos(details['uploads_playlist_id'], max_results=5)
                    details['latest_videos'] = latest_videos

                # Merge with original data
                enriched = {**channel, **details}
                enriched_channels.append(enriched)

                self.channels_fetched += 1
                print(f"   ✅ Subscribers: {details['subscriber_count']:,} | Videos: {details['video_count']:,}")
            else:
                print(f"   ❌ Failed to fetch details")
                self.failed_channels.append(channel)

            # Rate limiting: YouTube API allows 10,000 units per day
            # Each request uses ~4 units, so we can make ~2,500 requests
            # Add small delay to be safe
            time.sleep(0.5)

            # Save progress every 50 channels
            if idx % 50 == 0:
                self.save_progress(output_path, enriched_channels, idx, total)

        # Final save
        self.save_final(output_path, enriched_channels)

        print(f"\n{'='*60}")
        print(f"✅ Successfully fetched: {self.channels_fetched}/{total}")
        print(f"❌ Failed: {len(self.failed_channels)}")
        print(f"💾 Saved to: {output_path}")

        if self.failed_channels:
            failed_path = Path(output_path).parent / 'failed_channels.json'
            with open(failed_path, 'w', encoding='utf-8') as f:
                json.dump({'failed': self.failed_channels}, f, indent=2, ensure_ascii=False)
            print(f"⚠️  Failed channels saved to: {failed_path}")

    def save_progress(self, output_path: str, channels: List[Dict], current: int, total: int):
        """Save progress checkpoint"""
        checkpoint_data = {
            'progress': f"{current}/{total}",
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_enriched': len(channels),
            'channels': channels
        }

        checkpoint_path = str(output_path).replace('.json', '_checkpoint.json')
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

        print(f"   💾 Progress checkpoint saved")

    def save_final(self, output_path: str, channels: List[Dict]):
        """Save final enriched data"""
        final_data = {
            'total_channels': len(channels),
            'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'channels': channels
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)


def main():
    # Get API key from environment variable
    api_key = os.getenv('YOUTUBE_API_KEY')

    if not api_key:
        print("❌ YOUTUBE_API_KEY environment variable not set!")
        print("\n📝 To get a YouTube API key:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create a new project or select existing")
        print("   3. Enable YouTube Data API v3")
        print("   4. Create credentials (API Key)")
        print("   5. Export it: export YOUTUBE_API_KEY='your-key-here'")
        print("\n💡 Then run this script again")
        return

    channels_data = Path(__file__).parent / 'channels_data.json'
    output_file = Path(__file__).parent / 'enriched_channels.json'

    if not channels_data.exists():
        print(f"❌ Channels data file not found: {channels_data}")
        print("   Run parse_channels.py first!")
        return

    fetcher = YouTubeAPIFetcher(api_key)
    fetcher.enrich_channels(str(channels_data), str(output_file))


if __name__ == '__main__':
    main()
