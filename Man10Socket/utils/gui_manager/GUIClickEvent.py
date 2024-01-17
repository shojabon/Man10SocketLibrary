from typing import Optional

from Man10Socket.data_class.Player import Player


class GUIClickEvent:

    def __init__(self):
        self.player: Optional[Player] = None
        self.slot: Optional[int] = None
        self.action: Optional[str] = None
        self.click_type: Optional[str] = None