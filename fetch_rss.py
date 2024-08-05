import os
import sys
import feedparser
import json
import toml
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import argparse


def read_config(config_path):
    with open(config_path, "r") as config_file:
        return toml.load(config_file)


def fetch_rss_feed(url, retries, backoff_factor):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url)
    response.raise_for_status()
    return feedparser.parse(response.content)


def fetch_rss(config):
    rss_data = []
    retries = config.get("retries", 3)
    backoff_factor = config.get("backoff_factor", 0.3)

    for url in config["rss_urls"]:
        try:
            feed = fetch_rss_feed(url, retries, backoff_factor)
            for entry in feed.entries:
                rss_data.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.published,
                        "summary": entry.summary,
                    }
                )
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)

    return rss_data


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Fetch RSS feeds and update JSON.")
    parser.add_argument(
        "--config",
        type=str,
        default=os.getenv("CONFIG_PATH", "config.toml"),
        help="Path to config file",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default=os.getenv("OUTPUT_JSON", "rss_data.json"),
        help="Path to output JSON file",
    )
    args = parser.parse_args()

    config = read_config(args.config)
    rss_data = fetch_rss(config["fetch_rss"])

    with open(args.output_json, "w") as json_file:
        json.dump(rss_data, json_file, indent=4)


if __name__ == "__main__":
    main()
