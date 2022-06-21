import socket
import threading
import tkinter
from tkinter import dialog
import tkinter.scrolledtext
from tkinter import simpledialog
from modules.pyrsa import create_key, decrypt_message, encrypt_message
import re


class Client:
    def __init__(self):

        # Generating client keypair
        self.keypair = create_key()
        self.public_key = self.keypair[0]
        self.private_key = self.keypair[1]

        # Requesting Host ip and port to connect to
        root = tkinter.Tk()
        root.title('PYCHAT')
        root.iconbitmap(default='./icon/pychatlogo.ico')
        root.withdraw()
        self.host = ""
        self.port = 0
        while re.match("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.host) is None:
            self.host=simpledialog.askstring("Host", "Please enter the host ip", parent=root)

        while self.port < 1 or self.port > 65535:
            self.port=simpledialog.askinteger("Port", "Please enter the port number", parent=root)

        # Starting websocket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


        #requesting username after succesfull connect
        self.username = simpledialog.askstring("Username", "Please create a username", parent=root)

        self.gui_done = False

        self.running = True

        self.server_public_key = []

        gui_thread = threading.Thread(target=self.gui_loop)
        recive_thread = threading.Thread(target=self.recive)

        gui_thread.start()
        recive_thread.start()


    # The creation of the GUI 
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title('PYCHAT')
        self.win.iconbitmap('./icon/pychatlogo.ico')
        self.win.resizable(False, False)
        self.win.config(bg="darkred")

        self.chat_label = tkinter.Label(self.win, text = "Chat:", bg="darkred")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.message_label = tkinter.Label(self.win, text = "Message:", bg="darkred")
        self.message_label.config(font=("Arial", 12))
        self.message_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text = "Send", command=self.write)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()


    # Function to stop program and close connection
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    # Function to write message to server
    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"

        # Encrypt message with server public key
        encrypted_message = encrypt_message(self.server_public_key,message)


        self.sock.send(encrypted_message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    # fucntion for handling incomming data
    def recive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')

                # Standard protocol for exchanging username and key values
                if message == "NCK":
                    self.sock.send(self.username.encode("utf-8"))
                if message == "PBK1":
                    self.sock.send(str(self.public_key[0]).encode("utf-8"))
                if message == "PBK2":
                    self.sock.send(str(self.public_key[1]).encode("utf-8"))
                
                if message.startswith('SVK1:'):
                    self.sock.send("ACK".encode("utf-8"))
                    self.server_public_key.append(int(message.split(":")[1]))
                    
                if message.startswith('SVK2:'):
                    self.sock.send("ACK".encode("utf-8"))
                    self.server_public_key.append(int(message.split(":")[1]))
                
                else:
                    if message == "NCK" or message == "PBK1" or message == "PBK2" or message.startswith('SVK1:') or message.startswith('SVK2:') :
                        pass
                    else:
                        # Decrypting data using own private key to make readble text
                        decrypted_message = decrypt_message(self.private_key, message)
                        if self.gui_done:
                            self.text_area.config(state='normal')
                            self.text_area.insert('end',decrypted_message)
                            self.text_area.yview('end')
                            self.text_area.config(state='disabled')

            # Exception for closing program
            except ConnectionAbortedError:
                exit(0)
                
            # Excetion for forced close on error
            except:
                print("Error")
                self.sock.close()
                exit(0)


client = Client()