import pandas as pd
import logging

logger = logging.getLogger("CPICalculations")

def calculate_laspeyres_index(price_history_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
    try:
        price_history_df['date'] = pd.to_datetime(price_history_df['date'])
        
        df = pd.merge(price_history_df, products_df, left_on='product_id', right_on='id', how='inner')
        
        # Находим базовые цены p0
        idx_min_dates = df.groupby('product_id')['date'].idxmin()
        base_prices = df.loc[idx_min_dates, ['product_id', 'current_price']]
        base_prices = base_prices.rename(columns={'current_price': 'base_price'})
        
        df = pd.merge(df, base_prices, on='product_id', how='left')
        
        # Расчет компонентов p_t*q_0 и p_0*q_0
        df['pt_q0'] = df['current_price'] * df['base_weight']
        df['p0_q0'] = df['base_price'] * df['base_weight']
        
        df['day'] = df['date'].dt.date
        daily_agg = df.groupby('day').agg(
            sum_pt_q0=('pt_q0', 'sum'),
            sum_p0_q0=('p0_q0', 'sum')
        ).reset_index()
        
        daily_agg['cpi'] = (daily_agg['sum_pt_q0'] / daily_agg['sum_p0_q0']) * 100
        result_df = daily_agg[['day', 'cpi']].rename(columns={'day': 'date'})
        result_df = result_df.sort_values('date').reset_index(drop=True)
        
        return result_df
        
    except Exception as e:
        logger.error(f"Ошибка расчета: {e}")
        raise