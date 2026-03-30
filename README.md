# Baku Alternative CPI Tracker 📈

An automated data engineering pipeline that calculates an alternative Consumer Price Index (CPI) for Baku, Azerbaijan, based on real-time web scraping of local supermarket prices.

## 🚀 Features
- **ETL Pipeline:** Automated price collection using Python & BeautifulSoup.
- **Econometric Engine:** Implementation of the **Laspeyres Price Index** formula using Pandas.
- **Interactive Dashboard:** Real-time visualization built with Streamlit and Plotly.
- **Relational Database:** Robust price history storage using SQLAlchemy and SQLite.

## 📊 Methodology
The index is calculated using the Laspeyres formula:
$$I_L = \frac{\sum (p_{t} \cdot q_{0})}{\sum (p_{0} \cdot q_{0})} \times 100$$
Where $p_t$ is the current price, $p_0$ is the base price, and $q_0$ is the assigned weight in the consumer basket.

## 🛠 Tech Stack
- **Language:** Python 3.9+
- **Data:** Pandas, NumPy
- **Database:** SQLAlchemy (SQLite)
- **Scraping:** BeautifulSoup4, Requests
- **Visualization:** Streamlit, Plotly

## 💻 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize and collect data: `python main.py`
3. Launch dashboard: `python -m streamlit run app.py`
