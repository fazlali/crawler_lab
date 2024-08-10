import scrapy

from scrapy.linkextractors import LinkExtractor

from scrapy.crawler import CrawlerProcess
from scrapy.utils.gz import gzip_magic_number, gunzip

from .dobby.items import ProductLoader
import multiprocessing
import re
from scrapy.http import XmlResponse
from parsel import Selector


class BaseExtractor(scrapy.Spider):
    loader_class = ProductLoader
    LIMIT = 200

    def __init__(self, start_urls: list, result: list, extraction_configs: dict = None, limit=LIMIT, **kwargs):
        super().__init__()
        self.timeout = int(kwargs.pop("timeout", "60"))
        self.start_urls = start_urls
        extraction_configs = extraction_configs or {}
        self.item_counter = iter(range(limit))
        self.extraction_configs = extraction_configs

        self.product_allow = list(map(re.compile, extraction_configs.get('product_allow', [])))
        self.product_deny = list(map(re.compile, extraction_configs.get('product_deny', [])))

        self.sub_rules = [(re.compile(rule['pattern']), rule['replacement'])
                          for rule in extraction_configs.get('sub_rules', [])]

        self.item_counter = iter(range(limit))
        self.limit = limit
        self.result = result

    def start_requests(self):
        from twisted.internet import reactor
        reactor.callLater(self.timeout, self.stop)

        for url in self.start_urls:
            yield from self.follow_extraction(url)

    def errback(self, failure):
        print(failure)

    def follow_extraction(self, url=None):
        yield scrapy.Request(
            url,
            callback=self.parse,
            errback=self.errback
        )

    def check_product_url(self, url=None):
        if self.product_allow:
            if not any(product_allow.match(url) for product_allow in self.product_allow):
                return

        if self.product_deny:
            if any(product_deny.match(url) for product_deny in self.product_deny):
                return
        try:
            next(self.item_counter)

            scrape_url = url
            for pattern, repl in self.sub_rules:
                scrape_url = pattern.sub(repl, scrape_url)

            self.result.append(scrape_url)

        except StopIteration:
            pass

    def stop(self):
        self.crawler.engine.close_spider(self, "timeout")


class SitemapExtractor(BaseExtractor):
    name = 'sitemap-extractor'

    def parse(self, response, **_kwargs):
        body = self._get_sitemap_body(response)
        selector = Selector(body=body, type='xml')
        selector.remove_namespaces()

        if selector.root.tag not in ['urlset', 'sitemapindex']:
            raise ValueError('Invalid root tag: %s', selector.root.tag)

        for page in selector.xpath('./*'):
            loc = page.xpath('./loc/text()').get()

            if selector.root.tag == 'sitemapindex':
                yield from self.follow_extraction(loc)
            else:
                self.check_product_url(loc)

    def _get_sitemap_body(self, response):
        if isinstance(response, XmlResponse):
            return response.body
        if gzip_magic_number(response):
            return gunzip(response.body)

        if response.url.endswith(".xml") or response.url.endswith(".xml.gz"):
            return response.body

        return b''


class CrawlExtractor(BaseExtractor):
    name = 'crawl-extractor'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        crawl_allow = self.extraction_configs.get('crawl_allow', ())
        crawl_deny = self.extraction_configs.get('crawl_deny', ())
        product_allow = self.extraction_configs.get('product_allow', ())
        product_deny = self.extraction_configs.get('product_deny', ())

        self.crawl_link_extractor = LinkExtractor(
            allow=crawl_allow,
            deny=crawl_deny,
        )
        self.product_link_extractor = LinkExtractor(
            allow=product_allow,
            deny=product_deny,
        )

    def parse(self, response, **_kwargs):
        product_links = self.product_link_extractor.extract_links(response)
        for link in product_links:
            self.check_product_url(link.url)

        links = self.crawl_link_extractor.extract_links(response)
        for link in links[:self.limit - len(self.result)]:
            yield from self.follow_extraction(link.url)


def _extract(start_urls: list, config: dict, *args, **kwargs):
    crawler_process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'LOG_LEVEL': 'ERROR'
    })
    spider = config.get('spider', 'sitemap-extractor')

    if spider == 'sitemap-extractor':
        extractor = SitemapExtractor

    elif spider == 'crawl-extractor':
        extractor = CrawlExtractor

    else:
        raise Exception('Invalid spider: ', spider)

    result = []
    crawler_process.crawl(extractor, start_urls, result, config, *args, **kwargs)
    crawler_process.start()
    return result


def do_work(a, queue):
    for item in _extract(*a):
        queue.put(item)


def extract(*args):
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
