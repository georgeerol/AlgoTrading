from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from src.tradingapp import config
import sqlite3
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, symbol, name FROM stock
        ORDER BY symbol;
    """)
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, symbol, name FROM stock WHERE symbol = ?;
    """, (symbol,))
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ?
        ORDER BY date DESC
    """, (row['id'],))

    bars = cursor.fetchall()
    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row,"bars": bars})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
