import os
import sys
import yaml
import feedparser
import json
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import argparse
import time
import hmac
import hashlib


def read_config(config_path):
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)


def fetch_rss_feed(url, retries, backoff_factor, since):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    headers = {}
    if since:
        headers["If-Modified-Since"] = since

    response = session.get(url, headers=headers)
    response.raise_for_status()
    return feedparser.parse(response.content), response


def fetch_rss(config):
    rss_data = []
    retries = config.get("retries", 3)
    backoff_factor = config.get("backoff_factor", 0.3)
    since = config.get("since")

    for url in config["rss_urls"]:
        try:
            feed, response = fetch_rss_feed(url, retries, backoff_factor, since)
            feed_info = {
                "feed_title": feed.feed.title,
                "feed_link": feed.feed.link,
                "feed_description": feed.feed.description,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "headers": dict(response.headers),
            }
            for entry in feed.entries:
                published_time = time.mktime(entry.published_parsed)
                if not since or published_time > time.mktime(
                    time.strptime(since, "%a, %d %b %Y %H:%M:%S %Z")
                ):
                    rss_data.append(
                        {
                            "title": entry.title,
                            "link": entry.link,
                            "published": entry.published,
                            "summary": entry.summary,
                            "feed_info": feed_info,
                        }
                    )
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)

    return rss_data


def sign_data(data, secret_key):
    signature = hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
    return signature


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Fetch RSS feeds and update JSON.")
    parser.add_argument(
        "--config",
        type=str,
        default=os.getenv("CONFIG_PATH", "config.yaml"),
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

    output = {"data": rss_data, "timestamp": time.strftime("%a, %d %b %Y %H:%M:%S %Z")}

    output_json = json.dumps(output, indent=4)

    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        signature = sign_data(output_json, secret_key)
        output = {"data": output, "signature": signature}

    with open(args.output_json, "w") as json_file:
        json.dump(output, json_file, indent=4)


if __name__ == "__main__":
    main()
