from __future__ import annotations

import typing
from threading import Thread
from typing import Callable, TYPE_CHECKING

from Man10Socket.data_class.Player import Player
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent
from Man10Socket.utils.gui_manager.Item import Item

if TYPE_CHECKING:
    from Man10Socket.utils.gui_manager.GUIHandler import GUIHandler


class GUI:

    def __init__(self, title: str, rows: int):
        self.__items: dict[int, Item] = {}
        self.__on_click_callable: dict[int, Callable[[GUIClickEvent, typing.ParamSpecKwargs], None]] = {}
        self.__on_click_kwargs: dict[int, dict] = {}
        self.__title = title
        self.__rows = rows
        self.session_id = None
        self.gui_handler: GUIHandler | None = None
        self.target: str | None = None

        self.__managed_threads: list[Thread] = []

    def set_item(self, item: Item, slots: list[int], callback: Callable[[GUIClickEvent], None] = None,
                 push: bool = True, callback_kwargs: dict = None):
        for slot in slots:
            self.__items[slot] = item
            if callback is not None:
                self.__on_click_callable[slot] = callback
                self.__on_click_kwargs[slot] = callback_kwargs if callback_kwargs is not None else {}

        if push:
            self.push()

    def push(self):
        if self.session_id is not None:
            self.gui_handler.update_gui(self.target, self)

    def clear(self, push: bool = True):
        self.__items = {}
        self.__on_click_callable = {}
        self.__on_click_kwargs = {}
        if push:
            self.push()

    def fill(self, item: Item, callback: Callable[[GUIClickEvent], None] = None, callback_kwargs: dict = None):
        self.set_item(item, [x for x in range(self.__rows * 9)], callback, push=False, callback_kwargs=callback_kwargs)
        self.push()

    def on_click(self, event: GUIClickEvent):
        pass

    def on_close(self, player: Player):
        pass

    def internal_on_click(self, event: GUIClickEvent):
        if event.slot in self.__on_click_callable:
            self.__on_click_callable[event.slot](event, **self.__on_click_kwargs[event.slot])

    def get_json(self):
        items_slots: dict[Item, list[int]] = {}
        for slot, item in self.__items.items():
            if item not in items_slots:
                items_slots[item] = []
            items_slots[item].append(slot)

        schema = []
        for item, slots in items_slots.items():
            schema.append({
                "item": item.get_json(),
                "slots": slots
            })

        return {
            "title": self.__title,
            "size": self.__rows,
            "schema": schema
        }

    def execute_async(self, func: Callable, *args):
        thread = Thread(target=func, daemon=True, args=args)
        thread.start()
        self.__managed_threads.append(thread)

