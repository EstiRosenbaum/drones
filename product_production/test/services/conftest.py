from unittest.mock import Mock

import pytest


@pytest.fixture
def queue_name():
    return "test_queue"


@pytest.fixture
def listener():
    return "test-listener"


@pytest.fixture
def connection():
    return "connection"


@pytest.fixture
def sender():
    return "test-sender"


@pytest.fixture
def date():
    return "2024-06-19T10:01:00"


@pytest.fixture
def mock_redis():
    return Mock()


@pytest.fixture
def information_entrance_approval(queue_name, listener, connection, sender):
    from services.information_entrance_approval import InformationEntranceApproval

    information_entrance_approval = InformationEntranceApproval(
        queue_name, listener, connection, sender
    )
    return information_entrance_approval


@pytest.fixture
def image(queue_name, listener, connection, sender):
    from services.image import Image

    image = Image(queue_name, listener, connection, sender)
    return image


@pytest.fixture
def end_systems_access_approval(queue_name, listener, connection, sender, mock_redis):
    from services.end_systems_access_approval import EndSystemsAccessApproval

    end_systems_access_approval = EndSystemsAccessApproval(
        queue_name, listener, connection, sender, mock_redis
    )
    return end_systems_access_approval


@pytest.fixture
def location_photography_request(queue_name, listener, connection, sender):
    from services.location_photography_request import LocationPhotographyRequest

    location_photography_request = LocationPhotographyRequest(
        queue_name, listener, connection, sender
    )
    return location_photography_request


@pytest.fixture
def flight_route(queue_name, listener, connection, sender):
    from services.flight_route import FlightRoute

    flight_route = FlightRoute(queue_name, listener, connection, sender)
    return flight_route


@pytest.fixture
def area_photography_request(queue_name, listener, connection, sender):
    from services.area_photography_request import AreaPhotographyRequest

    area_photography_request = AreaPhotographyRequest(
        queue_name, listener, connection, sender
    )
    return area_photography_request


@pytest.fixture
def sortie(queue_name, listener, connection, sender, mock_redis):
    from services.sortie import Sortie

    sortie = Sortie(
        queue_name, listener, connection, sender, redis_connection=mock_redis
    )
    return sortie


@pytest.fixture
def tagged_sortie(queue_name, listener, connection, sender, redis_instance):
    from services.tagged_sortie import TaggedSortie

    tagged_sortie = TaggedSortie(
        queue_name, listener, connection, sender, redis_instance
    )
    return tagged_sortie
