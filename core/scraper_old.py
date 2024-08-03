import requests
import parsel
from .dobby.selector import Selectors
from .dobby.items import ProductLoader


def scrape_product_data(content: str, selectors: dict):
    selectors = Selectors(selectors)
    item_loader = ProductLoader(selector=parsel.Selector(content))
    selectors.populate_item_loader(item_loader)
    item = item_loader.load_item()
    return item


def scrape(url: str, selectors_configuration: dict):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
    if not response.ok:
        print(response.status_code)
        return
    response.encoding = response.apparent_encoding
    return scrape_product_data(response.text, selectors_configuration)
