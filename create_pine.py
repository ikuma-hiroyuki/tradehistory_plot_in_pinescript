import datetime
import csv
import operator
import os
import sys
from datetime import datetime as dt


def SetTickerRoot(_ticker: str, date: dt):
    tz = 5  # CMEはのタイムゾーンは-5
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
        tz = 4  # NYSEは-4
    return _ticker, (date + datetime.timedelta(hours=tz)).isoformat()


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
            ticker_root, iso = SetTickerRoot(
                ticker, dt.strptime(row[6], '%Y-%m-%d, %H:%M:%S'))
            volume = row[7].replace(',', '')
            price = row[8].replace('$', '').replace(',', '')

            if history[0] == []:
                history[0] = [ticker_root, ticker, price, volume, iso]
            else:
                history.append([ticker_root, ticker, price, volume, iso])

    history.sort(key=operator.itemgetter(0, 4))

    with open('pine.txt', 'w', encoding='UTF-8') as pine_code:
        current_ticker = ''
        total = 0
        for record in history:
            root = record[0]
            if current_ticker != root:
                pine_code.writelines(f'\nif syminfo.root == "{root}"\n')
                total = 0

            ticker = record[1]
            price = record[2]
            volume = record[3]
            total += int(volume)
            iso = record[4]

            code = f'{" "*4}' \
                'PlotLabel('f'{volume}, {total}, {price}, "{ticker}", "{iso}"'')\n'
            pine_code.writelines(code)
            current_ticker = root

    print('Create text file.\n'
          'File is located in the same location as this executable.')
    input('')

elif target_csv == '':
    pass
else:
    print('File does not exist.')
    input('')
