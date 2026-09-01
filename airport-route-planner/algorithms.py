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

            edge_distance = get_distance(current, neighbour, airports)
            new_distance = distances[current] + edge_distance
            
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