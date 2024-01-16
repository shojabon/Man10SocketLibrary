from __future__ import annotations

import socket
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Man10Socket.utils.connection_handler.ConnectionHandler import ConnectionHandler
    from Man10Socket.utils.connection_handler.Connection import Connection


class ConnectionFunction:

    def information(self):
        pass

    def __init__(self):
        self.name: str = ""
        self.function_type: str = ""
        self.mode: list[str] = []
        self.information()
        self.main: ConnectionHandler|None = None

    def handle_message(self, connection: Connection, json_message: dict):
        pass
