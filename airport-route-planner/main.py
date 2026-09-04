import os
import time

from data_loader import load_airports, load_routes
from distance import calculate_route_distance
from algorithms import bfs_min_stops, dijkstra_shortest_distance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

AIRPORTS_FILE = os.path.join(DATA_DIR, "airports.dat")
ROUTES_FILE = os.path.join(DATA_DIR, "routes.dat")

# AIRPORTS_FILE = "airport-route-planner/data/airports.dat"
# ROUTES_FILE = "airport-route-planner/data/routes.dat"


def main():
    airports = load_airports(AIRPORTS_FILE)
    graph = load_routes(ROUTES_FILE, airports)

    print("Airport Route Planner")
    print("----------------------------------------")

    source = input("Enter source airport IATA code: ").upper()
    destination = input("Enter destination airport IATA code: ").upper()

    # Validate source airport
    if source not in airports:
        print(f"Error: Airport code '{source}' does not exist.")
        return

    # Validate destination airport
    if destination not in airports:
        print(f"Error: Airport code '{destination}' does not exist.")
        return

    print()
    print(f"Finding routes from {source} to {destination}...")


    # BFS - Minimum-stop route
    start_time = time.perf_counter()
    bfs_route = bfs_min_stops(graph, source, destination)
    end_time = time.perf_counter()
    bfs_running_time = end_time - start_time

    print("\nMinimum-stop route:")

    if bfs_route:
        bfs_distance = calculate_route_distance(bfs_route, airports)
        print("Route:", " -> ".join(bfs_route))
        print("Number of flights:", len(bfs_route) - 1)
        print("Number of intermediate stops:", max(0, len(bfs_route) - 2))
        print(f"Total estimated distance: {bfs_distance:.2f} km")
        print(f"Running time: {bfs_running_time:.6f} seconds")
    else:
        print("No route found.")
        print(f"Running time: {bfs_running_time:.6f} seconds")


    # Dijkstra - Shortest distance
    start_time = time.perf_counter()
    dijkstra_route, dijkstra_distance = dijkstra_shortest_distance(graph, airports, source, destination)
    end_time = time.perf_counter()
    dijkstra_running_time = end_time - start_time

    print("\nShortest-distance route:")

    if dijkstra_route:
        print("Route:", " -> ".join(dijkstra_route))
        print("Number of flights:", len(dijkstra_route) - 1)
        print("Number of intermediate stops:", max(0, len(dijkstra_route) - 2))
        print(f"Total estimated distance: {dijkstra_distance:.2f} km")
        print(f"Running time: {dijkstra_running_time:.6f} seconds")
    else:
        print("No route found.")
        print(f"Running time: {dijkstra_running_time:.6f} seconds")


if __name__ == "__main__":
    main()