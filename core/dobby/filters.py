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
    unwanted_characters = ',.٬٫ '

    table = str.maketrans(persian_digits, english_digits, unwanted_characters)
    price = price.translate(table)
    digits = re.search(r'\d+', price)
    if digits:
        return int(digits.group(0))

def currency_filter(currency: str):
    """
    Clean up a currency string by removing any non-word characters and keeping the first word.

    Parameters:
    - currency (str): The currency string to be cleaned up.

    Returns:
    - str: The cleaned up currency string.
    """
    if not currency:
        return ''

    list_of_known_currencies = [
        '﷼',
        'میلیون ریال',
        'ملیون ریال',
        'میلیون‌ریال',
        'ملیون‌ریال',
        'ریال',
        'هزارتومان',
        'هزار تومان',
        'تومان',
        'rial',
        'toman',
        'IRT',
        'IRR',
    ]

    for c in list_of_known_currencies:
        if c.lower() in currency.lower():
            return c

    # remove all non-word characters
    return re.sub(r'[\W\d]+', '', currency).strip()

def currency_translate(currency: str):
    """
    Translate the given currency to its equivalent in Persian currency. 

    Args:
        currency (str): The currency to be translated.

    Returns:
        str: The translated currency, or the original currency if no translation is found.
    """
    translate_table = {
        '﷼': 'ریال',
        'هزار تومان': 'هزارتومان',
        'میلیون ریال': 'میلیون‌ریال',
        'ملیون ریال': 'میلیون‌ریال',
        'rial': 'ریال',
        'toman': 'تومان',
        'irt': 'تومان',
        'irr': 'ریال',
    }

    return translate_table.get(currency.lower(), currency)