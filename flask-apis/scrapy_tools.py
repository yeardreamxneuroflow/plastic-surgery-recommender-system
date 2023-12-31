"""Using Scrapy to scrape and store wannabe face images.
"""


import requests
from PIL import Image

import boto3
from botocore.client import BaseClient

from macro import ScrapyMacro, AWSMacro


def run_scraper(wananbe_to_scrape: list[str]) -> dict[str, Image.Image]:
    """Execute Scrapy remotly and get scraped wannabe images.
    """

    payload = {"wannabe_list": wananbe_to_scrape}
    scrapy_macro = ScrapyMacro()

    r = requests.get(
        f"http://{scrapy_macro.SCRAPER_NODE_IP}:{scrapy_macro.SCRAPER_NODE_PORT}/run",
        params=payload,
    )
    pass  # Breakpoint

    # TODO: Parse return value

    # TODO: Return scraped images w/ attached wannabe information


def upload_wannabe_images_manually(s3: BaseClient, wannabe_list: list[str]) -> None:
    """Upload local-stored images to S3 Bucket.

    `aws_macro` is already generated by `if __name__: ...` logic.
    """

    for wannabe in wannabe_list:
        local_file_path = f"manual_images/{wannabe}/original.jpg"
        object_key = f"{wannabe}/original.jpg"
        s3.upload_file(
            Filename=local_file_path,
            Bucket=aws_macro.AWS_MANUAL_WANNABE_BUCKET_NAME,
            Key=object_key,
        )


if __name__ == "__main__":
    """Upload wannabe images manually.
    """

    aws_macro = AWSMacro()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_macro.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_macro.AWS_SECRET_ACCESS_KEY,
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

    upload_wannabe_images_manually(s3=s3, wannabe_list=wannabe_list)
