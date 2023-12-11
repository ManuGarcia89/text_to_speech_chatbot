from tiktok_chatbot import tiktok_chatbot
import socket
import json
import threading

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.chat = tiktok_chatbot()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")

        while not self.shutdown_requested():
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión establecida desde {addr}")
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Datos recibidos del cliente: {data}")
                json_data = json.loads(data)
                if json_data["type"] == "chat":
                    thread = threading.Thread(target=self.handle_chatbot_response, args=(json_data["data"], json_data["tiktok_user"]))
                    thread.start()
                    #client_socket.close()

                if json_data["type"] == "gift":
                    thread = threading.Thread(target=self.chat.recibir_regalo_y_dar_feednback, args=(json_data["gift_name"], json_data["gift_type"], json_data["gift_price"], json_data["gift_quantity"], json_data["tiktok_user"],))
                    thread.start()
                
                if json_data["type"] == "simple_conversation":
                    thread = threading.Thread(target=self.chat.generar_charla_aleatoria, args=(json_data["data"],))
                    thread.start()
                
                if json_data["type"] == "new_audio":
                    thread = threading.Thread(target=self.chat.crear_audio_temporal_con_texto, args=(json_data["data"],))
                    thread.start()
                
                print("onplay false")
                self.wait_for_finish_to_speak(client_socket=client_socket)
           
        self.server_socket.close()
    
    def wait_for_finish_to_speak(self, client_socket):
        while self.chat.on_play == False:
            pass
        response = {"on_play": True}
        response_json = json.dumps(response)
        client_socket.send(response_json.encode('utf-8'))
        print("onplay true")
        while self.chat.on_play == True:
            pass
        print("onplay false") 
        response = {"on_play": False}
        response_json = json.dumps(response)
        client_socket.send(response_json.encode('utf-8'))


    def handle_chatbot_response(self, data, user):
        # Llama a chatbot_response en el hilo
        self.chat.chatbot_response(data, user)

    def shutdown_requested(self):
        # Implementa lógica para determinar si se ha solicitado el cierre del servidor
        # Por ejemplo, verifica una variable de bandera, evento, señal, etc.
        return False  # Cambia esto según tu lógica de cierre

# Uso del servidor
host = '127.0.0.1'
port = 12345

server = TCPServer(host, port)
server.start()