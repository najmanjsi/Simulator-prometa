from tabulate import tabulate
import pandas as pd
import os
import sys
import numpy as np


def stringify(x: list) -> str:
    string = ''
    for e in x:
        string += e + ' | '
    return string


def csv_to_pickle(filepath: str, outputpath: str = None):

    MIO = 1_000_000
    BYTES_FOR_A_NUMBER = 182_943_047

    # if the output path is not specified, set it to './data/filename.pkl'
    if outputpath is None:
        outputpath = './data/' + filepath.split('/')[-1].split('.')[0] + '.pkl'

    # totally unnecessary stuff for the progress 'bar'
    filesize = os.path.getsize(filepath)
    #numbers = filesize // BYTES_FOR_A_NUMBER + 1

    number_of_lines = -1

    # '../../../Downloads/minute_full_station_merged.csv'
    with open(filepath, encoding='utf-8') as f:

        # attribute names
        headers = f.readline().strip().split(',')

        # elements (lines)
        content = []

        # some estimates for the progress 'bar'
        first_line = f.readline()
        line_length = sys.getsizeof(first_line)
        print(line_length)
        print(len(first_line) * 2)
        content.append(first_line.strip().split(','))
        number_of_lines = filesize // (len(first_line) * 2)
        numbers = number_of_lines // MIO + 1

        print(f'Reading dataset (0/{numbers}) ... ', end='', flush=True)

        for i, line in enumerate(f):
            line = line.strip().split(',')
            content.append(line)

            if i % MIO == 0:
                print(i // MIO, end=' ', flush=True)
            
            number_of_lines = i
        
        print(f'21\nReading finished ({numbers}/{numbers}) - all {round(number_of_lines / MIO, 2)} million lines read')

        # create table
        #table = tabulate(content, headers=headers)

        # create dataframe
        df = pd.DataFrame(content, columns=headers)
        #'./data/minute_full_station_merged.pkl'
        df.to_pickle(outputpath)
        print(df.head(20))

#print('reading pickle ...')
#df = pd.read_pickle('./data/minute_full_station_merged.pkl')
#print('reading finished')
#print(df.head(10))

#df_small = df.iloc[:2_000_000].copy()
#df_small.to_pickle('./data/mfsm_2mio_lines.pkl')

df = pd.read_pickle('./data/minute_full_station_merged.pkl')

# attribute names: 'STM', 'DIR', 'Err', 'Mot', 'Osebni', 'BUS', 'LTov', 'STov', 'TTov', 'TSP', 'Vlac', 'OCC', 'GAP', 'VMIN', 'VAVG', 'VMAX', 'Time', 'FULL', 'NAME', 'SRC\n'

# select numeric columns
#numeric_cols = df.select_dtypes(include='number').columns

# grouping
#df_agg = df.groupby(df.columns[:2])[numeric_cols].sum().reset_index()
#print(df.head(100))
#print(df_agg.head(100))


# uncertain counters (usually of the pattern xxxx-xx(a|0|6))
# 1005-23(a|0)

def counter_working_months(counter_id: str) -> str:
    result = ''

    years_months = list({t[:7] for t in df.loc[df['STM'] == counter_id]['Time']})
    years_months.sort()

    prev = ''
    for date in years_months:
        y, m = date.split('-')
        if prev != y:
            result += f'\n{y}: {m}'
            #print(f'\n{y}: {m}', end='')
        else:
            result += f', {m}'
            #print(f', {m}', end='')
        prev = y
    result += '\n'
    #print('\n\n------------------------------------------', end='')
    return result

#counter_working_months('1005-23a')
#counter_working_months('1005-230') - is empty

# števci na spodnjem delu Celovške ceste (Ruska - Tivolska) - 1027, 1028
# rabimo per-hour-rate
celovska_podvoz_severno = df.loc['1028' in df['STM']].iloc[:10]
#celovska_podvoz_juzno = df.loc['1027' in df['STM']]

print(celovska_podvoz_severno)
