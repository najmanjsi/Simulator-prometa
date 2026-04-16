# code for extracting only the counters within the input bounding box (4 coordinate pairs)

DEFAULT_BBOX = (14.49620, 14.50963, 46.05045, 46.06111)


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


def counters_in_bounding_box(counter_locations_path: str = 'lokacije_stevcev.txt', bbox: tuple = DEFAULT_BBOX, is_Slovenia = True) -> list:
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


def counter_id2name(counter_id: str, id_name_path: str = 'polna_imena_stevcev.txt') -> str:
    '''
    Maps counter's ID to its descriptive name
    '''

    with open(id_name_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip().lstrip('CSV:').lstrip('EXC:')

            if line.startswith(counter_id):
                return line.lstrip(counter_id + '-')
    
    return ''


# let's find the counters we want

counter_subset = counters_in_bounding_box()

for c_id, y, x in counter_subset:
    c_name = counter_id2name(c_id)
    print(f'{c_id}: {c_name if c_name else 'could not find counter id'}, ({y}, {x})')
