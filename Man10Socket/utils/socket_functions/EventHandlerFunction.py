from __future__ import annotations

import socket
import traceback
from typing import TYPE_CHECKING, Callable

from Man10Socket.utils.connection_handler.ConnectionFunction import ConnectionFunction

if TYPE_CHECKING:
    from Man10Socket.utils.connection_handler.ConnectionHandler import ConnectionHandler
    from Man10Socket.utils.connection_handler.Connection import Connection


class EventHandlerFunction(ConnectionFunction):
    listeners: dict[str, list[Callable[[Connection, dict], None]]] = {}
    listening_event_types: list[str] = []

    def __init__(self, main: ConnectionHandler):
        super().__init__()
        self.main = main

    def information(self):
        self.name = "Event Handler Function"
        self.function_type = "event"
        self.mode = ["server"]

    def handle_message(self, connection: Connection, json_message: dict):
        event_type = json_message.get("event")
        json_message["server"] = connection.name
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    listener(connection, json_message)
                except Exception as e:
                    traceback.print_exc()

    def subscribe_to_server(self):
        response = self.main.get_socket("Man10Socket").send_message({"type": "event_subscribe", "event_types": self.listening_event_types}, reply=True)
        if response is None or response["status"] != "success":
            self.main.get_socket("Man10Socket").socket_close()

    def listener(self, event_type: str):
        if event_type not in self.listening_event_types:
            self.listening_event_types.append(event_type)
            self.subscribe_to_server()

        def decorator(func: Callable[[Connection, dict], None]):
            if event_type not in self.listeners:
                self.listeners[event_type] = []
            self.listeners[event_type].append(func)
            return func

        return decorator
