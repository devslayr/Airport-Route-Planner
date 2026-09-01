import math

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