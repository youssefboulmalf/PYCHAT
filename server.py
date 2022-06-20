import socket
import threading
from pyrsa.pyrsa import create_key, decrypt_message, encrypt_message

HOST = '127.0.0.1'
PORT = 9090


keypair = create_key()
server_public_key = keypair[0]
server_private_key = keypair[1]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))


server.listen()


users = []


class Session:
    def __init__(self, user_id, client, username, public_key):
        self.user_id = user_id
        self.client = client
        self.username = username
        self.public_key = public_key

def broadcast(message):
    decrypted_message = decrypt_message(server_private_key, message)
    print(decrypted_message)
    for user_session in users:
        encrypted_message = encrypt_message(user_session.public_key, decrypted_message)
        user_session.client.send(encrypted_message.encode("utf-8"))


def handle(user_session):
    while True:
        try:
            username = user_session.username
            message = user_session.client.recv(1024).decode('utf-8')
            broadcast(message)
        except:
            print(f"{user_session.username} disconected")
            broadcast(encrypt_message(server_public_key,f"{user_session.username} disconected\n"))
            users.remove(user_session)
            user_session.client.close()
            break

def receive():
    while True:
        client,address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NCK".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')


        client.send("PBK1".encode("utf-8"))
        pbk1 = client.recv(1024).decode('utf-8')
        print(pbk1)

        client.send("PBK2".encode("utf-8"))
        pbk2 = client.recv(1024)

        svk1 = f"SVK1:{str(server_public_key[0])}"
        svk2 = f"SVK2:{str(server_public_key[1])}"
        print(svk1, svk2)

        client.send(svk1.encode("utf-8"))
        client.recv(1024)

        client.send(svk2.encode("utf-8"))
        client.recv(1024)

        public_key=[int(pbk1),int(pbk2)]

        user_id = len(users) + 1
        user_session = Session(user_id, client, username, public_key)
        users.append(user_session)

        print(f"Username of client is {username}")
        broadcast(encrypt_message(server_public_key,f"{username} connected to the server\n"))
        welcome_message = encrypt_message(public_key, "You are connected to the server\n")
        client.send(welcome_message.encode("utf-8"))

        thread = threading.Thread(target=handle, args=(user_session,))
        thread.start()

print("Started server...")
receive()