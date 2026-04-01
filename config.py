"""Configuration for GMK Center news parser."""

import os

# GMK Center RSS feed URL
RSS_FEED_URL = "https://gmk.center/ua/feed/"

# n8n webhook URL — set via N8N_WEBHOOK_URL environment variable or .env file
N8N_WEBHOOK_URL = os.environ.get(
    "N8N_WEBHOOK_URL",
    "https://n8n.mafiavlc.org/webhook/2850361e-3299-4b0a-a847-86727de3fc58",
)
