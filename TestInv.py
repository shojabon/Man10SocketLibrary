from Man10Socket.data_class.Player import Player
from Man10Socket.utils.gui_manager.GUI import GUI
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent
from Man10Socket.utils.gui_manager.Item import Item


class TestInv(GUI):

    def __init__(self, material: str):
        super().__init__("テストインベントリ", 6)
        self.material = material

        def click_diamond(event: GUIClickEvent):
            if self.material == "DIAMOND":
                return
            next_inv = TestInv("DIAMOND")
            event.player.open_gui(next_inv)

        [self.set_item(Item().set_material(material).set_display_name(material).set_amount(x+1), [x], callback=click_diamond) for x in range(54)]

    def on_click(self, event: GUIClickEvent):
        print(event.slot, event.action, event.click_type)

    def on_close(self, player: Player):
        if self.material == "CHEST":
            return
        next_inv = TestInv("CHEST")
        player.open_gui(next_inv)
