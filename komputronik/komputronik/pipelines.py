import csv
from itemadapter import ItemAdapter


class KomputronikPipeline:
    def open_spider(self, spider):
        self.file = open("computers.csv", "w", newline="")
        self.fieldnames = [
            "category_url",
            "link",
            "computer_name",
            "graphic_card",
            "price",
        ]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print(ItemAdapter(item).asdict())
        self.writer.writerow(ItemAdapter(item).asdict())
        return item
