import socket

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.connect(('localhost',8080))

    

    request = "POST /upload.txt HTTP/1.1\r\nHost: daata.com\r\nUser-Agent: Firefox/3.6.10\r\nAccept: text/html,application/xhtml+xml\r\nAccept-Language: en-us,en;q=0.5\r\nContent-Length: 512\r\nConnection: keep-alive\r\n"
    
    serversocket.send(request.encode())



    print(serversocket.recv(1000).decode())

    upload = 'This is my uploaded file'

    serversocket.send(upload.encode())
    serversocket.close()

main()