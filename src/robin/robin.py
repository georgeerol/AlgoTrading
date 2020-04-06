import click, json
import robin_stocks as rh
import ui


@click.group()
def main():
    print("Logging in")
    content = open('config.json').read()
    config = json.loads(content)
    rh.login(config['username'], config['password'], by_sms=False)


@main.command(help="Gets a stock quote for one or more symbols")
@click.argument('symbols', nargs=-1)
def quote(symbols):
    quotes = rh.get_quotes(symbols)
    print(quotes)
    for qte in quotes:
        ui.success("{}| {}".format(qte['symbol'], qte['ask_price']))


@main.command(help="Gets quotes for all stocks in your watchlist")
def watchlist():
    print("Getting quotes for watchlist")
    with open('watchlist')as f:
        symbols = f.read().splitlines()
    quotes = rh.get_quotes(symbols)
    for qte in quotes:
        ui.success("{}| {}".format(qte['symbol'], qte['ask_price']))


# robin.py buy 100 AAPL --limit 100
@main.command(help='Buy quantity of stocks by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def buy(quantity, symbol, limit):
    if limit is not None:
        ui.success("Buying {} of {} at {}".format(quantity, symbol, limit))
        result = rh.order_buy_limit(symbol, quantity, limit)
    else:
        # market order
        ui.success("Buying {} of {} at market price".format(quantity, symbol))
        result = rh.order_buy_market(symbol, quantity)
    if 'ref_id' in result:
        ui.success(result)
    else:
        ui.error(result)


@main.command(help='Sell quantity of stock by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def sell(quantity, symbol, limit):
    if limit is not None:
        ui.success("Selling {} of {} at {}".format(quantity, symbol, limit))
        result = rh.order_sell_limit(symbol, quantity, limit)
    else:
        # market order
        ui.success("Selling {} of {} at market price".format(quantity, symbol))
        result = rh.order_sell_market(symbol, quantity)
    if 'ref_id' in result:
        ui.success(result)
    else:
        ui.error(result)


if __name__ == '__main__':
    main()
