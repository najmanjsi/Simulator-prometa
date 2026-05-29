import xml.etree.ElementTree as ET
import extract_intervals


def generate_edgedata_file(counter_edges: list, counter_data: list, intervals: int):

    # Root element with attribute
    data = ET.Element("data", {"id": "counts"})

    for i in range(intervals):

        # Child element with attributes
        interval = ET.SubElement(data, "interval", {
            "begin": f"{i * 900}",
            "end": f"{(i + 1) * 900}"
        })

        for edge, edge_data in zip(counter_edges, counter_data):
            # Edge elements
            ET.SubElement(interval, "edge", {
                "id": edge,
                "entered": edge_data
            })

    # Pretty print (Python 3.9+)
    ET.indent(data, space="  ")

    # Write to file
    tree = ET.ElementTree(data)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True)


def generate_edgedata_file_v2(counter_data: dict, intervals: int):

    data = ET.Element("data", {"id": "counts"})
    
    for i in range(intervals):

        interval = ET.SubElement(data, "interval", {
            "begin": f"{i * 900}",
            "end": f"{(i + 1) * 900}"
        })

        for counter_id, car_counts in counter_data.items():

            single_count = str(int(car_counts[i]) + int(car_counts[i + intervals]))

            # Edge elements
            ET.SubElement(interval, "edge", {
                "id": counter_id,
                "entered": single_count
            })

    # Pretty print (Python 3.9+)
    ET.indent(data, space="  ")

    # Write to file
    tree = ET.ElementTree(data)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True)


def generate_edgedata_file_v3(intervals: list):
    data = ET.Element("data", {"id": "counts"})
    
    for i, elem in enumerate(intervals):

        interval = ET.SubElement(data, "interval", {
            "begin": f"{i * 900}",
            "end": f"{(i + 1) * 900}"
        })

        for counter_id, car_count in elem.items():

            # Edge elements
            ET.SubElement(interval, "edge", {
                "id": counter_id,
                "entered": car_count
            })

    # Pretty print (Python 3.9+)
    ET.indent(data, space="  ")

    # Write to file
    tree = ET.ElementTree(data)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True)


def generate_edgedata_file_v4(intervals: list, output_file: str = 'counts.xml'):
    data = ET.Element("data", {"id": "counts"})
    
    for i, elem in enumerate(intervals):

        interval = ET.SubElement(data, "interval", {
            "begin": f"{i * 900}",
            "end": f"{(i + 1) * 900}"
        })

        for edge_id, car_count in elem.items():

            # Edge elements
            ET.SubElement(interval, "edge", {
                "id": edge_id,
                "entered": car_count
            })

    # Pretty print (Python 3.9+)
    ET.indent(data, space="  ")

    # Write to file
    tree = ET.ElementTree(data)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


counters_list = ['1028-18a', '1002-17a', '1027-166', '1002-170', '1935-230', '1935-238', '1035-136', '1036-11a', '1036-116', '1028-180', '1056-186', '1055-166']
counting_filepath = '../data/reduced_area.pkl'
counter2edge_mapping_filepath = '../simulations/small_tests/test2/reduced_net_test3/stevci2edges_table.csv'
day = '2013-04-09'
start_hour = '04:00'
end_hour = '05:00'

intervals = extract_intervals.prepare_for_edge_data_v2(extract_intervals.extract_cars(counters_list, day, start_hour, end_hour, counting_filepath), counter2edge_mapping_filepath)
#intervals2 = [{'1002-17a': 13, '1027-166': 26, '1028-180': 29, '1035-136': 21, '1036-116': 18, '1055-166': 10, '1056-186': 13}, {'1002-17a': 36, '1027-166': 57, '1028-180': 54, '1035-136': 36, '1036-116': 36, '1055-166': 18, '1056-186': 15}, {'1002-17a': 52, '1027-166': 86, '1028-180': 110, '1035-136': 73, '1036-116': 47, '1055-166': 25, '1056-186': 34}, {'1002-17a': 66, '1027-166': 96, '1028-180': 117, '1035-136': 97, '1036-116': 61, '1055-166': 30, '1056-186': 36}]
#print(intervals)

generate_edgedata_file_v4(intervals)
