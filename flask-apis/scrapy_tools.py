from typing import List, Any

import requests
from PIL.Image import Image
import boto3

from scrapy_macro import SCRAPER_NODE_IP, SCRAPER_NODE_PORT
from aws_macro import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from aws_macro import AWS_MANUAL_WANNABE_BUCKET_NAME


def run_scraper(wananbe_to_scrape: list[str]) -> dict[str, Image]:
    payload = {"wannabe_list": wananbe_to_scrape}

    r = requests.get(
        f"http://{SCRAPER_NODE_IP}:{SCRAPER_NODE_PORT}/run",
        params=payload,
    )

    # TODO: Parse return value

    # TODO: Return scraped images w/ attached wannabe information


def upload_wannabe_images_manually(s3: Any, wannabe_list: List[str]) -> None:
    """Upload local-stored images to S3 Bucket
    """

    for wannabe in wannabe_list:
        local_file_path = f"manual_images/{wannabe}/original.jpg"
        object_key = f"{wannabe}/original.jpg"
        s3.upload_file(
            Filename=local_file_path,
            Bucket=AWS_MANUAL_WANNABE_BUCKET_NAME,
            Key=object_key,
        )


if __name__ == "__main__":
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    wannabe_list = [
        "박보검",
        "뷔",
        "서강준",
        "송강",
        "송중기",
        "신세경",
        "아이린",
        "아이유",
        "오연서",
        "윈터",
        "육성재",
        "윤아",
        "이주빈",
        "장원영",
        "정국",
        "정우성",
        "제니",
        "차은우",
        "카리나",
    ]

    upload_wannabe_images_manually(s3, wannabe_list)
