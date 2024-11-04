import re
import logging

logger = logging.getLogger(__name__)

def strip_text(item_input):
    '''
    Only apply strip if input type is str
    '''
    if isinstance(item_input, str):
        return re.sub(r'\s+', ' ', item_input.strip())
    return item_input

def sitemap_filter(sitemap_urls: list) -> list:
    if not sitemap_urls:
        return []

    if len(sitemap_urls) < 2:
        return sitemap_urls

    if any('product-sitemap' in s for s in sitemap_urls):
        return [s for s in sitemap_urls if 'product-sitemap' in s]

    if any('wp-sitemap-posts-product' in s for s in sitemap_urls):
        return [s for s in sitemap_urls if 'wp-sitemap-posts-product' in s]

    return sitemap_urls

def price_filter(price: str):
    """
    Clean up a price string by removing any non-numeric characters and converting any Persian digits to English digits.

    Parameters:
    - price (str): The price string to be cleaned up.

    Returns:
    - str: The cleaned up price string.
    """
    if not price:
        return None

    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    # comma, period, thousands separator, decimal separator, space
    unwanted_characters = ',٬٫ /.،'

    table = str.maketrans(persian_digits, english_digits, unwanted_characters)
    price = price.translate(table)
    digits = re.search(r'\d+', price)
    if digits:
        return int(digits.group(0))