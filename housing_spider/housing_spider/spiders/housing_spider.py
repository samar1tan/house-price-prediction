from ..items import HousingSpiderItem
from scrapy import Request
from scrapy.spiders import Spider


class HouseSpider(Spider):
    name = 'houses_info'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://sy.lianjia.com/ershoufang'
        yield Request(url, headers=self.headers, callback=self.parse)
        NUM_PAGES = 100  # total amount of pages to crawl
        for i in range(NUM_PAGES - 1):
            next_url = "https://sy.lianjia.com/ershoufang/pg%d" % (i + 2)
            yield Request(next_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        """ crawl all the houses """
        houses = response.xpath('//ul[@class="sellListContent"]/li/div[1]/div[1]/a/@href').extract()
        for house in houses:
            yield Request(house, callback=self.parse_util, headers=self.headers)

    @staticmethod
    def parse_util(response):
        """ crawl every house """
        item = HousingSpiderItem()

        # retrieve
        # overview
        url_o = response.xpath('//div[@class="overview"]/div[@class="content"]/div[@class="price "]')
        price = url_o.xpath('./span[1]/text()').extract()[0]
        unit_price = url_o.xpath('./div[1]/div[1]/span/text()').extract()[0]
        # base
        url_b = response.xpath('//div[@class="base"]/div[@class="content"]/ul')
        bedroom = url_b.xpath('./li[1]/text()').re('(.*)室.*')[0]
        hall = url_b.xpath('./li[1]/text()').re('.*室(.*)厅.*')[0]
        chicken = url_b.xpath('./li[1]/text()').re('.*厅(.*)厨.*')[0]
        washroom = url_b.xpath('./li[1]/text()').re('.*厨(.*)卫')[0]
        floor = url_b.xpath('./li[2]/text()').re('(.*)楼层.*')
        building_size = url_b.xpath('./li[3]/text()').re('(.*)㎡')
        house_structure = url_b.xpath('./li[4]/text()').extract()[0]
        building_type = url_b.xpath('./li[6]/text()').extract()[0]
        building_structure = url_b.xpath('./li[8]/text()').extract()[0]
        fitment = url_b.xpath('./li[9]/text()').extract()[0]
        pro_limit = url_b.xpath('./li[13]/text()').re('(.*)年')
        heating = url_b.xpath('./li[11]/text()').extract()[0]
        # transaction
        url_t = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul')
        pro_owner = url_t.xpath('./li[6]/span[2]/text()').extract()[0]
        pledge = url_t.xpath('./li[7]/span[2]/@title').re('(.)抵押.*')
        replacement = url_t.xpath('./li[8]/span[2]/text()').extract()[0]
        transaction_owner = url_t.xpath('./li[2]/span[2]/text()').extract()[0]
        house_use = url_t.xpath('./li[4]/span[2]/text()').extract()[0]

        # load
        item['price'] = price
        item['unit_price'] = unit_price
        item['bedroom'] = bedroom
        item['hall'] = hall
        item['chicken'] = chicken
        item['washroom'] = washroom
        if floor:
            item['floor'] = floor[0]
        else:
            item['floor'] = '暂无数据'
        if building_size:
            item['building_size'] = building_size[0]
        else:
            item['building_size'] = '暂无数据'
        item['house_structure'] = house_structure
        item['building_type'] = building_type
        item['building_structure'] = building_structure
        item['fitment'] = fitment
        if pro_limit:
            item['pro_limit'] = pro_limit[0]
        else:
            item['pro_limit'] = '暂无数据'
        item['pro_owner'] = pro_owner
        if pledge:
            item['pledge'] = pledge[0]
        else:
            item['pledge'] = '暂无数据'
        item['replacement'] = replacement
        item['heating'] = heating
        item['transaction_owner'] = transaction_owner
        item['house_use'] = house_use

        yield item
