import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

AIRPORTS_FILE = os.path.join(DATA_DIR, "airports.dat")
ROUTES_FILE = os.path.join(DATA_DIR, "routes.dat")


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

            graph[source].append(destination)

    return graph


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


if __name__ == "__main__":
    main()