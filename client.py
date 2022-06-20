import socket
import threading
import tkinter
from tkinter import dialog
import tkinter.scrolledtext
from tkinter import simpledialog
from pyrsa.pyrsa import create_key, decrypt_message, encrypt_message


HOST = "127.0.0.1"
PORT = 9090

class Client:
    def __init__(self, host, port):


        self.keypair = create_key()
        self.public_key = self.keypair[0]
        self.private_key = self.keypair[1]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))


        msg = tkinter.Tk()
        msg.withdraw()


        self.username = simpledialog.askstring("Username", "PLease create a username", parent=msg)

        self.gui_done = False

        self.running = True

        self.server_public_key = []

        gui_thread = threading.Thread(target=self.gui_loop)
        recive_thread = threading.Thread(target=self.recive)

        gui_thread.start()
        recive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
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

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        encrypted_message = encrypt_message(self.server_public_key,message)
        self.sock.send(encrypted_message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def recive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
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
                    print(self.server_public_key)
                

                else:
                    if message == "NCK" or message == "PBK1" or message == "PBK2" or message.startswith('SVK1:') or message.startswith('SVK2:') :
                        pass
                    else:
                        print(f"else {message}")
                        decrypted_message = decrypt_message(self.private_key, message)
                        if self.gui_done:
                            self.text_area.config(state='normal')
                            self.text_area.insert('end',decrypted_message)
                            self.text_area.yview('end')
                            self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                exit(0)
            except:
                print("Error")
                self.sock.close()
                exit(0)


client = Client(HOST,PORT)