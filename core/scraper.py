import multiprocessing
from email.utils import parsedate_to_datetime

import charset_normalizer
import scrapy

from scrapy.crawler import CrawlerProcess

from .dobby.items import ProductLoader

from .dobby.selector import Selectors
from scrapy.http import Request


class ProductScraper(scrapy.Spider):
    name = 'Product Scraper'
    loader_class = ProductLoader

    def __init__(self, scrape_urls: list[str], selectors: dict, result: list[dict], **kwargs):
        super().__init__(**kwargs)
        self.timeout = int(kwargs.pop("timeout", "180"))
        self.scrape_urls = scrape_urls
        self.selectors = Selectors(selectors)
        self.result = result

    def start_requests(self):
        from twisted.internet import reactor
        reactor.callLater(self.timeout, self.stop)

        for scrape_url in self.scrape_urls:
            yield Request(scrape_url)

    def _parse_header_to_date(self, response, header_name):
        try:
            return parsedate_to_datetime(
                response.headers[header_name].decode()
            )
        except (KeyError, ValueError):
            self.logger.debug('Ignoring invalid %s header on page %s', header_name, response.url)

    def create_item_loader(self, **kwargs):
        item_loader = self.loader_class(**kwargs)
        return item_loader

    def parse(self, response):
        encoding = charset_normalizer.detect(response.body)['encoding']
        if encoding != 'utf-8':
            response = response.replace(body=response.body.decode(encoding, 'replace').encode('utf-8'))

        item_loader = self.create_item_loader(selector=response.selector)
        item_loader.add_value('scrape_url', response.url)
        item_loader.add_value('status_code', response.status)

        self.selectors.populate_item_loader(item_loader)

        item = item_loader.load_item()
        if 'image_urls' in item:
            for i in range(len(item['image_urls'])):
                item['image_urls'][i] = response.urljoin(item['image_urls'][i])
        self.result.append(item)
        yield item

    def stop(self):
        self.crawler.engine.close_spider(self, "timeout")


def _scrape(urls: list, selectors: dict, *args, **kwargs):
    crawler_process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_TIMEOUT': 30
    })
    result = []
    crawler_process.crawl(ProductScraper, urls, selectors, result, *args, **kwargs)
    crawler_process.start()
    return result


def do_work(a, queue):
    for item in _scrape(*a):
        queue.put(item)


def scrape(*args):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=do_work, args=(args, result_queue))
    process.start()

    result = []
    while True:
        try:
            result.append(result_queue.get(True, 1))
        except multiprocessing.queues.Empty:
            if not process.is_alive():
                break

    return result
