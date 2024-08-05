import os
import sys
import feedparser
import json
import toml
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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
    config_path = os.getenv("CONFIG_PATH", "config.toml")
    output_json = os.getenv("OUTPUT_JSON", "rss_data.json")

    config = read_config(config_path)
    rss_data = fetch_rss(config["fetch_rss"])

    with open(output_json, "w") as json_file:
        json.dump(rss_data, json_file, indent=4)


if __name__ == "__main__":
    main()
