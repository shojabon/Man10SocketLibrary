import time
from random import Random
from threading import Thread

from Man10Socket.data_class.Player import Player
from Man10Socket.utils.gui_manager.GUI import GUI
from Man10Socket.utils.gui_manager.GUIClickEvent import GUIClickEvent
from Man10Socket.utils.gui_manager.Item import Item


class TestInv(GUI):

    def __init__(self, material: str):
        super().__init__("テストインベントリ", 6)
        self.material = material
        self.icon = Item().set_material(material).set_display_name(material).set_amount(1)

        self.materials = [
            "WHITE_STAINED_GLASS_PANE",
            "ORANGE_STAINED_GLASS_PANE",
            "MAGENTA_STAINED_GLASS_PANE",
            "LIGHT_BLUE_STAINED_GLASS_PANE",
            "YELLOW_STAINED_GLASS_PANE",
            "LIME_STAINED_GLASS_PANE",
            "PINK_STAINED_GLASS_PANE",
            "GRAY_STAINED_GLASS_PANE",
            "LIGHT_GRAY_STAINED_GLASS_PANE",
            "CYAN_STAINED_GLASS_PANE",
            "PURPLE_STAINED_GLASS_PANE",
            "BLUE_STAINED_GLASS_PANE",
            "BROWN_STAINED_GLASS_PANE",
            "GREEN_STAINED_GLASS_PANE",
            "RED_STAINED_GLASS_PANE",
            "BLACK_STAINED_GLASS_PANE"
        ]

        def render_task():
            start_time = time.time()
            for _ in range(2):
                self.clear(push=False)
                for x in range(54):
                    # select random material
                    random_material = self.materials[Random().randint(0, len(self.materials) - 1)]

                    def on_click(event: GUIClickEvent, clicked_material=None):
                        print("clicked_material:", clicked_material)

                    self.set_item(Item().set_material(random_material).set_display_name(random_material).set_amount(1),
                                  [x], push=False, callback=on_click, callback_kwargs={"clicked_material": random_material})
                self.push()
                time.sleep(0.01)
            elapsed_time = time.time() - start_time
            predicted_time = 0.01 * 1000
            print(f"elapsed_time:{elapsed_time}[sec]")
            print(f"predicted_time:{predicted_time}[sec]")
            print(f"diff:{elapsed_time - predicted_time}[sec]")

        Thread(target=render_task, daemon=True).start()

        # def click(event: GUIClickEvent):
        #     for slot in self.route:
        #         self.clear(push=False)
        #         self.set_item(Item().set_material(material).set_display_name(material).set_amount(1), [slot],
        #                       callback=click, push=True)
        #         time.sleep(0.01)
        #
        # self.set_item(Item().set_material(material).set_display_name(material).set_amount(1), [0], callback=click)

    def on_click(self, event: GUIClickEvent):
        print(event.slot, event.action, event.click_type)

    def on_close(self, player: Player):
        print("x")
