from modules.sortie_functions import is_sortie_finished, sortie_already_exists
from utils.const import FoldersInRedis


def test_is_sortie_finished_False(
    sortie_id, mock_redis_sorties, sortie_not_finished_excepted, number_of_images_tagged
):
    mock_redis_sorties.get_obj_from_folder.return_value = sortie_not_finished_excepted
    result = is_sortie_finished(mock_redis_sorties, sortie_id, number_of_images_tagged)

    assert result is False
    mock_redis_sorties.get_obj_from_folder.assert_called_once_with(
        FoldersInRedis.COLLECTOR, sortie_id
    )


def test_is_sortie_finished_True(
    sortie_id, mock_redis_sorties, sortie_finished_excepted, number_of_images_tagged
):
    mock_redis_sorties.get_obj_from_folder.return_value = sortie_finished_excepted
    result = is_sortie_finished(mock_redis_sorties, sortie_id, number_of_images_tagged)

    assert result is True
    mock_redis_sorties.get_obj_from_folder.assert_called_once_with(
        FoldersInRedis.COLLECTOR, sortie_id
    )


def test_sortie_already_exists(mock_redis_sorties, sortie_id):
    mock_redis_sorties.obj_exist.return_value = True
    result = sortie_already_exists(mock_redis_sorties, sortie_id)
    mock_redis_sorties.obj_exist.assert_called_with(
        FoldersInRedis.SORTIES_UPLOADED, sortie_id
    )
    assert result is True


def test_sortie_already_exists_False(mock_redis_sorties, sortie_id):
    mock_redis_sorties.obj_exist.return_value = False
    result = sortie_already_exists(mock_redis_sorties, sortie_id)
    mock_redis_sorties.obj_exist.assert_called_with(
        FoldersInRedis.SORTIES_UPLOADED, sortie_id
    )
    assert result is False
