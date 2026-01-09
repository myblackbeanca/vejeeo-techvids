#!/usr/bin/env python3
"""
Test channels using Apify's RAG Web Browser
Extract channel information from top 10 channels
"""

import json
from pathlib import Path


def get_top_10_channels():
    """Get the top 10 channels by subscriber count"""
    channels_file = Path(__file__).parent / 'channels_data.json'

    if not channels_file.exists():
        print("❌ channels_data.json not found. Run parse_channels.py first!")
        return []

    with open(channels_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    channels = data['channels']

    # Sort by name to get a diverse sample
    sample = [
        channels[0],   # freeCodeCamp.org
        channels[10],  # Traversy Media
        channels[20],  # The Net Ninja
        channels[30],  # Academind
        channels[50],  # Corey Schafer
        channels[100], # Ben Awad
        channels[150], # Fireship
        channels[200], # Web Dev Simplified
        channels[300], # Programming with Mosh
        channels[400], # Code with Ania Kubów
    ]

    return sample


def print_channel_info(channel):
    """Print channel information in a readable format"""
    print(f"\n{'='*70}")
    print(f"📺 Channel: {channel.get('name', 'Unknown')}")
    print(f"{'='*70}")
    print(f"URL: {channel.get('url', 'N/A')}")
    print(f"Category: {channel.get('category', 'Unknown')}")
    print(f"Language: {channel.get('language', 'Unknown')}")
    print(f"Channel ID: {channel.get('channel_id', 'N/A')}")
    print()


def main():
    print("🚀 Vejeeo TechVids - Apify Test")
    print("=" * 70)
    print("\nFetching top 10 diverse channels for testing...\n")

    channels = get_top_10_channels()

    if not channels:
        return

    print(f"✅ Selected {len(channels)} channels for testing:\n")

    urls_to_test = []

    for idx, channel in enumerate(channels, 1):
        print_channel_info(channel)
        print(f"[{idx}] Testing with Apify RAG Web Browser")
        urls_to_test.append({
            'index': idx,
            'name': channel.get('name', 'Unknown'),
            'url': channel.get('url', ''),
            'channel_id': channel.get('channel_id', ''),
            'category': channel.get('category', 'Unknown'),
            'language': channel.get('language', 'Unknown')
        })

    # Save test list
    test_file = Path(__file__).parent / 'test_channels.json'
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(urls_to_test),
            'channels': urls_to_test,
            'notes': 'These 10 channels have been selected for Apify testing'
        }, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"✅ Test channels saved to: {test_file}")
    print(f"\n📝 To test with Apify RAG Web Browser:")
    print("   1. Each channel URL can be passed to the RAG Web Browser")
    print("   2. Extract channel metadata, description, video info")
    print("   3. Validate against our YouTube API data")
    print("\n🔗 Sample Apify calls:")

    for channel_info in urls_to_test[:3]:
        print(f"\n   Channel: {channel_info['name']}")
        print(f"   Query: YouTube channel {channel_info['name']} subscribers videos")
        print(f"   Direct URL: {channel_info['url']}")


if __name__ == '__main__':
    main()
