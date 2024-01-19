from __future__ import annotations

import traceback
import uuid
from typing import TYPE_CHECKING, Callable

from expiring_dict import ExpiringDict

from Man10Socket.data_class.Player import Player

if TYPE_CHECKING:
    from Man10Socket import Man10Socket


class CommandEvent:

    def __init__(self, player: Player, command: str):
        self.__player: Player = player
        self.__command: str = command

    def get_player(self) -> Player:
        return self.__player

    def get_command(self) -> str:
        return self.__command

    def get_base_command(self) -> str:
        return self.__command.split(" ")[0]

    def get_args(self) -> list[str]:
        return self.__command.split(" ")[1:]