#!/usr/bin/env python3
"""GMK Center news parser — fetches today's news from RSS and sends to n8n webhook."""

import sys
from datetime import datetime, timezone

import feedparser
import requests

from config import RSS_FEED_URL, N8N_WEBHOOK_URL


def fetch_today_news():
    """Parse RSS feed and return today's news items."""
    feed = feedparser.parse(RSS_FEED_URL)

    if feed.bozo and not feed.entries:
        print(f"Error parsing feed: {feed.bozo_exception}", file=sys.stderr)
        sys.exit(1)

    today = datetime.now(timezone.utc).date()
    news = []

    for entry in feed.entries:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

        if published.date() != today:
            continue

        news.append({
            "title": entry.title,
            "link": entry.link,
            "published": published.isoformat(),
            "description": entry.get("summary", ""),
            "categories": [tag.term for tag in entry.get("tags", [])],
            "author": entry.get("author", ""),
        })

    return news


def send_to_n8n(news):
    """Send news list to n8n webhook."""
    if not news:
        print("No news for today.")
        return

    payload = {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "count": len(news),
        "news": news,
    }

    resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
    resp.raise_for_status()
    print(f"Sent {len(news)} news items to n8n. Status: {resp.status_code}")


def main():
    news = fetch_today_news()
    print(f"Found {len(news)} news items for today.")
    send_to_n8n(news)


if __name__ == "__main__":
    main()
