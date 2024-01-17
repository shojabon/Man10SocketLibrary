import typing


class Item:

    def __init__(self):
        self.__material = None
        self.__display_name = None
        self.__lore = None
        self.__amount = None
        self.__custom_model_data = None
        self.__type_base64 = None

    def set_material(self, material: str) -> 'Item':
        self.__material = material
        return self

    def set_display_name(self, display_name: str) -> 'Item':
        self.__display_name = display_name
        return self

    def set_lore(self, lore: list[str]) -> 'Item':
        self.__lore = lore
        return self

    def set_amount(self, amount: int) -> 'Item':
        self.__amount = amount
        return self

    def set_custom_model_data(self, custom_model_data: int) -> 'Item':
        self.__custom_model_data = custom_model_data
        return self

    def set_type_base64(self, type_base64: str) -> 'Item':
        self.__type_base64 = type_base64
        return self

    def get_json(self):
        result = {
            "material": self.__material,
            "displayName": self.__display_name,
            "lore": self.__lore,
            "amount": self.__amount,
            "customModelData": self.__custom_model_data,
            "typeBase64": self.__type_base64
        }
        # delete all None
        return {k: v for k, v in result.items() if v is not None}

