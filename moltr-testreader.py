from tabulate import tabulate
import pandas as pd


def stringify(x: list) -> str:
    string = ''
    for e in x:
        string += e + ' | '
    return string


def csv_to_pickle():
    MIO = 1000000

    with open('../../../Downloads/minute_full_station_merged.csv', encoding='utf-8') as f:

        # attribute names
        headers = f.readline().split(',')

        # elements (lines)
        content = []
        print('Reading dataset (0/21) ... ', end='', flush=True)
        for i, line in enumerate(f):
            line = line.strip().split(',')
            content.append(line)

            if i % MIO == 0:
                print(i // MIO, end=' ', flush=True)
        
        print('21\nReading finished (21/21) - all 20.4 million lines read')

        # create table
        #table = tabulate(content, headers=headers)

        # create dataframe
        df = pd.DataFrame(content, columns=headers)
        df.to_pickle('./data/minute_full_station_merged.pkl')
        print(df.head(20))

csv_to_pickle()