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
import uuid


def read_config(config_path):
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)


def fetch_rss_feed(url, retries, backoff_factor, modified_since, etag):
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
    if modified_since:
        headers["If-Modified-Since"] = modified_since
    if etag:
        headers["If-None-Match"] = etag

    response = session.get(url, headers=headers)
    response.raise_for_status()

    relevant_headers = {
        "date": response.headers.get("date"),
        "content-type": response.headers.get("content-type"),
        "etag": response.headers.get("etag"),
    }

    return feedparser.parse(response.content), response, relevant_headers


def fetch_rss(config):
    feeds = []
    articles = []
    retries = config.get("retries", 3)
    backoff_factor = config.get("backoff_factor", 0.3)

    for feed_config in config["feeds"]:
        url = feed_config["url"]
        modified_since = feed_config.get("if_modified_since")
        etag = feed_config.get("etag")
        feed_id = feed_config.get("id") or str(uuid.uuid4())

        try:
            feed, response, headers = fetch_rss_feed(
                url, retries, backoff_factor, modified_since, etag
            )
            feed_info = {
                "feed_id": feed_id,
                "feed_title": feed.feed.title,
                "feed_link": feed.feed.link,
                "feed_description": feed.feed.description,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "headers": headers,
            }
            feeds.append(feed_info)
            for entry in feed.entries:
                articles.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.published,
                        "summary": entry.summary,
                        "feed_id": feed_id,
                    }
                )
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)

    return {"feeds": feeds, "articles": articles}


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

    signature_key = os.getenv("NF_SIGNATURE_KEY")
    if signature_key:
        signature = sign_data(output_json, signature_key)
        output = {"data": output, "signature": signature}

    with open(args.output_json, "w") as json_file:
        json.dump(output, json_file, indent=4)


if __name__ == "__main__":
    main()
