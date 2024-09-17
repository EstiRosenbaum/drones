from unittest.mock import MagicMock

import pytest
from modules.calculate_area import convert_polygon_to_utm, get_area_in_km
from shapely.geometry import Polygon


def test_get_area_in_km():
    footprints = [
        [
            [32.62795535049612, 35.149691256695185],
            [32.4491110885965, 35.537654655739885],
            [32.19985326081084, 35.16712781395562],
            [32.62795535049612, 35.149691256695185],
        ]
    ]
    expected_area = 849.9700599702759
    assert pytest.approx(get_area_in_km(footprints), abs=1e-10) == expected_area


def test_get_area_in_km_multiple_polygons():
    footprints = [
        [
            [32.62795535049612, 35.149691256695185],
            [32.4491110885965, 35.537654655739885],
            [32.19985326081084, 35.16712781395562],
            [32.62795535049612, 35.149691256695185],
        ],
        [
            [33.62795535049612, 36.149691256695185],
            [33.4491110885965, 36.537654655739885],
            [33.19985326081084, 36.16712781395562],
            [33.62795535049612, 36.149691256695185],
        ],
    ]
    expected_area = 1691.5387254577636
    assert get_area_in_km(footprints) == expected_area


def test_get_area_in_km_empty_footprints():
    footprints = []
    expected_area = 0.0
    assert get_area_in_km(footprints) == expected_area


@pytest.fixture
def mock_pyproj_transformer(monkeypatch):
    mock_transformer = MagicMock()
    mock_transformer.from_crs.return_value = mock_transformer
    monkeypatch.setattr("modules.calculate_area.pyproj.Transformer", mock_transformer)
    return mock_transformer


def test_convert_polygon_to_utm(mock_pyproj_transformer):
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    zone_number = 30
    transformer = mock_pyproj_transformer
    convert_polygon_to_utm(polygon, zone_number)
    transformer.from_crs.assert_called_once_with("epsg:4326", f"epsg:326{zone_number}")
