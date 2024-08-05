import feedparser
import json

# List of RSS feed URLs
rss_urls = ["https://example.com/rss", "https://another-example.com/rss"]


# Function to fetch and parse RSS feeds
def fetch_rss():
    rss_data = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            rss_data.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "summary": entry.summary,
                }
            )
    return rss_data


# Fetch RSS feeds
rss_data = fetch_rss()

# Save to JSON file
with open("rss_data.json", "w") as json_file:
    json.dump(rss_data, json_file, indent=4)
