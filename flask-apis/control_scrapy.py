import requests
from PIL import Image

from scrapy_macro import SCRAPER_NODE_IP, PORT

def run_scraper(wananbe_to_scrape: list[str]) -> dict[str, Image]:
    payload = {"wannabe_list": wananbe_to_scrape}

    r = requests.get(
        f"http://{SCRAPER_NODE_IP}:{PORT}/run",
        params=payload,
    )

    # TODO: Parse return value

    # TODO: Return scraped images w/ attached wannabe information
