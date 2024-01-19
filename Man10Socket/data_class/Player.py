from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Man10Socket import Man10Socket
    from Man10Socket.utils.gui_manager.GUI import GUI


class Player:

    def __init__(self, player_uuid: str, main: Man10Socket):
        self.__uuid = player_uuid
        self.__main: Man10Socket = main
        self.current_gui: str|None = None

    def get_uuid(self) -> str:
        return self.__uuid

    def open_gui(self, gui: GUI):
        self.__main.gui_handler.open_gui(self, gui)

    def send_message(self, message: str, send_async: bool = False):
        return self.__main.connection_handler.get_socket("Man10Socket").send_message({
            "type": "player_tell",
            "target": self.__uuid,
            "player": self.__uuid,
            "message": message
        }, reply=not send_async)