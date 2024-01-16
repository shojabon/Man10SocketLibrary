import time

from Man10Socket import Man10Socket

if __name__ == '__main__':
    man10_socket = Man10Socket("Man10Shop", "localhost", 5000)
    res = man10_socket.connection_handler.get_socket("Man10Socket").send_message({"server": "main", "type": "sCommand", "command": "mshop moneyGive ffa9b4cb-ada1-4597-ad24-10e318f994c8 1"}, reply=True)
    print(res)
    def route1(message: dict):
        return "success", {"test": "b", "id": 2}

    man10_socket.custom_request.register_route("test/a/d", route1)

    time.sleep(1000000)