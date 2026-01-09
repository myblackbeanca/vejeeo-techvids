#!/usr/bin/env python3
"""
Parse DevYouTubeList README.md and extract all channel information
"""

import re
import json
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse, parse_qs


class ChannelParser:
    def __init__(self, readme_path: str):
        self.readme_path = readme_path
        self.channels = []
        self.current_language = None
        self.current_category = None

    def extract_channel_id(self, url: str) -> str:
        """Extract channel ID from YouTube URL"""
        parsed = urlparse(url)

        # Handle /channel/ URLs
        if '/channel/' in url:
            return url.split('/channel/')[1].split('/')[0].split('?')[0]

        # Handle /user/ URLs
        if '/user/' in url:
            username = url.split('/user/')[1].split('/')[0].split('?')[0]
            return f"@{username}"

        # Handle /c/ URLs
        if '/c/' in url:
            custom = url.split('/c/')[1].split('/')[0].split('?')[0]
            return f"@{custom}"

        # Handle /@username URLs
        if '/@' in url:
            username = url.split('/@')[1].split('/')[0].split('?')[0]
            return f"@{username}"

        # Handle bare domain URLs
        if parsed.path and len(parsed.path) > 1:
            path_parts = parsed.path.strip('/').split('/')
            if path_parts:
                return f"@{path_parts[0]}"

        return url

    def parse_markdown_link(self, line: str) -> List[Dict]:
        """Extract all markdown links from a line"""
        # Pattern: [Channel Name](URL)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(pattern, line)

        results = []
        for name, url in matches:
            if 'youtube.com' in url or 'youtu.be' in url:
                channel_id = self.extract_channel_id(url)
                results.append({
                    'name': name.strip(),
                    'url': url.strip(),
                    'channel_id': channel_id,
                    'language': self.current_language,
                    'category': self.current_category
                })

        return results

    def parse(self):
        """Parse the README.md file"""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            # Detect language sections
            if line.startswith('##') and not line.startswith('###'):
                # Extract language
                lang = line.replace('#', '').strip()
                if lang == "Russian":
                    self.current_language = "Russian"
                elif lang == "Hindi":
                    self.current_language = "Hindi"
                elif lang == "Turkish":
                    self.current_language = "Turkish"
                elif lang == "Italian":
                    self.current_language = "Italian"
                elif lang == "Bengali":
                    self.current_language = "Bengali"
                elif lang == "Brazilian":
                    self.current_language = "Brazilian Portuguese"
                elif lang == "Korean":
                    self.current_language = "Korean"
                elif lang == "Chinese":
                    self.current_language = "Chinese"
                elif lang == "Hebrew":
                    self.current_language = "Hebrew"
                elif lang == "French":
                    self.current_language = "French"
                elif lang == "Farsi":
                    self.current_language = "Farsi"
                elif lang == "Spanish":
                    self.current_language = "Spanish"
                elif lang == "Catalan":
                    self.current_language = "Catalan"
                elif lang == "Indonesian":
                    self.current_language = "Indonesian"
                elif lang == "Arabic":
                    self.current_language = "Arabic"
                elif lang == "German":
                    self.current_language = "German"
                elif lang == "Polish":
                    self.current_language = "Polish"
                elif lang == "Somali":
                    self.current_language = "Somali"
                elif lang == "Vietnam":
                    self.current_language = "Vietnamese"
                elif lang == "Uzbek":
                    self.current_language = "Uzbek"
                elif lang == "Non English":
                    self.current_language = None
                else:
                    self.current_language = "English"

            # Detect category sections
            elif line.startswith('###'):
                self.current_category = line.replace('#', '').strip()
                if not self.current_language:
                    self.current_language = "English"

            # Parse channel links
            elif line.startswith('*'):
                channels = self.parse_markdown_link(line)
                self.channels.extend(channels)

        return self.channels

    def save_to_json(self, output_path: str):
        """Save parsed channels to JSON"""
        data = {
            'total_channels': len(self.channels),
            'channels': self.channels
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_stats(self):
        """Get statistics about parsed channels"""
        stats = {
            'total': len(self.channels),
            'by_language': {},
            'by_category': {}
        }

        for channel in self.channels:
            lang = channel['language'] or 'Unknown'
            cat = channel['category'] or 'Uncategorized'

            stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
            stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1

        return stats


def main():
    # Path to the cloned DevYouTubeList README
    readme_path = Path(__file__).parent.parent / 'DevYouTubeList' / 'README.md'

    parser = ChannelParser(str(readme_path))
    channels = parser.parse()

    print(f"✅ Parsed {len(channels)} channels")

    # Save to JSON
    output_json = Path(__file__).parent / 'channels_data.json'
    parser.save_to_json(str(output_json))
    print(f"✅ Saved to {output_json}")

    # Print statistics
    stats = parser.get_stats()
    print(f"\n📊 Statistics:")
    print(f"   Total channels: {stats['total']}")
    print(f"\n   By Language:")
    for lang, count in sorted(stats['by_language'].items(), key=lambda x: x[1], reverse=True):
        print(f"      {lang}: {count}")
    print(f"\n   By Category:")
    for cat, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"      {cat}: {count}")


if __name__ == '__main__':
    main()
