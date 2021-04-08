import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import Bb1bankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class Bb1bankSpider(scrapy.Spider):
	name = 'b1bank'
	start_urls = ['https://www.b1bank.com/about-b1bank/news-events']

	def parse(self, response):
		post_links = response.xpath('//div[@class="article-button"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="date-display-single"]/text()').get()
		title = response.xpath('(//h1)[last()]/text()').get().strip()
		content = response.xpath('(//div[@class="content"])[last()]//text()[not (ancestor::span[@class="date-display-single"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=Bb1bankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
