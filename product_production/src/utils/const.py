import os


class FoldersInRedis:
    COLLECTOR = "time_and_counter_collector"
    AREA_REQUESTS = "area_requests"
    LOCATION_REQUESTS = "location_requests"
    SORTIE = "sortie"
    SORTIES_UPLOADED = "sorties_uploaded"


class Indexes:
    DATES = "image_dates"
    AREA_PHOTOGRAPHY_REQUEST = "area_photography_request"
    END_SYSTEMS_ACCESS_APPROVAL = "end_systems_access_approval"
    FLIGHT_ROUTE = "flight_route"
    IMAGE = "image"
    INFORMATION_ENTRANCE_APPROVAL = "information_entrance_approval"
    LOCATION_PHOTOGRAPHY_REQUEST = "location_photography_request"
    SORTIE = "sortie"
    TAGGED_SORTIE = "tagged_sortie"


class Formats:
    DATE_TIME = "%Y-%m-%dT%H:%M:%S"
    DATE = "%Y-%m-%d"


class ProcessEnvs:
    MAX_WAITING_TIME = os.getenv("MAX_SORTIE_WAITING_TIME") or 3600
    TIME_INTERVAL = os.getenv("TIME_INTERVAL") or 60
