import typing

import scrapy


def read_wannabe_list(gender: str) -> list:
    """Read List of Wannabies from 'txt' File and Return the Python List

    Args:
        gender: Which gender list to read

    Returns:
        Read list as type of Python's `list`
    """

    if gender == "men":
        file_to_read = "./wannabe_men.txt"
    elif gender == "women":
        file_to_read = "./wannabe_women.txt"

    with open(file_to_read, "r", encoding="UTF-8") as file:
        # open() reads newline too
        return [line.rstrip("\n") for line in file.readlines()]


class WannabeMenSpider(scrapy.Spider):
    name = "wannabe_men"
    custom_settings = {
        "ITEM_PIPELINES": {
            "wannabe_image_scraper.pipelines.WannabeImageScraperPipeline": 300,
        },
        "IMAGES_STORE": "s3://dev-team12-wannabe-men-image/",
    }

    def start_requests(self) -> typing.Iterable[scrapy.Request]:
        wannabe_list = read_wannabe_list("men")

        for wannabe in wannabe_list:
            yield scrapy.Request(
                url=f"https://search.naver.com/search.naver?query={wannabe}+증명사진",
                meta={"wannabe_is": wannabe},
                callback=self.parse,
            )

    def parse(self, response):
        img_src_urls = []
        top_thumbnail_imgs = response.css("img.thumb")[:5]  # Top 5 Temporary

        for top_thumbnail_img in top_thumbnail_imgs:
            img_src_urls.append(top_thumbnail_img.attrib["src"])

        yield {
            "image_urls": img_src_urls,
            "wannabe_is": response.meta["wannabe_is"]
        }
