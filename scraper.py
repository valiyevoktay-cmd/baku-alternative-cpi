import re
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CPIScraper")

class PriceScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
            "Accept-Language": "az-AZ,az;q=0.9,ru;q=0.8,en;q=0.7",
        }

    def _clean_price(self, raw_price: str) -> float:
        try:
            clean_str = raw_price.replace('AZN', '').replace('₼', '').replace(' ', '').strip()
            clean_str = clean_str.replace(',', '.')
            match = re.search(r'\d+\.?\d*', clean_str)
            if match:
                return float(match.group())
            else:
                raise ValueError(f"Число не найдено: '{raw_price}'")
        except Exception as e:
            logger.error(f"Ошибка очистки цены '{raw_price}': {e}")
            raise

    def get_price(self, url: str, css_selector: str) -> Optional[float]:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.select_one(css_selector)
            
            if not price_element:
                return None
                
            return self._clean_price(price_element.get_text())
            
        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {e}")
            return None