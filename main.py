import logging
from datetime import datetime, timedelta
import random
from database import get_engine, get_session, Product, PriceHistory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("ETL")

def run_etl():
    engine = get_engine()
    session = get_session(engine)
    
    try:
        # 1. Заполняем корзину, если база пустая
        if session.query(Product).count() == 0:
            logger.info("Создаем базовую корзину товаров...")
            session.add_all([
                Product(name="Чай Azerçay 100г", category="Напитки", store_name="Bravo", base_weight=0.15, url="http://test.com/1", css_selector=".price"),
                Product(name="Хлеб заводской", category="Хлеб", store_name="Bazarstore", base_weight=0.35, url="http://test.com/2", css_selector=".price"),
                Product(name="Говядина 1кг", category="Мясо", store_name="Araz", base_weight=0.50, url="http://test.com/3", css_selector=".price")
            ])
            session.commit()

        products = session.query(Product).all()
        
        # 2. Генерируем историю за 10 дней для красивого графика (только при первом запуске)
        if session.query(PriceHistory).count() == 0:
            logger.info("Генерируем исторические данные за последние 10 дней для демо...")
            base_prices = {"Чай Azerçay 100г": 2.50, "Хлеб заводской": 0.70, "Говядина 1кг": 14.50}
            
            for days_ago in range(10, -1, -1):
                past_date = datetime.now() - timedelta(days=days_ago)
                for product in products:
                    trend = (10 - days_ago) * 0.003 # Легкая инфляция
                    noise = random.uniform(-0.02, 0.03)
                    price = round(base_prices[product.name] * (1 + trend + noise), 2)
                    
                    session.add(PriceHistory(product_id=product.id, current_price=price, date=past_date))
            session.commit()
            logger.info("Исторические данные успешно сгенерированы!")
        else:
            # 3. Ежедневный запуск (обычный режим)
            logger.info("Сбор свежих цен на сегодня...")
            for product in products:
                # В продакшене: price = scraper.get_price(product.url, product.css_selector)
                last_price = session.query(PriceHistory).filter_by(product_id=product.id).order_by(PriceHistory.date.desc()).first().current_price
                new_price = round(last_price * random.uniform(0.99, 1.02), 2) # Имитация изменения цены
                
                session.add(PriceHistory(product_id=product.id, current_price=new_price, date=datetime.now()))
            session.commit()
            logger.info("Свежие цены добавлены.")

    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()