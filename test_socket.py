import socket
import json

host = "127.0.0.1"
port = 12345

# Crear un socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect((host, port))
print(f"Conectado al servidor en {host}:{port}")

# Enviar un mensaje al servidor

mensaje = {
    "type": "gift",
    "gift_name": "taco",
    "gift_type": 1,
    "gift_price": 1,
    "gift_quantity": 20,
    "tiktok_user": "blacknoise89",
}

mensaje_json = json.dumps(mensaje)

client_socket.send(mensaje_json.encode("utf-8"))

# Recibir la respuesta del servidor
# respuesta = client_socket.recv(1024).decode("utf-8")
# print(f"Respuesta del servidor: {respuesta}")


# Cerrar la conexión con el servidor
client_socket.close()
print("Conexión cerrada.")
