from itemadapter import ItemAdapter
import json

class SpiderGeoogePipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item