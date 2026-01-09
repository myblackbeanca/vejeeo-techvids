#!/usr/bin/env python3
"""
Generate comprehensive markdown documentation from enriched channel data
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class MarkdownGenerator:
    def __init__(self, enriched_data_path: str):
        with open(enriched_data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.channels = self.data['channels']

    def format_number(self, num: int) -> str:
        """Format large numbers with K, M, B suffixes"""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return str(num)

    def format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y')
        except:
            return date_str

    def generate_channel_card(self, channel: Dict) -> str:
        """Generate markdown for a single channel"""
        name = channel.get('title', channel.get('name', 'Unknown'))
        url = channel.get('url', '')
        description = channel.get('description', '')[:200] + ('...' if len(channel.get('description', '')) > 200 else '')

        subs = self.format_number(channel.get('subscriber_count', 0))
        views = self.format_number(channel.get('view_count', 0))
        videos = channel.get('video_count', 0)

        language = channel.get('language', 'Unknown')
        category = channel.get('category', 'Uncategorized')
        published = self.format_date(channel.get('published_at', ''))

        card = f"""
### [{name}]({url})

**Category:** {category} | **Language:** {language}

**Stats:**
- 👥 Subscribers: {subs}
- 👁️  Total Views: {views}
- 🎬 Videos: {videos}
- 📅 Created: {published}

**Description:**
{description}

**Channel ID:** `{channel.get('channel_id', 'N/A')}`

---
"""
        return card

    def generate_by_category(self) -> str:
        """Generate markdown organized by category"""
        # Group channels by category
        by_category = {}
        for channel in self.channels:
            cat = channel.get('category', 'Uncategorized')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(channel)

        # Sort by subscriber count within each category
        for cat in by_category:
            by_category[cat].sort(key=lambda x: x.get('subscriber_count', 0), reverse=True)

        md = "# YouTube Tech Channels by Category\n\n"
        md += f"**Total Channels:** {len(self.channels)}\n\n"
        md += "## Table of Contents\n\n"

        # Generate TOC
        for cat in sorted(by_category.keys()):
            anchor = cat.lower().replace(' ', '-').replace('&', 'and')
            md += f"- [{cat} ({len(by_category[cat])})](#{anchor})\n"

        md += "\n---\n\n"

        # Generate content
        for cat in sorted(by_category.keys()):
            md += f"## {cat}\n\n"
            md += f"**Total:** {len(by_category[cat])} channels\n\n"

            for channel in by_category[cat]:
                md += self.generate_channel_card(channel)

            md += "\n\n"

        return md

    def generate_by_language(self) -> str:
        """Generate markdown organized by language"""
        # Group channels by language
        by_language = {}
        for channel in self.channels:
            lang = channel.get('language', 'Unknown')
            if lang not in by_language:
                by_language[lang] = []
            by_language[lang].append(channel)

        # Sort by subscriber count within each language
        for lang in by_language:
            by_language[lang].sort(key=lambda x: x.get('subscriber_count', 0), reverse=True)

        md = "# YouTube Tech Channels by Language\n\n"
        md += f"**Total Channels:** {len(self.channels)}\n\n"
        md += "## Table of Contents\n\n"

        # Generate TOC
        for lang in sorted(by_language.keys()):
            anchor = lang.lower().replace(' ', '-')
            md += f"- [{lang} ({len(by_language[lang])})](#{anchor})\n"

        md += "\n---\n\n"

        # Generate content
        for lang in sorted(by_language.keys()):
            md += f"## {lang}\n\n"
            md += f"**Total:** {len(by_language[lang])} channels\n\n"

            for channel in by_language[lang]:
                md += self.generate_channel_card(channel)

            md += "\n\n"

        return md

    def generate_top_channels(self, limit: int = 100) -> str:
        """Generate markdown for top channels by subscribers"""
        sorted_channels = sorted(self.channels, key=lambda x: x.get('subscriber_count', 0), reverse=True)[:limit]

        md = f"# Top {limit} YouTube Tech Channels\n\n"
        md += f"**Ranked by Subscriber Count**\n\n"
        md += "| Rank | Channel | Subscribers | Videos | Views | Language | Category |\n"
        md += "|------|---------|-------------|--------|-------|----------|----------|\n"

        for idx, channel in enumerate(sorted_channels, 1):
            name = channel.get('title', channel.get('name', 'Unknown'))
            url = channel.get('url', '')
            subs = self.format_number(channel.get('subscriber_count', 0))
            views = self.format_number(channel.get('view_count', 0))
            videos = channel.get('video_count', 0)
            lang = channel.get('language', 'Unknown')
            cat = channel.get('category', 'Uncategorized')

            md += f"| {idx} | [{name}]({url}) | {subs} | {videos} | {views} | {lang} | {cat} |\n"

        md += "\n"
        return md

    def generate_stats(self) -> str:
        """Generate statistics markdown"""
        total_subs = sum(c.get('subscriber_count', 0) for c in self.channels)
        total_views = sum(c.get('view_count', 0) for c in self.channels)
        total_videos = sum(c.get('video_count', 0) for c in self.channels)

        avg_subs = total_subs // len(self.channels)
        avg_views = total_views // len(self.channels)
        avg_videos = total_videos // len(self.channels)

        md = "# YouTube Tech Channels Statistics\n\n"
        md += "## Overall Stats\n\n"
        md += f"- **Total Channels:** {len(self.channels):,}\n"
        md += f"- **Total Subscribers:** {self.format_number(total_subs)}\n"
        md += f"- **Total Views:** {self.format_number(total_views)}\n"
        md += f"- **Total Videos:** {total_videos:,}\n\n"

        md += "## Averages\n\n"
        md += f"- **Avg Subscribers per Channel:** {self.format_number(avg_subs)}\n"
        md += f"- **Avg Views per Channel:** {self.format_number(avg_views)}\n"
        md += f"- **Avg Videos per Channel:** {avg_videos:,}\n\n"

        # Language breakdown
        by_lang = {}
        for c in self.channels:
            lang = c.get('language', 'Unknown')
            by_lang[lang] = by_lang.get(lang, 0) + 1

        md += "## By Language\n\n"
        md += "| Language | Channels | Percentage |\n"
        md += "|----------|----------|------------|\n"

        for lang, count in sorted(by_lang.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(self.channels)) * 100
            md += f"| {lang} | {count} | {pct:.1f}% |\n"

        # Category breakdown
        by_cat = {}
        for c in self.channels:
            cat = c.get('category', 'Uncategorized')
            by_cat[cat] = by_cat.get(cat, 0) + 1

        md += "\n## By Category\n\n"
        md += "| Category | Channels | Percentage |\n"
        md += "|----------|----------|------------|\n"

        for cat, count in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(self.channels)) * 100
            md += f"| {cat} | {count} | {pct:.1f}% |\n"

        return md

    def generate_all(self, output_dir: Path):
        """Generate all markdown files"""
        output_dir.mkdir(exist_ok=True)

        print("📝 Generating markdown files...\n")

        # Generate by category
        print("   ✍️  Generating by category...")
        by_category = self.generate_by_category()
        (output_dir / 'CHANNELS_BY_CATEGORY.md').write_text(by_category, encoding='utf-8')
        print("   ✅ Saved CHANNELS_BY_CATEGORY.md")

        # Generate by language
        print("   ✍️  Generating by language...")
        by_language = self.generate_by_language()
        (output_dir / 'CHANNELS_BY_LANGUAGE.md').write_text(by_language, encoding='utf-8')
        print("   ✅ Saved CHANNELS_BY_LANGUAGE.md")

        # Generate top channels
        print("   ✍️  Generating top channels...")
        top_channels = self.generate_top_channels(100)
        (output_dir / 'TOP_100_CHANNELS.md').write_text(top_channels, encoding='utf-8')
        print("   ✅ Saved TOP_100_CHANNELS.md")

        # Generate stats
        print("   ✍️  Generating statistics...")
        stats = self.generate_stats()
        (output_dir / 'STATISTICS.md').write_text(stats, encoding='utf-8')
        print("   ✅ Saved STATISTICS.md")

        print(f"\n✅ All markdown files generated in {output_dir}")


def main():
    enriched_data = Path(__file__).parent / 'enriched_channels.json'

    if not enriched_data.exists():
        print(f"❌ Enriched data file not found: {enriched_data}")
        print("   Run fetch_youtube_data.py first!")
        return

    output_dir = Path(__file__).parent / 'docs'

    generator = MarkdownGenerator(str(enriched_data))
    generator.generate_all(output_dir)


if __name__ == '__main__':
    main()
