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
            "BLACK_STAINED_GLASS_PANE",
            "AIR"
        ]

        self.materials: list[Item] = [Item().set_material(x) for x in self.materials]

        def render_task():
            start_time = time.time()
            for _ in range(10):
                self.clear(push=False)
                for x in range(54):
                    # select random material
                    random_material = self.materials[Random().randint(0, len(self.materials) - 1)]

                    if random_material == "AIR":
                        self.unset_item([x], push=False)
                        continue

                    def on_click(event: GUIClickEvent, clicked_material: Item=None):
                        print("clicked_material:", clicked_material.get_json())

                    self.set_item(random_material.set_amount(1),
                                  [x], push=False, callback=on_click, callback_kwargs={"clicked_material": random_material})
                self.push()
                time.sleep(0.01)

            elpased_time = time.time() - start_time
            predicted_time = 1000 * 0.01
            print("elapsed_time:{0}".format(elpased_time) + "[sec]")
            print("predicted_time:{0}".format(predicted_time) + "[sec]")
            print("diff:{0}".format(elpased_time - predicted_time) + "[sec]")




        Thread(target=render_task, daemon=True).start()

        self.route = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        def click(event: GUIClickEvent):
            for slot in self.route:
                self.clear(push=False)
                self.set_item(Item().set_material(material).set_display_name(material).set_amount(1), [slot],
                              callback=click, push=True)
                time.sleep(0.1)

        self.set_item(Item().set_material(material).set_display_name(material).set_amount(1), [0], callback=click)

    def on_click(self, event: GUIClickEvent):
        print(event.slot, event.action, event.click_type)

    def on_close(self, player: Player):
        print("x")
