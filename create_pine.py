import datetime
import csv
import operator
import os
import sys
from datetime import datetime as dt


def SetTickerRoot(_ticker: str, date: dt):
    adjust = True
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
        adjust = False
    # 現物は+1日しないとTrading viewで1日ずれる
    return _ticker, date if adjust else date + datetime.timedelta(days=1)


target_csv = input('Input csv file path.\n').replace('"', '')

if os.path.isfile(target_csv):
    with open(target_csv, 'r', encoding='UTF-8') as f:
        try:
            next(f)
        except UnicodeDecodeError:
            input(f'{"*"*5} Error!! CSV file should be saved in UTF-8. {"*"*5}\n')
            sys.exit()

        reader = csv.reader(f)

        # リストに追加
        history = [[]]
        for row in reader:
            ticker = row[5]
            ticker_root, d = SetTickerRoot(
                ticker, dt.strptime(row[6], '%Y-%m-%d, %H:%M:%S'))
            volume = row[7]
            price = row[8]

            if history[0] == []:
                history[0] = [ticker_root, ticker, d, price, volume]
            else:
                history.append([ticker_root, ticker, d, price, volume])

    history.sort(key=operator.itemgetter(0, 2))

    with open('pine.txt', 'w', encoding='UTF-8') as pine_code:
        current_ticker = ''
        total = 0
        for record in history:
            root = record[0]
            if current_ticker != root:
                pine_code.writelines(f'\nif syminfo.root == "{root}"\n')
                total = 0

            ticker = record[1]
            year = record[2].year
            month = record[2].month
            day = record[2].day
            price = record[3]
            volume = record[4]
            total += int(volume)

            code = f'{" "*4}'  \
                'PlotLabel(' \
                f'{year}, {month}, {day}, {volume}, {total}, {price}, "{ticker}"' \
                ')\n'
            pine_code.writelines(code)
            current_ticker = root

elif target_csv == '':
    pass
else:
    print('File does not exist.')
    input('')
