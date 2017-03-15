import datetime as dt
import operator

import matplotlib
matplotlib.use('Qt5Agg')  # must be specified before we import pyplot
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web


ADJ_CLOSE = 'Adj Close'
LOOKBACK = 365


US_SYMBOLS = ['IVV', 'VEU', 'BND']
UK_SYMBOLS = []


def run():
    _calc_returns(US_SYMBOLS)


def _calc_returns(symbols):
    end = dt.datetime.today()
    start = end - dt.timedelta(days=LOOKBACK)

    returns = []

    for symbol in symbols:
        returns.append(_get_returns(symbol, start, end))

    total_returns = dict(zip(symbols, [i[1] for i in returns]))
    sorted_returns = sorted(total_returns.items(), key=operator.itemgetter(1), reverse=True)

    print('12 Month Return')
    print('----------------')
    for r in sorted_returns:
        print('{:<10}{:>6.2%}'.format(r[0], r[1]))
    print('----------------')

    returns_df = pd.concat([i[0] for i in returns], names=symbols, axis=1)
    returns_df.plot(title='12 Month Returns')
    plt.show()


def _get_returns(symbol, start, end):
    prices = web.DataReader(symbol, 'yahoo', start, end)
    returns = prices[ADJ_CLOSE].pct_change().add(1).cumprod()
    returns.rename(symbol, inplace=True)

    total_return = returns[-1] - 1.
    return returns, total_return


if __name__ == '__main__':
    run()
