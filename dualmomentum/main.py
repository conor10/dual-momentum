import datetime as dt

import matplotlib
matplotlib.use('Qt5Agg')  # must be specified before we import pyplot
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import quandl


QUANDL_AUTH_TOKEN = 'nWa2ZMz44c7gyZPzk8dW'


ADJ_CLOSE = 'Adj Close'


def run():
    quandl.get('LSE/VUSA', authtoken=QUANDL_AUTH_TOKEN)
    quandl.get('LSE/VUTY', authtoken=QUANDL_AUTH_TOKEN)

    end = dt.datetime.today()
    start = end - dt.timedelta(days=365)

    ivv = web.DataReader('IVV', 'yahoo', start, end)
    veu = web.DataReader('VEU', 'yahoo', start, end)
    bnd = web.DataReader('BND', 'yahoo', start, end)

    ivv_return = ivv[ADJ_CLOSE].pct_change().add(1).cumprod()
    veu_return = veu[ADJ_CLOSE].pct_change().add(1).cumprod()
    bnd_return = bnd[ADJ_CLOSE].pct_change().add(1).cumprod()

    ivv_return.rename('IVV', inplace=True)
    veu_return.rename('VEU', inplace=True)
    bnd_return.rename('BND', inplace=True)

    returns = pd.concat([ivv_return, veu_return, bnd_return], names=['IVV', 'VEU', 'BND'], axis=1)

    returns.plot(title='12 month returns')

    plt.show()


if __name__ == '__main__':
    run()
