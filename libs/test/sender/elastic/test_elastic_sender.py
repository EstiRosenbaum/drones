from sender.elastic.elastic_sender import ElasticSender

from conftest import mock_calls


def test_create_connection_success(mock_elastic, mock_env):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    with mock_env:
        sender = ElasticSender.create_connection()

        assert isinstance(sender, ElasticSender)
        assert sender.elastic_search == mock_elasticsearch_instance
        assert sender.is_connected is True


def test_create_connection_failure(mock_elastic, mock_env):
    mock_calls(mock_elastic, ping=False)
    with mock_env:
        sender = ElasticSender.create_connection()
        assert sender.is_connected is False


def test_create_message_success(mock_elastic, message):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    document = message.get("message")
    index = message.get("index")
    sender = ElasticSender(mock_elasticsearch_instance)
    sender._create_message(document, index)

    mock_elasticsearch_instance.index.assert_called_once_with(
        index=index, document=document
    )


def test_update_message_success(mock_elastic, message, doc_ID):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    document = message.get("message")
    index = message.get("index")
    sender = ElasticSender(mock_elasticsearch_instance)
    sender._update_message(document, index, doc_ID)

    mock_elasticsearch_instance.update.assert_called_once_with(
        index=index, id=doc_ID, body={"doc": document}
    )


def test_send_message_by_type_create(
    mock_elastic,
    patch_create_message,
    patch_get_docID,
    message,
    type_created,
    type="create",
):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    document = message.get("message")
    index = message.get("index")
    with patch_create_message as send, patch_get_docID as get_docID:
        sender = ElasticSender(mock_elasticsearch_instance)
        result = sender._send_message_by_type(message, type)
        send.assert_called_once_with(document, index)
        get_docID.assert_not_called()
        assert result == type_created


def test_send_message_by_type_update(
    mock_elastic,
    patch_update_message,
    patch_get_docID,
    doc_ID,
    message_update,
    type_updated,
    type="update",
):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    document = message_update.get("message")
    index = message_update.get("index")
    identifiers = message_update.get("identifiers")
    with patch_update_message as send, patch_get_docID as get_docID:
        sender = ElasticSender(mock_elasticsearch_instance)

        result = sender._send_message_by_type(message_update, type)
        send.assert_called_once_with(document, index, doc_ID)
        get_docID.assert_called_once_with(identifiers, index)
        assert result == type_updated


def test_send_message_success(mock_elastic, message, patch_send_message_by_type):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    with patch_send_message_by_type as send:
        sender = ElasticSender(mock_elasticsearch_instance)
        sender.send_message(message)

        send.assert_called_once_with(message, "create")


def test_send_message_not_connected(exception, mock_elastic, message, patch_logger):
    mock_elasticsearch_instance = mock_elastic.return_value
    sender = ElasticSender(mock_elasticsearch_instance)
    sender.is_connected = False

    with exception, patch_logger as logger:
        sender.send_message(message)
        logger.error.assert_called()


def test_get_docID_success(mock_elastic, message_update, doc_ID):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    identifiers = message_update.get("identifiers")
    index = message_update.get("index")
    sender = ElasticSender(mock_elasticsearch_instance)
    result = sender.get_docID(identifiers, index)
    mock_elasticsearch_instance.search.assert_called_once_with(
        index=index, body={"query": {"bool": {"must": [{"term": identifiers}]}}}
    )
    assert result == doc_ID


def test_get_docID_is_None(mock_elastic, message_update):
    mock_elasticsearch_instance = mock_calls(mock_elastic, ping=True)
    identifiers = message_update.get("identifiers")
    index = message_update.get("index")
    sender = ElasticSender(mock_elasticsearch_instance)
    mock_elasticsearch_instance.search.return_value = {
        "hits": {
            "total": {"value": -1},
        }
    }
    result = sender.get_docID(identifiers, index)
    mock_elasticsearch_instance.search.assert_called_once_with(
        index=index, body={"query": {"bool": {"must": [{"term": identifiers}]}}}
    )
    assert result is None


def test_check_connection(mock_elasticsearch):
    sender = ElasticSender(mock_elasticsearch)
    assert sender.is_connected is True


def test_check_connection_failure(mock_elasticsearch):
    mock_elasticsearch.ping.return_value = False
    sender = ElasticSender(mock_elasticsearch)
    assert sender.is_connected is False
