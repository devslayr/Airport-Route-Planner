from queue import Queue
from distance import get_distance

def bfs_min_stops(graph, source, destination):
    queue = Queue()
    queue.enqueue((source, [source]))

    visited = set()
    visited.add(source)

    while not queue.is_empty():
        current, path = queue.dequeue()
        if current == destination:
            return path

        for connected_airport in graph[current]:
            if connected_airport not in visited:
                visited.add(connected_airport)
                queue.enqueue((connected_airport, path + [connected_airport]))
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
        for connected_airport in graph[current]:
            if connected_airport not in unvisited:
                continue

            edge_distance = get_distance(current, connected_airport, airports)
            new_distance = distances[current] + edge_distance
            
            if new_distance < distances[connected_airport]:
                distances[connected_airport] = new_distance
                previous[connected_airport] = current

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