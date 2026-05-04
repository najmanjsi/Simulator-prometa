import xml.etree.ElementTree as ET


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



generate_edgedata_file(['1000', '2000'], ['200', '150'], 1)