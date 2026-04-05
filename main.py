import logging
import time
from datetime import datetime
from database import get_engine, get_session, Product, PriceHistory
from scraper import PriceScraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("ETL_Production")

def run_etl():
    engine = get_engine()
    session = get_session(engine)
    scraper = PriceScraper() # Initialize our scraper
    
    try:
        # 1. Base basket with REAL links
        if session.query(Product).count() == 0:
            logger.info("Creating base basket with real products...")
            session.add_all([
                Product(
                    name="Sugar (Şəkər tozu) 1kg", 
                    category="Groceries", 
                    store_name="Bazarstore", 
                    base_weight=0.30, 
                    url="https://bazarstore.az/products/səkər-tozu-kg", 
                    css_selector=".price-item--regular" 
                ),
                Product(
                    name="Eggs (Giləzi 10 pcs)", 
                    category="Groceries", 
                    store_name="Bazarstore", 
                    base_weight=0.30, 
                    url="https://bazarstore.az/products/gilezi-yumurta-qablasdirma-10-lu", 
                    css_selector=".price-item--regular"
                ),
                Product(
                    name="Butter Spread (Kalinka 200g)", 
                    category="Dairy", 
                    store_name="Bazarstore", 
                    base_weight=0.40, 
                    url="https://bazarstore.az/products/kalinka-bitki-yag-spredi-200-q-82", 
                    css_selector=".price-item--regular"
                )
            ])
            session.commit()

        products = session.query(Product).all()
        
        # 2. Daily collection of REAL prices
        logger.info("Starting real price parsing...")
        for product in products:
            logger.info(f"Scraping price for: {product.name} ({product.store_name})")
            
            # RUN THE REAL SCRAPER
            real_price = scraper.get_price(product.url, product.css_selector)
            
            if real_price is not None:
                # If the price is found successfully, save to DB with current date
                session.add(PriceHistory(product_id=product.id, current_price=real_price, date=datetime.now()))
                logger.info(f"✅ Success! Price: {real_price} ₼")
            else:
                # If the site changed its design or the selector is wrong
                logger.warning(f"❌ Failed to find price for {product.name}. Check URL or selector.")
            
            # Mandatory pause (2 seconds) to avoid anti-bot blocks from the store
            time.sleep(2) 
            
        session.commit()
        logger.info("Price collection completed.")

    except Exception as e:
        session.rollback()
        logger.error(f"Critical error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()
