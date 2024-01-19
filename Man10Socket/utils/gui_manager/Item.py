import hashlib
import json
import typing


class Item:

    def __init__(self, material: str = None, display_name: str = None, lore: list[str] = None, amount: int = None, custom_model_data: int = None, type_base64: str = None, type_md5: str = None):
        self.__material = material
        self.__display_name = display_name
        self.__lore = lore
        self.__amount = amount
        self.__custom_model_data = custom_model_data
        self.__type_base64 = type_base64
        self.__type_md5 = type_md5

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

    def set_type_md5(self, type_md5: str) -> 'Item':
        self.__type_md5 = type_md5
        return self

    def get_json(self):
        result = {
            "material": self.__material,
            "displayName": self.__display_name,
            "lore": self.__lore,
            "amount": self.__amount,
            "customModelData": self.__custom_model_data,
            "typeBase64": self.__type_base64,
            "typeMd5": self.__type_md5
        }
        # delete all None
        return {k: v for k, v in result.items() if v is not None}

    def get_md5(self):
        if self.__type_md5 is not None:
            return self.__type_md5
        else:
            return hashlib.md5(json.dumps(self.get_json(), ensure_ascii=False).encode("utf-8")).hexdigest()

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.get_md5() == other.get_md5()
        else:
            return False

    def __hash__(self):
        return hash(self.get_md5())

