import logging

from listener.rabbitmq.connection import Connection


def test_Connection(
    caplog,
    patch_BlockingConnection,
    patch_ConnectionParameters,
    mock_logger_info,
    mock_connection,
):
    with patch_BlockingConnection as connection, patch_ConnectionParameters as parameters:
        Connection()
        caplog.set_level(logging.INFO)
        parameters.assert_called_once()
        connection.assert_called_once_with(mock_connection)
        assert mock_logger_info in caplog.text


def test_connection_failure(
    caplog, exception, patch_BlockingConnection, mock_logger_error, mock_connection
):
    caplog.set_level(logging.ERROR)
    with exception, patch_BlockingConnection as connection:
        Connection()
        assert connection is None
        assert mock_logger_error in caplog.text
        connection.assert_called_once_with(mock_connection)
