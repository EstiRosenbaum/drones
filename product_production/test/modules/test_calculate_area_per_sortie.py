from modules.calculate_area_per_sortie import _contains_coordinates, get_area_for_sortie


def test__contains_coordinates_with_correct_message(coordinates_obj):
    assert _contains_coordinates(coordinates_obj) is True


def test__contains_coordinates_false_when_message_is_not_dict(short_message):
    assert _contains_coordinates(short_message) is False


def test__contains_coordinates_false_when_message_has_no_coordinates(
    obj_without_coordinates,
):
    assert _contains_coordinates(obj_without_coordinates) is False


def test_get_area_for_sortie(
    mock_redis_sorties, patch_getArea, sortie_id, mock_get_area, coordinates
):
    with patch_getArea as getArea:
        res = get_area_for_sortie(sortie_id, mock_redis_sorties)
        getArea.assert_called_once_with(coordinates)
        mock_redis_sorties.get_folder_content.assert_called_once_with(sortie_id)
        mock_redis_sorties.delete_folder.assert_called_once_with(sortie_id)
        mock_redis_sorties.remove_obj_from_folder.assert_called_once_with(
            "time_and_counter_collector", sortie_id
        )
        assert res == mock_get_area


def test_get_area_for_sortie_fails_on_exception(
    patch_logger,
    mock_redis_sorties,
    patch_getArea,
    sortie_id,
    coordinates,
    error_message,
    exception,
    exception_with_error_instance,
):
    with exception as exc, patch_getArea as getArea, patch_logger as logger_error:
        mock_redis_sorties.delete_folder.side_effect = exception_with_error_instance
        get_area_for_sortie(sortie_id, mock_redis_sorties)
        getArea.assert_called_once_with(coordinates)
        mock_redis_sorties.get_folder_content.assert_called_once_with(sortie_id)
        assert str(exc.value) == error_message
        mock_redis_sorties.delete_folder.assert_called_once_with(sortie_id)
        logger_error.error.assert_called()
        assert not mock_redis_sorties.remove_obj_from_folder.calle
