from __future__ import annotations

import typing
from threading import Thread
from typing import Callable, TYPE_CHECKING

from Man10Socket.data_class.Player import Player
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent
from Man10Socket.data_class.Item import (Item)

if TYPE_CHECKING:
    from Man10Socket.utils.gui_manager.GUIHandler import GUIHandler


class GUI:

    def __init__(self, rows: int):
        self.__items: dict[int, Item] = {}
        self.__on_click_callable: dict[int, Callable[[GUIClickEvent, typing.ParamSpecKwargs], None]] = {}
        self.__on_click_kwargs: dict[int, dict] = {}
        self.__slot_updated: list[int] = []
        self.__title = None
        self.__rows = rows
        self.session_id = None
        self.gui_handler: GUIHandler | None = None
        self.target: str | None = None

        self.__managed_threads: list[Thread] = []

        self.__global_air_item = Item().set_material("AIR")

    def set_title(self, title: str):
        self.__title = title

    def set_item(self, item: Item, slots: list[int], callback: Callable[[GUIClickEvent], None] = None,
                 push: bool = True, callback_kwargs: dict = None):
        for slot in slots:
            self.__items[slot] = item
            if callback is not None:
                self.__on_click_callable[slot] = callback
                self.__on_click_kwargs[slot] = callback_kwargs if callback_kwargs is not None else {}

            if slot not in self.__slot_updated:
                self.__slot_updated.append(slot)

        if push:
            self.push()

    def unset_item(self, slots: list[int], push: bool = True):
        for slot in slots:
            self.set_item(self.__global_air_item, [slot], push=push)

    def push(self):
        if self.session_id is not None:
            result = self.gui_handler.update_gui(self.target, self)
            if result:
                self.__slot_updated = []

    def clear(self, push: bool = True):
        self.unset_item([x for x in range(self.__rows * 9)], push=push)

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

    def get_json(self, updated_only=False):
        items_slots: dict[Item, list[int]] = {}
        clear_slots: list[int] = []
        if not updated_only:
            for slot, item in self.__items.items():
                if item not in items_slots:
                    items_slots[item] = []
                items_slots[item].append(slot)
        else:
            for slot in self.__slot_updated:
                if slot in self.__items:
                    item = self.__items[slot]
                    if item not in items_slots:
                        items_slots[item] = []
                    items_slots[item].append(slot)
                else:
                    clear_slots.append(slot)

        schema = []
        for item, slots in items_slots.items():
            if item.get_json() is not None:
                schema.append({
                    "item": item.get_json(),
                    "slots": slots
                })

        if len(clear_slots) > 0:
            schema.append({
                "item": None,
                "slots": clear_slots
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

    def icon(self, slots: list[int], item: Item):
        def decorator(func: Callable[[GUIClickEvent], None]):
            self.set_item(item, slots, func, push=False)
            return func

        return decorator

