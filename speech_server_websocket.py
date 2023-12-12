from multiprocessing import freeze_support

from handlers.gift_handler import GifHandler
from tiktok_chatbot import tiktok_chatbot
import socket
import json
import threading


class TCPServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 12345):
        self.host = host
        self.port = port
        self.chat = tiktok_chatbot()
        self.server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gift_handler = GifHandler()

    def gift_received(self, json_data: dict):
        self.gift_handler.add_gift(
            json_data["gift_name"],
            json_data["gift_type"],
            json_data["gift_price"],
            json_data["gift_quantity"],
            json_data["tiktok_user"],
        )

    def chat_received(self, json_data: dict):
        thread = threading.Thread(
            target=self.handle_chatbot_response,
            args=(json_data["data"], json_data["tiktok_user"]),
        )
        thread.start()

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Servidor escuchando en {self.host}:{self.port}")

            while not self.shutdown_requested():
                client_socket, addr = self.server_socket.accept()
                print(f"Conexión establecida desde {addr}")
                data = client_socket.recv(1024).decode("utf-8")
                if data:
                    print(f"Datos recibidos del cliente: {data}")
                    json_data = json.loads(data)
                    print(f"Datos recibidos del cliente: {json_data}")

                    if json_data["type"] == "chat":
                        self.chat_received(json_data)

                    if json_data["type"] == "gift":
                        self.gift_received(json_data)

                    if json_data["type"] == "simple_conversation":
                        thread = threading.Thread(
                            target=self.chat.generar_charla_aleatoria,
                            args=(json_data["data"],),
                        )
                        thread.start()

                    print("onplay false")

            self.server_socket.close()

        except KeyboardInterrupt:
            print("Señal de interrupción recibida. Cerrando el servidor...")
            self.server_socket.close()

    def handle_chatbot_response(self, data, user):
        # Llama a chatbot_response en el hilo
        self.chat.chatbot_response(data, user)

    def shutdown_requested(self):
        # Implementa lógica para determinar si se ha solicitado el cierre del servidor
        # Por ejemplo, verifica una variable de bandera, evento, señal, etc.
        return False  # Cambia esto según tu lógica de cierre


def main():
    try:
        server = TCPServer()
        server.start()
    except KeyboardInterrupt:
        print("Señal de interrupción recibida. Cerrando el servidor...")
        server.server_socket.close()
        server.gift_handler.stop()


if __name__ == "__main__":
    freeze_support()
    main()
