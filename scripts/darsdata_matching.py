import os
import pandas as pd
import datetime
import argparse
from collections import defaultdict
from sumolib.net import readNet
import json

import location2edge_mapping as l2e

#parser = argparse.ArgumentParser('read_parquet', suggest_on_error=True)
#parser.add_argument('-f', '--filetype', default='traffic', choices=['segments', 'traffic'], help='either "segments" (segment id to geometry mapping) or "traffic" (daily scraped files)')
#parser.add_argument('-t', '--tail', default=10, type=int, help='number of lines to be returned (at the end of the file)')
#args = parser.parse_args()

# this is (basically) the only argument (the only parameter you have to change)
NETWORK_FILE = '../simulations/small_tests/test2/reduced_net_test3/network_with_netconvert_options_corrected.net.xml'

DATA_DIR = "../data/scraperfiles/"
SEGMENTS_FILE = DATA_DIR + 'segments.parquet'

APP_FOLDER = './darsdatamappingapp/data/'
JSON_OUTPUT = APP_FOLDER + 'edge2segments.json'
PARQUET_OUTPUT = APP_FOLDER + 'segment2edge.parquet'
JSON_GEOMETRY = APP_FOLDER + 'geometry.json'
#TRAFFIC_DIR = os.path.join(DATA_DIR, "traffic")
#TODAY_FILE = datetime.datetime.now().strftime('%Y-%m-%d.parquet')

#segments_df = pd.read_parquet(SEGMENTS_FILE)
#traffic_df = pd.read_parquet(TRAFFIC_DIR + '/' + TODAY_FILE)

#segments_df['direction'] = segments_df['geometry'].apply(l2e.segment_direction)

def segment2edge(geometry, network):
    #segment_id = segment['segment_id']
    #geometry = segment_geometry #segment['geometry']

    #lat1, lon1 = geometry[0]
    #lat2, lon2 = geometry[-1]
    direction = l2e.segment_direction(geometry)

    edges = set() # i only want unique edge IDs, if a segment is fully on one edge, that's fine, it'll just return one edge ID
    for lat, lon in geometry:
        edge, _ = l2e.latlon2edge(lat, lon, network, radius=2, direction=direction, verbose=False)
        if edge is not None:
            edges.add(edge.getID())
        else:
            edges.add(None)

    #edge1, _ = l2e.latlon2edge(lat1, lon1, network, radius=2, direction=direction)
    #edge2, _ = l2e.latlon2edge(lat2, lon2, network, radius=2, direction=direction)

    return list(edges)
    
    # note: it would be better if i checked how much of the segment extends to either edge
    # but also, if i wanted a more accurate average congestion value (c) for an edge, i would have
    # to average it by segments' length
    # but that kind of accuracy maybe isn't even helpful, since c values are:
    #   1. only from cars with gps turned on
    #   2. i don't even know what it represents (probably some collection of speed, normal speed, normal congestion, ...)
    # so even if i try to be more accurate, it might give false results
    # i'll just average all the segments that extend to an edge in any way


def mapsegments2edges(network_file: str, segments_file: str) -> tuple[dict, list]:
    edge_segments = defaultdict(list) # edge_id: [segment_ids]
    mapping_rows = [] # segment_id, edge_id

    network = readNet(network_file)
    segments_df = pd.read_parquet(segments_file) # segment_id, geometry

    for row in segments_df.itertuples():

        segment_id = row.segment_id
        geometry = row.geometry

        edges = segment2edge(geometry, network)

        if any(edges): # just checking if we actually got any matched edges
            for edge_id in edges:
                mapping_rows.append({
                    'segment_id': segment_id,
                    'edge_id': edge_id
                })

                edge_segments[edge_id].append(segment_id)
    
    return edge_segments, mapping_rows


def geometry2json(parquet_file, json_file):
    df = pd.read_parquet(parquet_file)
    df['geometry'] = df['geometry'].apply(lambda g: g.tolist())

    df.to_json(json_file, orient='records')


edge2segments, mapping_rows = mapsegments2edges(NETWORK_FILE, SEGMENTS_FILE)

#mapping_df = pd.DataFrame(mapping_rows)
#mapping_df.to_parquet(DATA_DIR + 'segment2edge.parquet', index=False)
#mapping_df.to_parquet(PARQUET_OUTPUT, index=False)

#print(mapping_df['edge_id'].unique())
#print('\n----------------------------------------------------------\n')
#print(json.dumps(edge2segments, indent=4))

#with open(JSON_OUTPUT, 'w') as f:
#    json.dump(edge2segments, f)

#geometry2json(SEGMENTS_FILE, JSON_GEOMETRY)




#t = args.tail
#if args.filetype == 'segments':
#    print(segments_df.iloc[0]['geometry'])
#else:
#    pass
#    #print(traffic_df.tail(t))


