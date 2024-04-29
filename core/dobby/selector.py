import logging

from collections import defaultdict

from itemloaders import ItemLoader
from itemloaders.processors import Compose, MapCompose

from lxml.cssselect import SelectorError

logger = logging.getLogger(__name__)


class SelectorLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = Compose(set, list)  # remove duplicates


class Selectors:
    def __init__(self, selectors={}):
        self.selectors = defaultdict(SelectorLoader)
        self.load_selectors_from_dict(selectors)

    def load_selectors_from_dict(self, selectors):
        for expression_lang, selector_dict in selectors.items():
            for key, selector_list in selector_dict.items():
                self.selectors[expression_lang].add_value(key, selector_list)

    @property
    def as_dict(self):
        return {
            expression_lang: self.selectors[expression_lang].load_item()
            for expression_lang in self.selectors.keys()
        }

    def populate_item_loader(self, item_loader: ItemLoader):
        for expression_lang, selector_item in self.selectors.items():
            f = getattr(item_loader, f'add_{expression_lang}')
            for key, selector_list in selector_item.load_item().items():
                for selector in selector_list:
                    try:
                        f(key, selector)
                    except SelectorError as ex:
                        url = None
                        # TODO: refactor this
                        if item_loader.selector and item_loader.selector.response:
                            url = item_loader.selector.response.url
                        
                        logger.warning('Selector %s failed on page %s | Message: %s', selector, url, ex)
