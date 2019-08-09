# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os import path


class HousingSpiderPipeline(object):
    def open_spider(self, spider):
        # store csv file in project root
        csv_path = path.join(path.pardir, 'houses_info.csv')
        self.f = open(csv_path, 'w', encoding='utf-8')
        self.f.write(
            "price,unit_price,bedroom,hall,chicken,washroom,floor,building_size,house_structure,building_type,building_structure,fitment,pro_limit,pro_owner,pledge,replacement,heating,transaction_owner,house_use" + '\n')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        # convert pre-defined categories into digits
        Floor = {"低": "0", "中": "1", "高": "2"}
        House_str = {"平层": "0", "错层": "1", "复式": "2", "跃层": "3", "暂无数据": "0"}
        Building_t = {"板楼": "0", "塔楼": "1", "板塔结合": "2", "平房": "3", "暂无数据": "0"}
        Building_str = {"钢混结构": "0", "混合结构": "1", "框架结构": "2", "未知结构": "3", "砖混结构": "4", "砖木结构": "5"}
        Fitment = {"简装": "0", "精装": "1", "毛坯": "2", "其他": "3"}
        Pro_owner = {"共有": "0", "非共有": "1", "暂无数据": "1"}
        Pledge = {"无": "0", "有": "1", "暂无数据": "0"}
        Replacement = {"已上传房本照片": "0", "未上传房本照片": "1"}
        Heating = {"集中供暖": "0", "自供暖": "1", "暂无数据": "0"}
        Transaction_o = {"商品房": "0", "经济适用房": "1", "已购公房": "2"}
        House_use = {"普通住宅": "0", "商住两用": "1"}
        try:
            price = str(float(str(item["price"])) * 10000.0)  # 万元
            unit_price = str(item["unit_price"])
            bedroom = str(item["bedroom"])
            hall = str(item["hall"])
            chicken = str(item['chicken'])
            washroom = str(item['washroom'])
            floor = Floor[str(item['floor'])]
            building_size = str(item['building_size'])
            house_structure = House_str[str(item['house_structure'])]
            building_type = Building_t[str(item['building_type'])]
            building_structure = Building_str[str(item['building_structure'])]
            fitment = Fitment[str(item['fitment'])]
            pro_limit = str(item['pro_limit'])
            if pro_limit == str("暂无数据"):
                pro_limit = str("70")
            pro_owner = Pro_owner[str(item['pro_owner'])]
            pledge = Pledge[str(item['pledge'])]
            replacement = Replacement[str(item['replacement'])]
            heating = Heating[str(item['heating'])]
            transaction_owner = Transaction_o[str(item['transaction_owner'])]
            house_use = House_use[str(item['house_use'])]

            line = price + ',' + unit_price + ',' + bedroom + ',' + hall + ',' + chicken + ',' + \
                   washroom + ',' + floor + ',' + building_size + ',' + house_structure + ',' + building_type + ',' + building_structure + ',' + fitment + ',' + pro_limit + ',' + pro_owner + ',' + pledge + ',' + replacement + ',' + heating + ',' + transaction_owner + ',' + house_use + '\n'
            self.f.write(line)
        except IOError as ioe:
            print(ioe)
        return item
