import pandas as pd
import sys
from collections import defaultdict


REDUCED_NETWORK_COUNTERS = ['1028-18a', '1028-180', '1027-166','1002-17a', '1002-170', '1935-230', '1935-238', '1056-186', '1055-166']
REDUCED_NETWORK_COUNTERS_WITH_1036 = ['1028-18a', '1002-17a', '1027-166', '1002-170', '1935-230', '1935-238', '1035-136', '1036-11a', '1036-116', '1028-180', '1056-186', '1055-166']
FULL_COUNTING_DATA_FILEPATH = '../data/minute_full_station_merged.pkl'
REDUCED_COUNTING_DATA_FILEPATH = '../data/reduced_area.pkl'


def create_reduced_pickle(big_pickle_filepath: str, small_pickle_outputpath: str, counters):

    df = pd.read_pickle(big_pickle_filepath)
    counters_df = df[(df['STM'].isin(counters))]
    counters_df.to_pickle(small_pickle_outputpath)


def extract_cars(counters: list, day: str, start_time: str, end_time: str, counting_data_filepath: str = FULL_COUNTING_DATA_FILEPATH, verbose : bool = False) -> dict:

    hour_diff, minute_diff = [int(end) - int(start) for end, start in zip(end_time.split(':'), start_time.split(':'))]
    number_of_intervals = hour_diff * 4 + minute_diff // 15

    if verbose:
        print('reading pickle...', end='', flush=True)
    #
    df = pd.read_pickle(counting_data_filepath)
    #
    if verbose:
        print(' done')

    if verbose:
        print('converting to datetime...', end='', flush=True)
    #
    df['Time'] = pd.to_datetime(df['Time'])
    #
    if verbose:
        print(' done')

    if verbose:
        print('creating interval dataframe...', end='', flush=True)
    #
    interval_df = df[
        (df['STM'].isin(counters)) &
        (df['Time'].dt.date == pd.to_datetime(day).date()) &
        (df['Time'].dt.time >= pd.to_datetime(start_time).time()) &
        (df['Time'].dt.time < pd.to_datetime(end_time).time())
    ]
    #
    if verbose:
        print(' done', end='\n')

    if verbose:
        print('making dictionary...', end='', flush=True)
    #
    result = (interval_df.groupby(['STM', 'DIR'])['Osebni'].apply(list).to_dict())
    #
    nested_result = defaultdict(dict)
    for (stm, dir), values in result.items():
        # fill in potential missing data
        if len(values) < number_of_intervals:
            if verbose:
                print(f'Only {len(values)}/{number_of_intervals} for key {stm} / {dir}')
            while len(values) < number_of_intervals:
                values.append('0')
        # nest lanes to counter ids
        nested_result[stm][dir] = values
    #
    if verbose:
        print(' done')

    if verbose:
        print(interval_df)
    #
    return nested_result


def prepare_for_edge_data(intervals: dict) -> dict:
    summed_by_lane = {}
    for counter, lanes in intervals.items():
        summed_by_lane[counter] = [str(sum(map(int, values))) for values in zip(*lanes.values())]
    
    # let's now invert the dictionary, so that we can just iterate over the intervals when generating the edgedata file
    by_intervals = [dict(zip(summed_by_lane.keys(), values)) for values in zip(*summed_by_lane.values())]
    return by_intervals


def csv2dict(csv_file: str) -> dict:
    mapping_dict = {}

    with open(csv_file, encoding='utf-8') as f:
        f.readline() # skip the header

        for line in f:
            cid, eid, _ = line.split(',')
            mapping_dict[cid] = eid
    
    return mapping_dict


def prepare_for_edge_data_v2(intervals: dict, cid2eid_csv: str) -> dict:
    cid2eid = csv2dict(cid2eid_csv)

    summed_by_lane = {}
    for counter, lanes in intervals.items():
        edge = cid2eid[counter]
        summed_by_lane[edge] = [str(sum(map(int, values))) for values in zip(*lanes.values())]
    
    # let's now invert the dictionary, so that we can just iterate over the intervals when generating the edgedata file
    by_intervals = [dict(zip(summed_by_lane.keys(), values)) for values in zip(*summed_by_lane.values())]
    return by_intervals


day = '2013-04-09'  # a tuesday - example full 'Time': 2016-03-01 00:45:00
start_hour = '05:00'
end_hour = '6:00'

#create_reduced_pickle(FULL_COUNTING_DATA_FILEPATH, '../data/reduced_area.pkl', REDUCED_NETWORK_COUNTERS_WITH_1036)

intervals = extract_cars(REDUCED_NETWORK_COUNTERS_WITH_1036, day, start_hour, end_hour, counting_data_filepath=REDUCED_COUNTING_DATA_FILEPATH, verbose=False)
#print(intervals)

intervals_for_edge_data = prepare_for_edge_data(intervals)
#print(intervals_for_edge_data)

