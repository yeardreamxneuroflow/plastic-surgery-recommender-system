# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline


class WannabeImageScraperPipeline(ImagesPipeline):
    none_wannabe_counter = 0
    img_counter = {
        "countered_wannabies": [],
    }

    def file_path(self, request, response=None, info=None, *, item=None) -> str:
        # Pass pseudo method calling(this method)
        # See below 'Request Twice Issue'
        if response == None:
            return f""

        if item is None or item["wannabe_is"] is None:
            self.none_wannabe_counter += 1
            return f"None/{self.none_wannabe_counter}/original.jpg"
        else:
            wannabe = item["wannabe_is"]

            if wannabe not in self.img_counter["countered_wannabies"]:
                # First-time Countered
                self.img_counter["countered_wannabies"].append(wannabe)
                self.img_counter[wannabe] = 0
                c = 0
            elif wannabe in self.img_counter["countered_wannabies"]:
                self.img_counter[wannabe] += 1
                c = self.img_counter[wannabe]

            # TODO: Reqeust Twice Issue
            # print("--------------------------------------------------")
            # print(f"wannabe={wannabe}, c={c}")
            # print("--------------------------------------------------")
            # return f"{wannabe}/{c}/original.jpg"  # Correct Code
            return f"{wannabe}/{c // 2}/original.jpg"
