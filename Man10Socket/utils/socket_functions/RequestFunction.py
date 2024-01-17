from __future__ import annotations

import socket
from typing import TYPE_CHECKING, Callable, Tuple

from Man10Socket.utils.connection_handler.ConnectionFunction import ConnectionFunction

if TYPE_CHECKING:
    from Man10Socket.utils.connection_handler.Connection import Connection


class RequestFunction(ConnectionFunction):

    def __init__(self):
        super().__init__()
        self.routes: dict[str, Callable[[dict], Tuple]] = {}

    def information(self):
        self.name = "Custom Request Function"
        self.function_type = "request"
        self.mode = ["server"]

    def handle_message(self, connection: Connection, json_message: dict):
        if "path" not in json_message:
            return "invalid_args_path", None
        if "data" not in json_message:
            return "invalid_args_data", None
        json_message["server"] = connection.name
        if json_message["path"] in self.routes:
            result = self.routes[json_message["path"]](json_message)
            return result
    def register_route(self, path: str, callback: Callable[[dict], Tuple]):
        self.routes[path] = callback
