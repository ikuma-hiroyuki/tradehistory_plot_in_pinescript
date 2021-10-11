import csv
import operator
import os
import sys
from datetime import datetime as dt

target_csv = input('Input csv file path.\n').replace('"', '')
pine_code = open('pine.txt', 'w', encoding='UTF-8')


def SetTickerRoot(_ticker: str):
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
    with open(target_csv, 'r', encoding='UTF-8') as f:
        try:
            next(f)
        except UnicodeDecodeError:
            input(f'{"*"*5} Error!! CSV file should be saved in UTF-8. {"*"*5}\n')
            sys.exit()

        reader = csv.reader(f)
        sorted_csv = sorted(reader, key=operator.itemgetter(5))
        current_ticker = ''
        total = 0

        for row in sorted_csv:
            ticker = row[5]
            ticker_root = SetTickerRoot(ticker)

            if current_ticker != ticker_root:
                pine_code.writelines(f'\nif syminfo.root == "{ticker_root}"\n')
                total = 0

            d = dt.strptime(row[6], '%Y-%m-%d, %H:%M:%S')
            volume = row[7]
            price = row[8]
            total += int(volume)

            code = f'{" "*4}'  \
                'PlotLabel(' \
                f'{d.year}, {d.month}, {d.day}, {volume}, {total}, {price}, "{ticker}"' \
                ')\n'

            pine_code.writelines(code)
            current_ticker = ticker_root
    input('Complete!\nCreated a Pine script in the same location as this python script.')

elif target_csv == '':
    pass
else:
    print('File does not exist.')
    input('')
