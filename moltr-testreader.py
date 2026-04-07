from tabulate import tabulate
import pandas as pd


def stringify(x: list) -> str:
    string = ''
    for e in x:
        string += e + ' | '
    return string


with open('../../../Downloads/minute_full_station_merged.csv', encoding='utf-8') as f:

    # attribute names
    headers = f.readline().split(',')

    # elements (lines)
    content = []
    for line in f:
        line = line.strip().split(',')
        content.append(line)
    
    # create table
    table = tabulate(content, headers=headers)

    # create dataframe
    df = pd.DataFrame(content, columns=headers)
    print(df)