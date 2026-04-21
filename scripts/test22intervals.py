import pandas as pd

CELOVSKA_JUZNO_DATA = '../data/celovska_podvoz_juzno.pkl'
CELOVSKA_SEVERNO_DATA = '../data/celovska_podvoz_severno.pkl'
FULL_PICKLE_DATA = '../data/minute_full_station_merged.pkl'
TEST2_DIR = '../simulations/small_tests/test2/'
TEST2_COUNTERS_FILE = TEST2_DIR + 'stevci_ids_test2.txt'

TIMEFRAMES = ['2019-04-01 08:00:00', '2019-04-01 08:15:00', '2019-04-01 08:30:00', '2019-04-01 08:45:00']

# loading data
#df = pd.read_pickle(FULL_PICKLE_DATA)
df_celovska_juzno = pd.read_pickle(CELOVSKA_JUZNO_DATA)
df_celovska_severno = pd.read_pickle(CELOVSKA_SEVERNO_DATA)
df = pd.concat([df_celovska_juzno, df_celovska_severno])

counter_list = ['1027-166', '1028-180']
#counter_list = ['1036-11a', '1036-116']
#with open(TEST2_COUNTERS_FILE, encoding='utf-8') as f:
#    for line in f:
#        id, _, _ = line.strip().split(',')
#        counter_list.append(id)



for counter in counter_list:
    for timeframe in TIMEFRAMES:
        df_selected_datetime = df.loc[df['STM'] == counter].loc[df['Time'] == timeframe]
        if len(df_selected_datetime) == 0:
            print(f'Data for counter {counter} at {TIMEFRAME} not in the dataset.')
        else:
            print(df_selected_datetime)
        print('-' * 200)
    print('\n' + ('-' * 200) + '\n')