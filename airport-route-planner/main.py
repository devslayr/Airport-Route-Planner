import csv
import os
import math


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")

# AIRPORTS_FILE = os.path.join(DATA_DIR, "airports.dat")
# ROUTES_FILE = os.path.join(DATA_DIR, "routes.dat")

AIRPORTS_FILE = "airport-route-planner/data/airports.dat"
ROUTES_FILE = "airport-route-planner/data/routes.dat"

class Queue:
    def __init__(self):
        self.items = []
        self.front = 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None

        item = self.items[self.front]
        self.front += 1
        return item

    def is_empty(self):
        return self.front >= len(self.items)

def load_airports(filename):
    airports = {}

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            iata_code = row[4]

            if iata_code == r"\N" or not iata_code:
                continue

            airports[iata_code] = {
                "name": row[1],
                "country": row[3],
                "latitude": float(row[6]),
                "longitude": float(row[7])
            }

    return airports

def load_routes(filename, airports):
    graph = {}

    # Create an empty adjacency list for every valid airport
    for code in airports:
        graph[code] = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            source = row[2]
            destination = row[4]

            # Ignore invalid or missing airport codes
            if source == r"\N" or destination == r"\N":
                continue

            # Only include routes where both airports exist
            if source not in airports or destination not in airports:
                continue

            if destination not in graph[source]:
                graph[source].append(destination)

    return graph

def haversine(lat1, lon1, lat2, lon2):
    EARTH_RADIUS_KM = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c

def get_distance(code1, code2, airports):
    airport1 = airports[code1]
    airport2 = airports[code2]

    return haversine(
        airport1["latitude"],
        airport1["longitude"],
        airport2["latitude"],
        airport2["longitude"]
    )

def bfs_min_stops(graph, source, destination):
    queue = Queue()
    queue.enqueue((source, [source]))

    visited = set()
    visited.add(source)

    while not queue.is_empty():
        current, path = queue.dequeue()

        if current == destination:
            return path

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.enqueue(
                    (neighbour, path + [neighbour])
                )

    return None


def main():
    airports = load_airports(AIRPORTS_FILE)
    graph = load_routes(ROUTES_FILE, airports)

    print("Number of airports loaded:", len(airports))

    total_routes = sum(len(neighbours) for neighbours in graph.values())
    print("Number of routes loaded:", total_routes)

    print("\nExample airport:")
    if "SGN" in airports:
        print("SGN:", airports["SGN"])

    print("\nDirect routes from SGN:")
    if "SGN" in graph:
        print(graph["SGN"][:20])

    # Test Haversine distance
    if "SGN" in airports and "SIN" in airports:
        distance = get_distance("SGN", "SIN", airports)
        print(f"\nEstimated SGN -> SIN distance: {distance:.2f} km")


if __name__ == "__main__":
    main()