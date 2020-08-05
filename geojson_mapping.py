"""Geojson mapping"""
import time
import json
import itertools
from typing import Dict, List

from shapely.geometry import Polygon, Point


GEOJSON_FILE = ""
INPUT_ADDR_LATLNG = ""
OUTPUT_FILE = ""


def flatten(nested_list: List[List[List[float]]]) -> List[List[float]]:
    """Flatten nested list"""
    return list(itertools.chain.from_iterable(nested_list))


def get_coa_map() -> Dict[str, Polygon]:
    """Get geojson map data from Council of Argiculture"""
    coa_map = dict()
    with open(GEOJSON_FILE, "r") as f_reader:
        doc = json.load(f_reader)
        features = doc["features"]
        for feature in features:
            coa_map[feature["id"]] = Polygon(flatten(feature["geometry"]["coordinates"]))
    return coa_map


def main():
    """Main function"""
    coa_map = get_coa_map()
    f_writer = open(f"{OUTPUT_FILE}", "w")

    start = time.time()
    with open(f"{INPUT_ADDR_LATLNG}", "r") as f_reader:

        for i, line in enumerate(f_reader):
            line = line.strip()
            _, lat, lng = line.split(",")
            point = Point(float(lng), float(lat))
            for coa_id, polygon in coa_map.items():
                if polygon.contains(point):
                    f_writer.write(f"{line},{coa_id}\n")
                    print(i, line, coa_id)
    print(f"Total time:{(time.time() - start) / 60}s")
    f_writer.close()


if __name__ == "__main__":
    main()
