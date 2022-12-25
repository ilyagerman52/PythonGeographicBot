from itemadapter import ItemAdapter
import json
import sqlite3

class SpiderGeoogePipeline:
    def open_spider(self, spider):
        print("еcли парсим 17ый номер введи 1, если 18ый что угодно другое")
        self.stat = input()
        self.conn = sqlite3.connect(r"../geonames.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ege_17(
            question TEXT,
            answer TEXT);
        """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ege_18(
           question TEXT,
           answer TEXT);
        """)
        self.conn.commit()
        # self.file = open('items.json', 'w')

    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        it = ItemAdapter(item).asdict()
        if self.stat == "1":
            self.cur.execute("INSERT INTO ege_17 VALUES(?, ?);", [it["question"], it["answer"]])
        else:
            self.cur.execute("INSERT INTO ege_18 VALUES(?, ?);", [it["question"], it["answer"]])
        self.conn.commit()
        # line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + ",\n"
        # self.file.write(line)
        return item