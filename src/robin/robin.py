import click, json
import robin_stocks as rh


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
        print("{}| {}".format(qte['symbol'], qte['ask_price']))


@main.command(help="Gets quotes for all stocks in your watchlist")
def watchlist():
    print("Getting quotes for watchlist")
    with open('watchlist')as f:
        symbols = f.read().splitlines()
    quotes = rh.get_quotes(symbols)
    for qte in quotes:
        print(qte)


if __name__ == '__main__':
    main()
