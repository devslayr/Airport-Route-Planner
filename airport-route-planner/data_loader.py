import csv

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