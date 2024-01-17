from __future__ import annotations

from typing import Callable

from Man10Socket.data_class.Player import Player
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent
from Man10Socket.utils.gui_manager.Item import Item


class GUI:

    def __init__(self, title: str, rows: int):
        self.__items: dict[int, Item] = {}
        self.__on_click_callable: dict[int, Callable[[GUIClickEvent], None]] = {}
        self.__title = title
        self.__size = rows * 9
        self.session_id = None

    def set_item(self, item: Item, slots: list[int], callback: Callable[[GUIClickEvent], None] = None):
        for slot in slots:
            self.__items[slot] = item
            if callback is not None:
                self.__on_click_callable[slot] = callback

    def fill(self, item: Item, callback: Callable[[GUIClickEvent], None] = None):
        for i in range(self.__size):
            self.__items[i] = item
            if callback is not None:
                self.__on_click_callable[i] = callback

    def on_click(self, event: GUIClickEvent):
        pass

    def on_close(self, player: Player):
        pass

    def internal_on_click(self, event: GUIClickEvent):
        if event.slot in self.__on_click_callable:
            self.__on_click_callable[event.slot](event)

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
            "size": self.__size/9,
            "schema": schema
        }