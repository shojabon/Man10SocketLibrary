from __future__ import annotations

import traceback
import uuid
from typing import TYPE_CHECKING, Callable

from expiring_dict import ExpiringDict

from Man10Socket.utils.gui_manager.GUI import GUI
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent

if TYPE_CHECKING:
    from Man10Socket.data_class.Player import Player
    from Man10Socket import Man10Socket
    from Man10Socket.utils.connection_handler.Connection import Connection


class GUIHandler:

    def __init__(self, main: Man10Socket):
        self.main = main
        self.__active_sessions = ExpiringDict(60*10)

        @self.main.event_handler.listener("gui_click")
        def on_gui_click(connection: Connection, data: dict):
            data = data.get("data", None)
            if data is None:
                return
            session_id = data.get("id", None)
            session = self.get_session(session_id)

            event = GUIClickEvent()
            event.player = self.main.get_player(data.get("player", None))
            event.slot = data.get("rawSlot", None)
            event.action = data.get("action", None)
            event.click_type = data.get("clickType", None)
            if session is None:
                return
            try:
                session.internal_on_click(event)
            except Exception as e:
                traceback.print_exc()

            try:
                session.on_click(event)
            except Exception as e:
                traceback.print_exc()

        @self.main.event_handler.listener("gui_close")
        def on_gui_close(connection: Connection, data: dict):
            data = data.get("data", None)
            if data is None:
                return
            session_id = data.get("id", None)
            player = self.main.get_player(data.get("player", None))
            session = self.get_session(session_id)
            if session is None:
                return
            try:
                session.on_close(player)
            except Exception as e:
                traceback.print_exc()

    def open_gui(self, player: Player, gui: GUI):
        session_id = str(uuid.uuid4())
        gui.session_id = session_id
        gui.gui_handler = self
        gui.target = player.get_uuid() # change to server name
        self.__active_sessions[session_id] = gui
        a = self.main.connection_handler.get_socket("Man10Socket").send_message({
            "target": player.get_uuid(),
            "player": player.get_uuid(),
            "type": "gui_open",
            "id": session_id,
            **self.get_session(session_id).get_json()
        }, reply=True)
        return a

    def update_gui(self, target: str, gui: GUI):
        if target is None:
            return False
        if gui.session_id not in self.__active_sessions:
            return False
        test = gui.get_json(updated_only=True)
        a = self.main.connection_handler.get_socket("Man10Socket").send_message({
            "type": "gui_update",
            "target": target,
            "id": gui.session_id,
            **test
        }, reply=True)
        if a is None:
            return False
        if a.get("status", None) == "error_invalid_args_id":
            if gui.session_id in self.__active_sessions:
                del self.__active_sessions[gui.session_id]
            return False
        return a.get("status", None) == "success"

    def get_session(self, session_id: str) -> GUI:
        return self.__active_sessions.get(session_id, None)
