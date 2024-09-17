import os
from typing import Any, Self

from elasticsearch import Elasticsearch
from helpers.logger.w_logger import logger
from helpers.utils.const import State
from sender.sender import Sender


class ElasticSender(Sender):
    def __init__(self, elastic_search: Elasticsearch) -> None:
        self.elastic_search = elastic_search
        self.is_connected = self._check_connection()

    @classmethod
    def create_connection(cls: Self, connection: Any | None = None) -> Self:
        if connection is None:
            connection = {}
        return cls(
            elastic_search=Elasticsearch(
                cloud_id=connection.get("cloud_id", os.environ["CLOUD_ID"]),
                basic_auth=(
                    connection.get("name", os.environ["NAME"]),
                    connection.get("password", os.environ["PASSWORD"]),
                ),
            )
        )

    def send_message(self, message: object) -> None:
        if self.is_connected is False:
            logger.critical("Elasticsearch is not connected")
        type = message.get("type")
        result = self._send_message_by_type(message, type)
        if result != State[type.upper()]:
            logger.info(f"message was not sent. res = {result}.")

    def _send_message_by_type(self, message: object, type: str) -> str:
        index = message.get("index")
        document = message.get("message")
        identifiers = message.get("identifiers")

        doc_id = self.get_docID(identifiers, index) if type == "update" else None
        res = (
            self._create_message(document, index)
            if doc_id is None
            else self._update_message(document, index, doc_id)
        )
        return res["result"]

    def _create_message(self, document: object, index: str) -> object:
        return self.elastic_search.index(index=index, document=document)

    def _update_message(self, document: object, index: str, doc_id: str) -> object:
        return self.elastic_search.update(
            index=index,
            id=doc_id,
            body={"doc": document},
        )

    def get_docID(self, identifiers: object, index: str) -> str | None:
        must_queries = [{"term": {key: value}} for key, value in identifiers.items()]
        search_res = self.elastic_search.search(
            index=index, body={"query": {"bool": {"must": must_queries}}}
        )
        return (
            search_res["hits"]["hits"][0]["_id"]
            if search_res["hits"]["total"]["value"] > 0
            else None
        )

    def _check_connection(self) -> bool:
        return self.elastic_search.ping()
