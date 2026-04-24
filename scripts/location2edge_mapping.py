from sumolib.net import readNet
from sumolib.geomhelper import polygonOffsetWithMinimumDistanceToPoint
import argparse


#parser = argparse.ArgumentParser('loc2edge')
#parser.add_argument('network', help='Network file that should be searched for counter locations.')
#args = parser.parse_args()

#print(args.network)


ONE_ROAD_NETWORK_FILE_PATH = '../simulations/small_tests/test1/working_simulation/network_corr1.net.xml'
SIMPLE_NETWORK_FILE_PATH = '../simulations/small_tests/test2/network_test222.net.xml'
COUNTERS_FOR_SIMPLE_NETWORK_FILE_PATH = '../simulations/small_tests/test2/stevci_ids_test2.txt'

#1027-166; 46.05939214417067, 14.498475690591329; - south - -983127894#0
#1028-18a; 46.057741464928675, 14.50035510918963; - north - 1184476405


def latlon2edge(lat: float, lon: float, network: any, radius: float = 5, print_all_edges: bool = False):
    #net = readNet(network_file)
    if type(network) == str:
        network = readNet(network)

    x, y = network.convertLonLat2XY(lon, lat)
    edges = network.getNeighboringEdges(x, y, radius)

    if not edges:
        radius = radius * 3
        edges = network.getNeighboringEdges(x, y, radius)
    
    if not edges:
        print('No edges found', end=' - ')
        return None, -1

    closest_edge, dist = min(edges, key=lambda x: x[1])
    #print(f'Found edge {closest_edge.getID()} {round(dist, 2)} meters away from counter location.')
    #print(closest_edge)
    # there's also an Edge function getLanes(), which could be useful for making induction loops (since they are lane-based)

    if print_all_edges:
        print(f'(all edges within {radius}m: {[e.getID() + f' ({round(d, 2)}m)' for e, d in edges]})', end=' - ')

    if dist < 2:
        print('Edge probably correct', end=' - ')
    else:
        print('Edge might be incorrect', end=' - ')

    # let's also calculate the positon of the counter on the edge
    offset = polygonOffsetWithMinimumDistanceToPoint((x, y), closest_edge.getShape())

    return closest_edge, offset



# now let's do this for test2 (or maybe test22) - the reduced simulation area proposed to me
counter_edges = {}

# additional two: '1027-166', '1028-180'

with open(COUNTERS_FOR_SIMPLE_NETWORK_FILE_PATH, encoding='utf-8') as f:
    net = readNet(SIMPLE_NETWORK_FILE_PATH)

    header = f.readline()
    for line in f:
        #print('\n' + line)
        cid, lat, lon = line.strip().split(',')
        lat = float(lat.strip())
        lon = float(lon.strip())

        print(cid, end=': ')

        edge, offset = latlon2edge(lat, lon, net, print_all_edges=True)
        counter_edges[cid] = edge, offset

        # for output
        eid, elen = '/', -1
        if edge is not None:
            eid = edge.getID()
            elen = edge.getLength()
        
        print(f'{eid}, offset = {round(offset)}m / {round(elen)}m (counter lat, lon: {lat}, {lon})')
