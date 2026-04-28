from sumolib.net import readNet
from sumolib.geomhelper import polygonOffsetWithMinimumDistanceToPoint
import argparse
import math


#parser = argparse.ArgumentParser('loc2edge')
#parser.add_argument('network', help='Network file that should be searched for counter locations.')
#args = parser.parse_args()

#print(args.network)


ONE_ROAD_NETWORK_FILE_PATH = '../simulations/small_tests/test1/working_simulation/network_corr1.net.xml'
SIMPLE_NETWORK_FILE_PATH = '../simulations/small_tests/test2/network_with_netconvert_options.net.xml'
COUNTERS_FOR_SIMPLE_NETWORK_FILE_PATH = '../simulations/small_tests/test2/stevci_ids_test2.txt'

OFF_MAP_COUNTER_IDS = ['1035', '1036']

#1027-166; 46.05939214417067, 14.498475690591329; - south - -983127894#0
#1028-18a; 46.057741464928675, 14.50035510918963; - north - 1184476405


# helpers

def normalize(v: tuple):
    length = math.sqrt((v[0] ** 2) + (v[1] ** 2))
    return (v[0] / length, v[1] / length)


def dot(a: tuple, b: tuple):
    return (a[0] * b[0]) + (a[1] * b[1])


def edge_direction(edge):
    shape = edge.getShape()
    x1, y1 = shape[0]
    x2, y2 = shape[-1]
    return normalize((x2 - x1, y2 - y1))


def counter_direction_vector(direction: str):
    return {
        'N': (0, 1),
        'S': (0, -1),
        'E': (1, 0),
        'W': (-1, 0),
        'NE': normalize((1, 1)),
        'NW': normalize((-1, 1)),
        'SE': normalize((1, -1)),
        'SW': normalize((-1, -1))
    }.get(direction, (0, 0))


def latlon2edge(lat: float, lon: float, network: any, radius: float = 5, direction: str = 'X', print_all_edges: bool = False):
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

    counter_vec = counter_direction_vector(direction)

    possible_edges = {}
    best_edge, best_score = None, -100
    for edge, dist in edges:
        edge_dir = edge_direction(edge)
        alignment = dot(counter_vec, edge_dir)

        if alignment > 0.5:
            possible_edges[edge.getID()] = dist

        score = alignment - 0.05 * dist
        if score > best_score:
            best_edge, best_score = edge, score
    
    closest_edge, closest_dist = best_edge, possible_edges.get(best_edge, -2)

        #print(f'{e.getID()}: {round(alignment, 2)}')

    #closest_edge, dist = min(edges, key=lambda x: x[1])
    #print(f'Found edge {closest_edge.getID()} {round(dist, 2)} meters away from counter location.')
    #print(closest_edge)
    # there's also an Edge function getLanes(), which could be useful for making induction loops (since they are lane-based)

    if print_all_edges:
        print(f'(all edges within {radius}m: {[e + f' ({round(d, 2)}m)' for e, d in possible_edges.items()]})', end=' - ')

    if dist < 2:
        print('Edge probably correct', end=' - ')
    else:
        print('Edge might be incorrect', end=' - ')

    # let's also calculate the positon of the counter on the edge
    offset = polygonOffsetWithMinimumDistanceToPoint((x, y), closest_edge.getShape())

    return closest_edge, offset



# now let's do this for test2 (or maybe test22) - the reduced simulation area proposed to me
counter_edges = {}

# additional two: '1035-136', '1036-11a/6'

with open(COUNTERS_FOR_SIMPLE_NETWORK_FILE_PATH, encoding='utf-8') as f:
    net = readNet(SIMPLE_NETWORK_FILE_PATH)

    header = f.readline()
    for line in f:
        #print('\n' + line)
        cid, lat, lon, direction = line.strip().split(',')
        lat = float(lat.strip())
        lon = float(lon.strip())
        direction = direction.strip()

        print(cid, end=': ')

        r = 5
        if cid.split('-')[0].strip() in OFF_MAP_COUNTER_IDS:
            r = 250

        edge, offset = latlon2edge(lat, lon, net, r, direction, print_all_edges=False)
        counter_edges[cid] = edge, offset

        # for output
        eid, elen, eshape = '/', -1, []
        if edge is not None:
            eid = edge.getID()
            elen = edge.getLength()
        
        print(f'{eid}, offset = {round(offset)}m / {round(elen)}m (counter lat, lon: {lat}, {lon})')
