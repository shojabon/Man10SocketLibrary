import time
from random import Random
from threading import Thread

from Man10Socket.data_class.Player import Player
from Man10Socket.utils.gui_manager.GUI import GUI
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent


class TestInv(GUI):

    def __init__(self, material: str):
        super().__init__(6)
        self.material = material
        self.icon_item = Item().set_material(material).set_display_name(material).set_amount(1)

        random_slot = Random().randint(0, 53)

        self.set_title(str(random_slot))

        @self.icon(slots=[random_slot], item=Item(material="DIAMOND_BLOCK"))
        def test(event: GUIClickEvent):
            if event.click_type != "DOUBLE_CLICK":
                return
            nextt = TestInv("DIAMOND_BLOCK")
            self.gui_handler.open_gui(event.player, nextt)
