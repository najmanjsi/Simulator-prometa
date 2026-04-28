# code for extracting only the counters within the input bounding box (4 coordinate pairs)

DEFAULT_BBOX = (14.49620, 14.50963, 46.05045, 46.06302)

COUNTERS_FULL_NAME_FILEPATH = '../metadata/polna_imena_stevcev.txt'
COUNTERS_LOCATION_FILEPATH = '../metadata/lokacije_stevcev.txt'

OUTPUT_FILE_PATH = '../simulations/small_tests/test2/stevci_ids_test2.txt'


def is_in_bounding_box(bbox: tuple[float], coords: tuple) -> bool:
    '''
    Returns true if the coordinates provided are within the bounding box limits.

    :param tuple bbox: (x1, x2, y1, y2) - Bounding box limits
    :param tuple coords: (x, y) - Coordinates to check
    '''

    x, y = coords
    x1, x2, y1, y2 = bbox

    if (min(x1, x2) < x and x < max(x1, x2)) and (min(y1, y2) < y and y < max(y1, y2)):
        return True

    return False


def counters_in_bounding_box(counter_locations_path: str = COUNTERS_LOCATION_FILEPATH, bbox: tuple = DEFAULT_BBOX, is_Slovenia = True) -> list:
    '''
    Returns a list of counter IDs (and their coordinates) that are located within the bounding box limits.
    Beware! Coordinates are sometimes (for example in Google Maps) represented by y, x (lat, long) instead of x, y (long, lat). This function automatically corrects this only for Slovenia.

    :param str counter_locations_path: the filepath where counter IDs and locations are stored. It has to be a CSV style file, delimiter is "; ", delimiter for coordinates is ", ". Locations need to be stored in x, y fashion (long, lat)
    :param tuple bbox: (x1, x2, y1, y2) - Bounding box limits (Default bbox is for the area of Bleiweisova-Celovška-Tivolska-Dunajska-Slovenska-Šubičeva)
    :return: [(ID, y, x), ...] - list with tuples of counter ID, y (lat) and x (long)
    :rtype: list
    '''

    counters_in = []

    with open(counter_locations_path, encoding='utf-8') as f:
        for line in f:
            if line.strip() == 'ENDOFCOUNTERS':
                f.close()
                break
            
            counter_id, location = line.strip().split('; ')[:2]
            x, y = location.split(', ')[:2]
            x = float(x)
            y = float(y)

            # correction for Google Maps coordinates (for Slovenia only)
            if is_Slovenia:
                if x > y:
                    x, y = y, x

            if is_in_bounding_box(bbox, (x, y)):
                counters_in.append((counter_id, y, x))

    return counters_in


def counter_id2name(counter_id: str, id_name_path: str = COUNTERS_FULL_NAME_FILEPATH) -> str:
    '''
    Maps counter's ID to its descriptive name
    '''

    with open(id_name_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip().lstrip('CSV:').lstrip('EXC:')

            if line.startswith(counter_id):
                return line.lstrip(counter_id + '-')
    
    return ''


def counter_id2direction(counter_id: str, id_name_path: str = COUNTERS_FULL_NAME_FILEPATH) -> str:
    '''
    Maps counter's ID to counter's lane direction (N, S, E, W, NE, NW, SE, SW, X)
    '''

    with open(id_name_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip().lstrip('CSV:').lstrip('EXC:')

            if line.startswith(counter_id):
                if line.endswith(')'):
                    descriptive_direction = line.split('(')[-1].rstrip(')')
                    return {
                        'sever': 'N',
                        'jug': 'S',
                        'vzhod': 'E',
                        'zahod': 'W',
                        'severovzhod': 'NE',
                        'severozahod': 'NW',
                        'jugovzhod': 'SE',
                        'jugozahod': 'SW'
                    }.get(descriptive_direction.lstrip('proti').rstrip('u'), 'X')
                        
                else:
                    return 'X'
    
    return ''


# let's find the counters we want

counter_subset = counters_in_bounding_box()

counters_with_location_and_direction = []
for cid, y, x in counter_subset:
    direction = counter_id2direction(cid)
    counters_with_location_and_direction.append((cid, y, x, direction))


for c_id, y, x in counter_subset:
    c_name = counter_id2name(c_id)
    #c_direction = counter_id2direction(c_id)
    print(f'{c_id}: {c_name if c_name else 'could not find counter id'}, ({y}, {x})')
    #print(f'{c_id}: {c_direction if c_direction else 'could not find counter lane direction'}, ({y}, {x})')
print(f'Število števcev na območju: {len(counter_subset)}')


# optional: save the counters to file
def write_counters_to_file(counters: list, file: str):
    with open(file, 'w', encoding='utf-8') as f:

        f.write('counter_id, lat, lon, direction\n')

        for c_id, y, x, direction in counters:
            f.write(f'{c_id.strip()}, {y}, {x}, {direction}\n')


#write_counters_to_file(counters_with_location_and_direction, OUTPUT_FILE_PATH)
