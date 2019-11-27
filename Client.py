import socket

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.connect(('localhost',8080))

    

    request = "POST /test.txt HTTP/1.1\r\nHost: data.com\r\nIf-Modified-Since: Tue, 23 Nov 2019 15:53:04 -0700 \r\nUser-Agent: Firefox/3.6.10\r\nAccept: text/html,application/xhtml+xml\r\nAccept-Language: en-us,en;q=0.5\r\nContent-Length: 512\r\nConnection: keep-alive\r\n\r\n"
    
    serversocket.send(request.encode())
    upload = 'This is my uploaded file'

    serversocket.send(upload.encode())  
    print(serversocket.recv(1000).decode())

    
    serversocket.close()

main()