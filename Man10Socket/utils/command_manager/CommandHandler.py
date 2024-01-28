from __future__ import annotations

import traceback
import uuid
from typing import TYPE_CHECKING, Callable

from expiring_dict import ExpiringDict

from Man10Socket.utils.command_manager.Command import Command
from Man10Socket.utils.command_manager.CommandEvent import CommandEvent

if TYPE_CHECKING:
    from Man10Socket import Man10Socket
    from Man10Socket.utils.connection_handler.Connection import Connection


class CommandHandler:

    def __init__(self, main: Man10Socket):
        self.main = main
        self.__registered_commands: dict[Command, Callable[[CommandEvent], None]] = {}

        @self.command(command=Command("testa").prefix("b").args(["command", "test", "x"]))
        def help_command(event: CommandEvent):
            print("executed b command")

        @self.command(command=Command("testa").prefix("a").args(["command", "test", "x"]))
        def test_command(event: CommandEvent):
            event.get_player().send_message("aコマンドを実行しました")

        @self.main.event_handler.listener("player_command_send")
        def on_command(connection: Connection, message: dict):
            data = message.get("data")
            if data is None:
                return
            command_event = CommandEvent(self.main.get_player(data.get("player")), data.get("command"))
            choices = []
            for command in self.__registered_commands:
                if command.is_viable_option(command_event.get_command()):
                    choices.append(command)

            if len(choices) == 0:
                return

            choice = choices[0]
            self.__registered_commands[choice](command_event)

        @self.main.event_handler.listener("server_connected")
        def on_command(connection: Connection, message: dict):
            server = message.get("server")
            if server is None:
                return
            self.main.command_handler.register_all_commands(server)





    def command(self, command: Command):
        def decorator(func: Callable):
            self.__registered_commands[command] = func
            return func

        return decorator

    def register_all_commands(self, target: str):
        registering_commands = {}
        for command in self.__registered_commands:
            if command.get_command_name() not in registering_commands:
                registering_commands[command.get_command_name()] = []

            registering_commands[command.get_command_name()].append(command.get_schema())

        for registering_commands_name in registering_commands:
            schema = {
                "type": "command_register",
                "command": registering_commands_name,
                "schema": registering_commands[registering_commands_name],
                "target": target
            }
            self.main.connection_handler.get_socket(target).send_message(schema)
