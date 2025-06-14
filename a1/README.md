Assignment #1

To run this program, open two terminals for the server and client.

Run the server first with this cmd python myvlserver.py

On the other terminal, run cmd python myvlclient.py

The client terminal will display this:
    Input lowercase sentence:

Enter a number based on the length of the message (only 2 bytes) eg:
    Input lowercase sentence: 15helloworldagain

The terminal will now show:
    From server:  HELLOWORLDAGAIN

On the server terminal, it will show:
    Connected from ('127.0.0.1', 39799)
    msg_len: 15
    processed: helloworldagain
    msg_len_sent: 15
    Connection closed

The server is still listening and the connection to client closed. To stop the program, manually kill the process.

In Windows, use the cmd is Get-Process -Name python to get the id then use Stop-Process -Id #.