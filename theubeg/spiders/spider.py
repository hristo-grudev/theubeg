import scrapy

from scrapy.loader import ItemLoader

from ..items import TheubegItem
from itemloaders.processors import TakeFirst


class TheubegSpider(scrapy.Spider):
	name = 'theubeg'
	start_urls = ['https://www.theubeg.com/press-room/news']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "read-more")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="prev"][2]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-md-9"]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date-time"]/text()').get()

		item = ItemLoader(item=TheubegItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
