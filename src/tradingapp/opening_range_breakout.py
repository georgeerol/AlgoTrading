"""
Opening Range Breakout Strategy
Note:
This script is meant to be schedule through the OS.
"""

import sqlite3
from tradingapp import config
import smtplib
import ssl
import alpaca_trade_api as tradeapi
import datetime as dt
from tradingapp.timezone import is_dst

# Create a secure SSL context
context = ssl.create_default_context()

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id FROM strategy WHERE name = 'opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    SELECT symbol, name
    FROM stock
    JOIN stock_strategy ON stock_strategy.stock_id = stock.id
    WHERE stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

current_date = dt.date.today().isoformat()

if is_dst():
    start_minute_bar = f"{current_date} 09:30:00-05:00"
    end_minute_bar = f"{current_date} 09:45:00-05:00"
else:
    start_minute_bar = f"{current_date} 09:30:00-04:00"
    end_minute_bar = f"{current_date} 09:45:00-04:00"

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

orders = api.list_orders(status="all", limit=500, after=current_date)
existing_order_symbols = [order.symbol for order in orders if order.status != 'canceled']

messages = []

for symbol in symbols:
    minute_bars = api.get_barset(symbol, '1Min', start=current_date, end=current_date).df

    opening_range_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    opening_range_bars = minute_bars[symbol].loc[opening_range_mask]
    if not opening_range_bars.empty:
        opening_range_low = opening_range_bars['low'].min()
        opening_range_high = opening_range_bars['high'].max()
        opening_range = opening_range_high - opening_range_low

        after_opening_range_mask = minute_bars.index >= end_minute_bar
        after_opening_range_bars = minute_bars[symbol].loc[after_opening_range_mask]
        after_opening_range_breakout = after_opening_range_bars[after_opening_range_bars['close'] > opening_range_high]

        if not after_opening_range_breakout.empty:
            if symbol not in existing_order_symbols:
                limit_price = after_opening_range_breakout.iloc[0]['close']

                messages.append(
                    f"Placing order for {symbol} at {limit_price}, closed above {opening_range_high}\n\n{after_opening_range_breakout.iloc[0]}\n\n")
                print(
                    f"Placing order for {symbol} at {limit_price}, closed above {opening_range_high} at {after_opening_range_breakout.iloc[0]}")

                try:
                    api.submit_order(
                        symbol=symbol,
                        side="buy",
                        type="limit",
                        qty='100',
                        time_in_force="day",
                        order_class="bracket",
                        limit_price=limit_price,
                        take_profit=dict(
                            limit_price=limit_price + opening_range,
                        ),
                        stop_loss=dict(
                            stop_price=limit_price - opening_range,
                        )
                    )
                except Exception as e:
                    print(f"Could not submit order {e}")
            else:
                print(f"Already an order for {symbol}, skipping")

with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT, context=context) as server:
    server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)

    email_message = f"Subject: Trade Notifications for {current_date}\n\n"
    email_message += "\n".join(messages)

    server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, email_message)
