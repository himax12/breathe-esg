"""
Utility functions for emissions calculation.
"""

from math import radians, sin, cos, sqrt, atan2

# IATA airport coordinates (lat, lon in degrees)
# Sourced from openflights.org database
IATA_COORDINATES = {
    # Europe
    'LHR': (51.4706, -0.4619),   # London Heathrow
    'LGW': (51.1537, -0.1823),   # London Gatwick
    'CDG': (49.0097, 2.5479),    # Paris Charles de Gaulle
    'FRA': (50.0333, 8.5706),    # Frankfurt
    'AMS': (52.3105, 4.7683),    # Amsterdam Schiphol
    'MAD': (40.4936, -3.5668),   # Madrid Barajas
    'BCN': (41.2974, 2.0830),   # Barcelona
    'FCO': (41.8003, 12.2389),   # Rome Fiumicino
    'MUC': (48.3537, 11.7750),   # Munich
    'ZRH': (47.4647, 8.5492),   # Zurich
    'VIE': (48.1103, 16.5697),   # Vienna
    'CPH': (55.6180, 12.6561),   # Copenhagen
    'OSL': (60.1979, 11.1006),  # Oslo
    'ARN': (59.6519, 17.9186),   # Stockholm Arlanda
    'HEL': (60.3172, 24.9633),   # Helsinki
    'DUB': (53.4264, -6.2499),   # Dublin
    'BRU': (50.9014, 4.4844),    # Brussels
    'DUS': (51.2895, 6.7668),    # Dusseldorf
    'HAM': (53.6304, 9.9882),    # Hamburg
    'NCE': (43.6584, 7.2159),    # Nice
    'ATH': (37.9364, 23.9445),   # Athens
    'PRG': (50.1080, 14.6320),   # Prague
    'BUD': (47.4367, 19.2557),   # Budapest
    'WAW': (52.4247, 20.6497),   # Warsaw
    # North America
    'JFK': (40.6413, -73.7781),  # New York JFK
    'LAX': (33.9416, -118.4085), # Los Angeles
    'SFO': (37.7749, -122.4194), # San Francisco
    'ORD': (41.9742, -87.9073),  # Chicago O'Hare
    'ATL': (33.6407, -84.4277),  # Atlanta
    'DFW': (32.8998, -97.0403),  # Dallas Fort Worth
    'DEN': (39.8561, -104.6737), # Denver
    'SEA': (47.6062, -122.3321), # Seattle
    'MIA': (25.7959, -80.2870),  # Miami
    'BOS': (42.3656, -71.0096),  # Boston
    'PHX': (33.4352, -112.0101), # Phoenix
    'LAS': (36.0840, -115.1537), # Las Vegas
    'IAH': (29.9902, -95.3368),  # Houston Bush
    'MSP': (44.8848, -93.2223),  # Minneapolis
    'DTW': (42.2162, -83.3554),  # Detroit
    'PHL': (39.8729, -75.2437),  # Philadelphia
    'CLT': (35.2077, -80.9473),  # Charlotte
    'SLC': (40.7884, -111.9778), # Salt Lake City
    'BNA': (36.1263, -86.6774),  # Nashville
    'SAN': (32.7338, -117.1933), # San Diego
    'IAD': (38.9492, -77.4606),  # Washington Dulles
    'DCA': (38.8512, -77.0401),  # Washington Reagan
    'PDX': (45.5898, -122.5951), # Portland OR
    'AUS': (30.1945, -97.6655),  # Austin
    'MCO': (28.4312, -81.3081),  # Orlando
    # Middle East
    'DXB': (25.2532, 55.3657),   # Dubai
    'DOH': (25.2731, 51.5311),   # Doha
    'AUH': (24.4330, 54.6511),   # Abu Dhabi
    'RUH': (24.9577, 46.6988),   # Riyadh
    'JED': (22.3090, 39.1548),   # Jeddah
    'KWI': (29.2266, 47.9688),   # Kuwait
    # Asia
    'BOM': (19.0896, 72.8656),   # Mumbai
    'DEL': (28.5665, 77.1031),   # Delhi
    'SIN': (1.3644, 103.9915),   # Singapore Changi
    'HKG': (22.3080, 113.9185),  # Hong Kong
    'NRT': (35.7720, 140.3929),  # Tokyo Narita
    'HND': (35.5494, 139.7798),  # Tokyo Haneda
    'ICN': (37.4602, 126.4407),  # Seoul Incheon
    'PEK': (40.0799, 116.6031),  # Beijing Capital
    'PVG': (31.1434, 121.8052),  # Shanghai Pudong
    'CAN': (23.3924, 113.2988),  # Guangzhou
    'SZX': (22.6393, 114.1309),  # Shenzhen
    'KIX': (34.4320, 135.2339),  # Osaka Kansai
    'BKK': (13.6900, 100.7501),  # Bangkok
    'KUL': (3.1422, 101.6930),   # Kuala Lumpur
    'CGK': (-6.1275, 106.6537),   # Jakarta Soekarno
    'MNL': (14.5086, 121.0192),  # Manila
    # South America
    'GRU': (-23.4356, -46.4731), # Sao Paulo Guarulhos
    'GIG': (-22.8089, -43.2436), # Rio de Janeiro Galeao
    'EZE': (-34.8151, -58.3817), # Buenos Aires Ezeiza
    'SCL': (-33.3930, -70.7858), # Santiago
    'LIM': (-12.0219, -77.1143), # Lima
    'BOG': (4.7016, -74.1461),   # Bogota
    # Africa
    'JNB': (-26.1392, 28.2460),  # Johannesburg
    'CPT': (-33.9648, 18.6017),  # Cape Town
    'CAI': (30.1219, 31.4056),   # Cairo
    'NBO': (-1.3192, 36.9275),  # Nairobi
    'ADD': (8.9779, 38.7993),    # Addis Ababa
    'LOS': (6.4541, 3.3947),    # Lagos
    'CMN': (33.3679, -7.5898),   # Casablanca Mohammed V
    # Oceania
    'SYD': (-33.9399, 151.1753), # Sydney
    'MEL': (-37.6690, 144.8407), # Melbourne
    'BNE': (-27.3982, 153.0856), # Brisbane
    'PER': (-31.9403, 115.9672), # Perth
    'AKL': (-37.0082, 174.7850), # Auckland
}

# Earth radius in km
EARTH_RADIUS_KM = 6371


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate great circle distance between two points using haversine formula.
    """
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def get_iata_distance(origin_code, destination_code):
    """
    Calculate distance in km between two IATA airport codes.
    Returns None if either code is not in the database.
    """
    origin_code = origin_code.upper().strip() if origin_code else ''
    destination_code = destination_code.upper().strip() if destination_code else ''

    if origin_code not in IATA_COORDINATES or destination_code not in IATA_COORDINATES:
        return None

    origin_coords = IATA_COORDINATES[origin_code]
    dest_coords = IATA_COORDINATES[destination_code]

    return haversine_distance(
        origin_coords[0], origin_coords[1],
        dest_coords[0], dest_coords[1]
    )