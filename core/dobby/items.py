# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from functools import partial
from itertools import islice

from itemloaders import ItemLoader

from itemloaders.processors import Compose, MapCompose, TakeFirst, Join, Identity

from w3lib.html import remove_tags, remove_tags_with_content

from .filters import price_filter, sitemap_filter, strip_text


class BaseLoader(ItemLoader):
    default_input_processor = MapCompose(strip_text)
    default_output_processor = Compose(reversed, TakeFirst())


class WebsiteLoader(BaseLoader):
    sitemap_urls_out = sitemap_filter

class ProductLoader(BaseLoader):
    title_in = MapCompose(remove_tags, strip_text)

    price_in = MapCompose(remove_tags, strip_text, price_filter)
    price_out = Compose(TakeFirst())
    selling_price_in = MapCompose(remove_tags, strip_text, price_filter)
    selling_price_out = Compose(TakeFirst())

    currency_in = MapCompose(remove_tags, strip_text)
    brand_in = MapCompose(remove_tags, strip_text)
    out_of_stock_in = MapCompose(remove_tags, strip_text)
    out_of_stock_out = Compose(TakeFirst())

    @staticmethod
    def image_urls_out(i):
        return list(islice(i, 10))

    description_in = MapCompose(partial(remove_tags_with_content, which_ones=['script', 'style']), remove_tags, strip_text)
    description_out = Compose(Join('\n\n'), strip_text)

    expires_out = Compose(max)
