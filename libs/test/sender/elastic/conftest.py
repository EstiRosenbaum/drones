from unittest.mock import MagicMock, patch

import pytest
from elasticsearch import Elasticsearch


@pytest.fixture
def message(type, message):
    return {**message, "type": type}


@pytest.fixture
def doc_ID():
    return "imageID123"


@pytest.fixture
def message_update(message, doc_ID):
    return {**message, **{"identifiers": {"imageID": doc_ID}}}


@pytest.fixture
def type_created():
    return "created"


@pytest.fixture
def type_updated():
    return "updated"


@pytest.fixture
def current_path():
    return "sender.elastic.elastic_sender"


@pytest.fixture
def path_ElasticSender(current_path):
    return f"{current_path}.ElasticSender"


@pytest.fixture
def patch_ElasticSearch(current_path):
    return patch(f"{current_path}.Elasticsearch")


@pytest.fixture
def patch_create_message(path_ElasticSender, type_created):
    return patch(
        f"{path_ElasticSender}._create_message",
        return_value={"result": type_created},
    )


@pytest.fixture
def patch_update_message(path_ElasticSender, type_updated):
    return patch(
        f"{path_ElasticSender}._update_message",
        return_value={"result": type_updated},
    )


@pytest.fixture
def patch_get_docID(path_ElasticSender, doc_ID):
    return patch(f"{path_ElasticSender}.get_docID", return_value=doc_ID)


@pytest.fixture
def patch_send_message_by_type(path_ElasticSender):
    return patch(f"{path_ElasticSender}._send_message_by_type")


@pytest.fixture
def mock_elasticsearch():
    mock_es = MagicMock(ES=Elasticsearch)
    mock_es.ping.return_value = True
    return mock_es


@pytest.fixture
def mock_elastic(patch_ElasticSearch):
    with patch_ElasticSearch as mock_es:
        mock_elastic_instance = MagicMock()
        mock_es.return_value = mock_elastic_instance
        yield mock_es


def mock_calls(mock_elasticsearch_class, ping):
    mock_elasticsearch_instance = mock_elasticsearch_class.return_value
    mock_elasticsearch_instance.ping.return_value = ping
    mock_elasticsearch_instance.search.return_value = {
        "hits": {
            "total": {"value": 1},
            "hits": [{"_id": "imageID123"}],
        }
    }
    return mock_elasticsearch_instance
