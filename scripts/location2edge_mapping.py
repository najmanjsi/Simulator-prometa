from sumolib.net import readNet
import argparse


#parser = argparse.ArgumentParser('loc2edge')
#parser.add_argument('network', help='Network file that should be searched for counter locations.')
#args = parser.parse_args()

#print(args.network)


NETWORK_FILE_PATH = '../simulations/small_tests/test1/working_simulation/network_corr1.net.xml'

#1027-166; 46.05939214417067, 14.498475690591329; - south - -983127894#0
#1028-18a; 46.057741464928675, 14.50035510918963; - north - 1184476405


def latlon2edge(lat: float, lon: float, network_file: str, radius: float = 5):
    net = readNet(network_file)
    x, y = net.convertLonLat2XY(lon, lat)
    edges = net.getNeighboringEdges(x, y, radius)

    if not edges:
        edges = net.getNeighboringEdges(x, y, radius * 3)
    
    closest_edge, dist = min(edges, key=lambda x: x[1])
    #print(f'Found edge {closest_edge.getID()} {round(dist, 2)} meters away from counter location.')
    print(closest_edge)
    print(closest_edge.getLanes()[1].getID())

    return closest_edge


latlon2edge(46.05939214417067, 14.498475690591329, NETWORK_FILE_PATH)

# now let's do this for test2 (or maybe test22) - the reduced simulation area proposed to me

