import os
import csv
import operator
from datetime import datetime as dt


target_csv = input('Input csv file path.\n')
target_csv = target_csv.replace('"', '')
pine_code = open('pine.txt', 'w', encoding='UTF-8')


def TickerAdjust(_ticker: str):
    if ('NQ' in _ticker):
        _ticker = 'NQ'
    elif ('ES' in _ticker):
        _ticker = 'ES'
    elif ('ZB' in _ticker):
        _ticker = 'ZB'
    elif ('UB' in _ticker):
        _ticker = 'UB'
    elif ('USD.JPY' == _ticker):
        _ticker = 'USDJPY'
    else:
        _ticker
    return _ticker


if os.path.isfile(target_csv):
    with open(target_csv, encoding='utf-8') as f:
        next(f)
        reader = csv.reader(f)
        sorted_csv = sorted(reader, key=operator.itemgetter(5))
        current_ticker = ''

        for row in sorted_csv:
            ticker = row[5]
            ticker_adj = TickerAdjust(ticker)
            day = dt.strptime(row[6], '%Y-%m-%d, %H:%M:%S')
            volume = row[7]
            price = row[8]

            if current_ticker != ticker_adj:
                pine_code.writelines(f'\nif syminfo.root == "{ticker_adj}"\n')

            code = f'{" "*4}'  \
                f'PlotLabel({day.year}, {day.month}, {day.day}, {volume}, {price}, "{ticker}")\n'
            pine_code.writelines(code)
            current_ticker = ticker_adj

elif target_csv == '':
    pass
else:
    print('The file does not exist.')
    input('')
