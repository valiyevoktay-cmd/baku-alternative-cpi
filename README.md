# 📈 Baku Alternative CPI Tracker

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

> An independent, automated data engineering pipeline designed to calculate an alternative Consumer Price Index (CPI) for Baku based on real-time microeconomic data.

## 🚀 Project Overview
Official inflation metrics often rely on aggregated, lagging indicators. This project takes a bottom-up approach to capture true market price signals by scraping daily grocery prices directly from local supermarkets. It serves as both a comprehensive Data Engineering showcase (ETL) and a practical microeconomic research tool.

## ⚙️ Core Features
* **Automated ETL Pipeline:** Robust web scraping engine using `BeautifulSoup4` and `Requests` to extract clean price data.
* **Econometric Engine:** Dynamic calculation of the Laspeyres Price Index using `Pandas`.
* **Interactive Dashboard:** Real-time data visualization deployed on **Streamlit Cloud**.
* **Relational Storage:** Persistent price history tracking powered by `SQLAlchemy` and `SQLite`.

## 📊 Economic Methodology
The index strictly follows the **Laspeyres Price Index** formula to measure changes in the cost of a fixed basket of goods:

$$I_L = \frac{\sum (p_t \cdot q_0)}{\sum (p_0 \cdot q_0)} \times 100$$

Where:
* $p_t$ = Current price of the item.
* $p_0$ = Base price of the item.
* $q_0$ = Assigned weight (quantity) in the consumer basket.

## 🛠 Tech Stack
* **Language:** Python 3.9+
* **Data Processing:** Pandas, NumPy
* **Database:** SQLAlchemy (SQLite)
* **Web Scraping:** BeautifulSoup4, Requests
* **Visualization:** Streamlit, Plotly

## 💻 How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
Run the ETL pipeline (collect real prices):

Bash
python main.py
Launch the dashboard:

Bash
python -m streamlit run app.py
Note: The public version of this repository uses simulated h<img width="1859" height="925" alt="image (2)" src="https://github.com/user-attachments/assets/0e820b8f-998c-4009-937b-24e281ea7b41" />
istorical data to demonstrate dashboard visualization capabilities. To use it as an actual tracking tool, clear the database and run the scraper locally to build your own real-time dataset.
