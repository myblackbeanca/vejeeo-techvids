#!/usr/bin/env python3
"""
Display and analyze test results from YouTube API testing
"""

import json
from pathlib import Path
from typing import Dict
import sys


class ResultsDisplay:
    def __init__(self, results_path: str):
        with open(results_path, 'r', encoding='utf-8') as f:
            self.results = json.load(f)

    def format_number(self, num: int) -> str:
        """Format large numbers with K, M, B suffixes"""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return str(num)

    def display_header(self):
        """Display test header"""
        print("\n" + "="*80)
        print("📺 YOUTUBE CHANNEL TEST RESULTS".center(80))
        print("="*80)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Total Channels Tested: {self.results['total_channels']}")
        print("="*80 + "\n")

    def display_summary(self):
        """Display summary statistics"""
        stats = self.results['statistics']

        print("📊 SUMMARY STATISTICS\n")
        print(f"   ✅ Successfully Tested: {stats['success']}/{self.results['total_channels']}")
        print(f"   ❌ Failed: {stats['failed']}/{self.results['total_channels']}\n")

        if stats['success'] > 0:
            print(f"   Total Subscribers: {self.format_number(stats['total_subscribers'])}")
            print(f"   Total Views: {self.format_number(stats['total_views'])}")
            print(f"   Total Videos: {stats['total_videos']:,}\n")

            print(f"   Average per Channel:")
            print(f"      Subscribers: {self.format_number(stats['total_subscribers'] // stats['success'])}")
            print(f"      Views: {self.format_number(stats['total_views'] // stats['success'])}")
            print(f"      Videos: {stats['total_videos'] // stats['success']}")

        print()

    def display_leaderboard(self):
        """Display channels ranked by subscribers"""
        print("🏆 CHANNEL LEADERBOARD (By Subscribers)\n")

        # Sort by subscribers
        sorted_channels = sorted(
            self.results['channels'],
            key=lambda x: x['subscriber_count'],
            reverse=True
        )

        print(f"{'Rank':<5} {'Channel':<30} {'Subs':<12} {'Views':<12} {'Videos':<8}")
        print("-" * 80)

        for idx, channel in enumerate(sorted_channels, 1):
            name = channel['name'][:28]
            subs = self.format_number(channel['subscriber_count'])
            views = self.format_number(channel['view_count'])
            videos = channel['video_count']

            print(f"{idx:<5} {name:<30} {subs:>11} {views:>11} {videos:>7}")

        print()

    def display_detailed_cards(self):
        """Display detailed card for each channel"""
        print("📋 DETAILED CHANNEL INFORMATION\n")

        for idx, channel in enumerate(self.results['channels'], 1):
            self.display_channel_card(idx, channel)

    def display_channel_card(self, idx: int, channel: Dict):
        """Display a detailed card for one channel"""
        print(f"\n[{idx}] {channel['name']}")
        print("-" * 80)

        print(f"  📌 Category: {channel['category']}")
        print(f"  🌍 Language: {channel['language']}")
        if channel.get('country'):
            print(f"  🗺️  Country: {channel['country']}")

        print(f"\n  📊 Statistics:")
        print(f"     👥 Subscribers: {self.format_number(channel['subscriber_count'])}")
        print(f"     👁️  Total Views: {self.format_number(channel['view_count'])}")
        print(f"     🎬 Videos: {channel['video_count']}")
        print(f"     📅 Created: {channel['published_at'][:10]}")

        print(f"\n  📝 Description:")
        desc = channel['description']
        if len(desc) > 76:
            print(f"     {desc[:73]}...")
        else:
            print(f"     {desc}")

        # Display latest videos
        if channel.get('latest_videos'):
            print(f"\n  🎥 Latest Videos:")
            for video in channel['latest_videos'][:3]:
                title = video['title'][:60]
                date = video['published_at'][:10]
                print(f"     • {title}")
                print(f"       📅 {date}")

        print()

    def display_category_breakdown(self):
        """Display breakdown by category"""
        print("\n📁 BREAKDOWN BY CATEGORY\n")

        categories = {}
        for channel in self.results['channels']:
            cat = channel['category']
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'subs': 0,
                    'views': 0
                }
            categories[cat]['count'] += 1
            categories[cat]['subs'] += channel['subscriber_count']
            categories[cat]['views'] += channel['view_count']

        print(f"{'Category':<25} {'Count':<8} {'Subscribers':<15} {'Views':<15}")
        print("-" * 75)

        for cat in sorted(categories.keys()):
            data = categories[cat]
            subs = self.format_number(data['subs'])
            views = self.format_number(data['views'])
            print(f"{cat:<25} {data['count']:<8} {subs:>14} {views:>14}")

        print()

    def display_language_breakdown(self):
        """Display breakdown by language"""
        print("\n🌐 BREAKDOWN BY LANGUAGE\n")

        languages = {}
        for channel in self.results['channels']:
            lang = channel['language']
            if lang not in languages:
                languages[lang] = {
                    'count': 0,
                    'subs': 0,
                    'channels': []
                }
            languages[lang]['count'] += 1
            languages[lang]['subs'] += channel['subscriber_count']
            languages[lang]['channels'].append(channel['name'])

        print(f"{'Language':<20} {'Count':<8} {'Total Subscribers':<20} {'Channels'}")
        print("-" * 80)

        for lang in sorted(languages.keys()):
            data = languages[lang]
            subs = self.format_number(data['subs'])
            channels = ', '.join(data['channels'][:3])
            if len(data['channels']) > 3:
                channels += f" (+{len(data['channels']) - 3} more)"

            print(f"{lang:<20} {data['count']:<8} {subs:>19} {channels}")

        print()

    def display_insights(self):
        """Display interesting insights"""
        print("\n💡 KEY INSIGHTS\n")

        channels = self.results['channels']
        stats = self.results['statistics']

        # Top channel
        top = max(channels, key=lambda x: x['subscriber_count'])
        print(f"  🥇 Largest Channel: {top['name']}")
        print(f"     Subscribers: {self.format_number(top['subscriber_count'])}")
        print(f"     Views: {self.format_number(top['view_count'])}")

        # Most videos
        most_vids = max(channels, key=lambda x: x['video_count'])
        print(f"\n  📺 Most Prolific: {most_vids['name']}")
        print(f"     Videos: {most_vids['video_count']}")

        # Highest engagement (views per video)
        engagement = [
            (c['name'], c['view_count'] / max(c['video_count'], 1))
            for c in channels
        ]
        engagement.sort(key=lambda x: x[1], reverse=True)
        print(f"\n  🔥 Highest Engagement (views/video): {engagement[0][0]}")
        print(f"     Avg Views/Video: {engagement[0][1]:,.0f}")

        # Newest channel
        newest = min(channels, key=lambda x: x['published_at'])
        print(f"\n  🆕 Newest Channel: {newest['name']}")
        print(f"     Created: {newest['published_at'][:10]}")

        print()

    def display_export_instructions(self):
        """Display instructions for exporting data"""
        print("\n📤 EXPORT OPTIONS\n")
        print("  JSON Export:")
        print(f"    Available in: test_results_mock.json\n")
        print("  To merge with main database:")
        print("    python3 merge_test_results.py\n")
        print("  To generate markdown documentation:")
        print("    python3 generate_markdown.py\n")


def main():
    results_file = Path(__file__).parent / 'test_results_mock.json'

    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        sys.exit(1)

    display = ResultsDisplay(str(results_file))

    display.display_header()
    display.display_summary()
    display.display_leaderboard()
    display.display_category_breakdown()
    display.display_language_breakdown()
    display.display_detailed_cards()
    display.display_insights()
    display.display_export_instructions()

    print("="*80)
    print("✅ Test Results Analysis Complete".center(80))
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
