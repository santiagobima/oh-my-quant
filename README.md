# 📈 Oh My Quant – Investment Dashboard in Search of Alpha

**Final project of Python Bootcamp – Flask web app for financial analysis and prediction.**

This application connects financial data from yfinance, stores it in PostgreSQL, analyzes it with pandas and scikit-learn, and displays dashboards using Plotly.

---

## 🚀 Features

- ✅ User login (admin & client)
- ✅ Fetch financial data from yfinance
- ✅ Store data in PostgreSQL
- ✅ Data visualization with Plotly
- ✅ Basic ML prediction (regression/classification)
- ✅ Clean UI with HTML + Bootstrap
- ✅ Built with Python & Flask

---

## 🧰 Tech Stack

| Layer       | Tools                         |
|-------------|-------------------------------|
| Backend     | Flask, Python                 |
| Database    | PostgreSQL + psycopg2         |
| Data/ML     | pandas, scikit-learn, yfinance|
| Frontend    | HTML, CSS (Bootstrap), Plotly |
| Config      | python-dotenv, .env file      |
| Versioning  | Git + GitHub                  |

---

## 📁 Project Structure

oh-my-quant/
├── app/              ← Web app logic (Flask)
├── ml/               ← ML models & utils
├── scripts/          ← Data fetching tools
├── data/             ← Local raw data
├── main.py           ← Entry point
├── config.py         ← App config
├── .env              ← Environment variables
├── requirements.txt  ← Dependencies
└── README.md         ← You’re here!
