import socket
import ssl

host = 'www.google.com'
port = 443
ctx = ssl.create_default_context()

with socket.create_connection((host,port)) as sock:
    with ctx.wrap_socket(sock,server_hostname=host) as ssock:
        ssock.sendall((f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n").encode())

        response =""
        while True:
            data = ssock.recv(1024).decode()
            if not data:
                break
            response += data

        #retrieve only the html part
        idx = response.find("\r\n\r\n") + 4
        html_response = response[idx:]


        with open("response.html", "w") as f:
            f.write(html_response)
        


