![alt text](img/pychatlogo.png?raw=true "PYCHAT")

# PYCHAT #
## An RSA encrypted client server messaging app ##

### About ###

PYCHAT lets you chat with other users connected to the PYCHAT server using an ecrypted websocket data stream between client and server. I made this project to learn more about websockets and to give my previous program  [PYRSA](https://github.com/youssefboulmalf/PYRSA "PYRSA") an actual use case.


### Installation ###

to install and use PYCHAT simply clone the repo

```git clone https://github.com/youssefboulmalf/PYRSA.git ./ ```

### Usage ###

Run the PYCHAT server file.

```python ./server.py ```

To connect to the server run the client file.

```python ./client.py```

The gui will ask for the host ip and port number.
(By default this will be 127.0.0.1:9090 but you can change that in the source code of server.py)

### EXTRA ###
*screenshot of the gui*

![alt text](images/chatting.jpg?raw=true "chatting")

*screenshot of raw packet capture of the communication between PYCHAT client and server*

![alt text](images/data.jpg?raw=true "data")


- - -

> If you want to participate/contribute, feel free to create pull requests or issues so we can make PYCHAT better and more efficient !

