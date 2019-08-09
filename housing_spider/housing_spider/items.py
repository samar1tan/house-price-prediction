# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HousingSpiderItem(Item):
    price = Field()  # 价格
    unit_price = Field()  # 单价
    bedroom = Field()  # 卧室
    hall = Field()  # 厅
    chicken = Field()  # 厨房
    washroom = Field()  # 卫生间
    floor = Field()  # 所在楼层
    building_size = Field()  # 建筑面积
    house_structure = Field()  # 户型结构
    building_type = Field()  # 建筑类型
    building_structure = Field()  # 建筑结构
    fitment = Field()  # 装修情况
    pro_limit = Field()  # 产权年限
    pro_owner = Field()  # 产权所属
    pledge = Field()  # 抵押信息
    replacement = Field()  # 房本备件
    heating = Field()  # 供暖方式
    transaction_owner = Field()  # 交易权属
    house_use = Field()  # 房屋用途

