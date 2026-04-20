# we'll make a csv with the following attributes: counter_id, road_name, direction, sumo_edge_id, notes

TEST2_DIRECTORY = '../simulations/small_tests/test2/'
COUNTER_IDS_TEST2_FILE_PATH = TEST2_DIRECTORY + 'stevci_ids_test2.txt'
COUNTERS_TABLE_TEST2_FILE_PATH = TEST2_DIRECTORY + 'stevci_preslikava.csv'

COUNTER_LOCATIONS_FILE_PATH = '../metadata/lokacije_stevcev.txt'
COUNTER_FULL_NAMES_FILES_PATH = '../metadata/polna_imena_stevcev.txt'


def get_counter_data_from_file(file: str) -> list:
    counters = []
    with open(file, encoding='utf-8') as f:
        for line in f:
            id, y, x = line.split(',')
            counters.append(id.strip())
    return counters


counter_ids_test2 = get_counter_data_from_file(COUNTER_IDS_TEST2_FILE_PATH)
