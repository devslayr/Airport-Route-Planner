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

def calculate_route_distance(route, airports):
    total_distance = 0.0

    for i in range(len(route) - 1):
        total_distance += get_distance(
            route[i],
            route[i + 1],
            airports
        )

    return total_distance

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

def dijkstra_shortest_distance(graph, airports, source, destination):
    distances = {}
    previous = {}
    unvisited = []

    for airport in airports:
        distances[airport] = float("inf")
        previous[airport] = None
        unvisited.append(airport)

    distances[source] = 0.0

    while unvisited:
        current = None
        current_distance = float("inf")

        # Find the unvisited airport with the smallest known distance
        for airport in unvisited:
            if distances[airport] < current_distance:
                current = airport
                current_distance = distances[airport]

        # No reachable airport remains
        if current is None:
            break

        # Destination reached
        if current == destination:
            break

        unvisited.remove(current)

        for neighbour in graph[current]:
            if neighbour not in unvisited:
                continue

            edge_distance = get_distance(
                current,
                neighbour,
                airports
            )

            new_distance = (
                distances[current]
                + edge_distance
            )

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

    # No route found
    if distances[destination] == float("inf"):
        return None, None

    # Reconstruct route
    route = []
    current = destination

    while current is not None:
        route.append(current)
        current = previous[current]

    route.reverse()

    return route, distances[destination]


def main():
    airports = load_airports(AIRPORTS_FILE)
    graph = load_routes(ROUTES_FILE, airports)

    print("Airport Route Planner")
    print("-" * 40)

    source = input("Enter source airport IATA code: ").strip().upper()
    destination = input("Enter destination airport IATA code: ").strip().upper()

    # Validate airport codes
    if source not in airports:
        print(f"Error: Airport code '{source}' does not exist.")
        return

    if destination not in airports:
        print(f"Error: Airport code '{destination}' does not exist.")
        return

    print(f"\nFinding routes from {source} to {destination}...")

    # -----------------------------------
    # BFS - Minimum-stop route
    # -----------------------------------
    bfs_route = bfs_min_stops(
        graph,
        source,
        destination
    )

    print("\nMinimum-stop route:")

    if bfs_route:
        bfs_distance = calculate_route_distance(
            bfs_route,
            airports
        )

        print("Route:", " -> ".join(bfs_route))
        print("Number of flights:", len(bfs_route) - 1)
        print(
            "Number of intermediate stops:",
            max(0, len(bfs_route) - 2)
        )
        print(
            f"Total estimated distance: "
            f"{bfs_distance:.2f} km"
        )

    else:
        print("No route found.")

    # -----------------------------------
    # Dijkstra - Shortest-distance route
    # -----------------------------------
    dijkstra_route, dijkstra_distance = (
        dijkstra_shortest_distance(
            graph,
            airports,
            source,
            destination
        )
    )

    print("\nShortest-distance route:")

    if dijkstra_route:
        print(
            "Route:",
            " -> ".join(dijkstra_route)
        )
        print(
            "Number of flights:",
            len(dijkstra_route) - 1
        )
        print(
            "Number of intermediate stops:",
            max(0, len(dijkstra_route) - 2)
        )
        print(
            f"Total estimated distance: "
            f"{dijkstra_distance:.2f} km"
        )

    else:
        print("No route found.")


if __name__ == "__main__":
    main()