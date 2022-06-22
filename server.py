import socket
import threading
from modules.pyrsa import create_key, decrypt_message, encrypt_message


# You can choose your own port 
HOST = '127.0.0.1'
PORT = 9090

# Generating server RSA keypair
keypair = create_key()
server_public_key = keypair[0]
server_private_key = keypair[1]


# starting PYCHAT server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()


# A list with all active connections
users = []

# Sessoin object
class Session:
    def __init__(self, user_id, client, username, public_key):
        self.user_id = user_id
        self.client = client
        self.username = username
        self.public_key = public_key




#Send message to all clients

def broadcast(message):
    # Decrypts messages encrypted with the server's public key comming from clients
    decrypted_message = decrypt_message(server_private_key, message)
    print(decrypted_message)

    # Encrypts messages using client public key and send it to all active clients 
    for user_session in users:
        encrypted_message = encrypt_message(user_session.public_key, decrypted_message)
        try:
            user_session.client.send(encrypted_message.encode("utf-8"))
        except:
            break


# Actively checking for an incomming massage and handling close connections

def handle(user_session):
    while True:
        try:
            message = user_session.client.recv(1024).decode('utf-8')
            print(user_session.client)
            broadcast(message)
        except:
            print(f"{user_session.username} disconected")
            broadcast(encrypt_message(server_public_key,f"{user_session.username} disconected\n"))
            users.remove(user_session)
            user_session.client.close()
            break


# Protocol for handeling incomming new connections
def receive():
    while True:
        client,address = server.accept()
        print(f"connected with {str(address)}")


        client.send("NCK".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        # Exchanging public key's
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

        # Broadcast a new connection
        broadcast(encrypt_message(server_public_key,f"{username} connected to the server\n"))
        welcome_message = encrypt_message(public_key, "You are connected to the server\n")
        client.send(welcome_message.encode("utf-8"))

        # Creating a new thread for every active client to handle communication
        thread = threading.Thread(target=handle, args=(user_session,))
        thread.start()

print("Started server...")
receive()