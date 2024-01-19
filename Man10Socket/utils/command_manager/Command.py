from __future__ import annotations

import traceback
import uuid
from typing import TYPE_CHECKING, Callable

from expiring_dict import ExpiringDict

if TYPE_CHECKING:
    from Man10Socket import Man10Socket


class Command:

    def __init__(self, command_name: str):
        self.command_name = command_name
        self.__args = []
        self.required_permission = None
        self.explanation = None

    def get_command_name(self):
        return self.command_name

    def prefix(self, prefix: str) -> "Command":
        self.__args.append(prefix)
        return self

    def args(self, args: list[str]) -> "Command":
        self.__args.append(args)
        return self

    def required_permission(self, required_permission: str) -> "Command":
        self.required_permission = required_permission
        return self

    def get_schema(self):
        result = {
            "schema": self.__args,
        }
        if self.required_permission is not None:
            result["required_permission"] = self.required_permission
        if self.explanation is not None:
            result["explanation"] = self.explanation
        return result

    def is_viable_option(self, command: str) -> bool:
        command_base = command.split(" ")[0][1:]
        command_args = command.split(" ")[1:]
        if command_base != self.command_name:
            return False
        if len(command_args) != len(self.__args):
            return False
        for i in range(len(command_args)):
            comparing = self.__args[i]
            if isinstance(comparing, list):
                continue

            if comparing != command_args[i]:
                return False

        return True