import socket
import datetime
import sys
import os

def server_start():

    create_hosts()
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.bind(('', 8080))
   
    serversocket.listen(5)

    i = 0
    while i < 100:
        i += 1
        
        
        (clientsocket, address) = serversocket.accept()
        #now do something with the clientsocket
        #in this case, we'll pretend this is a threaded server
        #ct = client_thread(clientsocket)
        #ct.run()
        connection(clientsocket)
        

            

            
def create_hosts():

    hosts = []
    directory = os.getcwd() + '/'

    with open('hosts.txt') as host_file:
        try:

            for host in host_file:
                
                os.mkdir(directory + host.rstrip('\n'))
        except:
            pass
        
    

def connection(socket):
    try:

        file = ''
       
        request = socket.recv(1000).decode()
        
        file, request, post = parse_request(request)
        response = generate_reply(request, file, post)
        
        socket.send(response)

        if post[0] and request == 1:
            receive_data(post, socket, file)


    finally:
        socket.close()

def receive_data(post, socket, file):

    data = socket.recv(post[1]).decode()

    file_object = open(file, 'w')

    file_object.write(data)

    

def parse_request(message):
    
    file_requested = ''
    found_file = False
    header_size = len(message) - 6
    directory = ''
    post = [0,0,0]
    
        
    file_requested, second_line, post = check_first_line(message)


    if(second_line == -1):

        reply_type = 0

    else:

        host = get_host(message)
        post.append(host) 
        valid_format = check_format(message[second_line:])

        if(valid_format) and (host != ''):

            directory = os.getcwd() + '/' + host + '/'
            
            for filename in os.listdir(directory):
                
                if(filename == file_requested[1:]):
                    
                    found_file = True
                    file_requested = directory + filename
                    break

            if found_file or post[0]:

                reply_type = 1

            else:
                reply_type = -1

        else:
            if not valid_format:
                reply_type = 0
            else:
                reply_type = -1
    
    return file_requested, reply_type, post

def get_host(message):
    host = ''
    start = message.find('Host:') + 5
    end = 0
    found = False

    if(start != 4):
        for i in range(start, len(message)):
            
            if(message[i] == '\r'):
                end = i
                break
        host = message[start:end].strip(' ')

    for filename in os.listdir(os.getcwd()):
        
        if filename == host:
            found = True
    
    if not found:
        host = ''
    return host

def check_first_line(message):

    tokens = []
    lastIndex = 0
    k = 0
    http_version = False
    correct = False
    file_requested = ''
    post = [False,0]

    for k in range(0, len(message)):
        if(message[k] == '\n'):
            break

    for l in range(0,k):
        if(message[l] == ' '):
            tokens.append(message[lastIndex:l])
            lastIndex = l + 1
    tokens.append(message[lastIndex:l])

    if(len(tokens) == 3):
        
        for token in tokens:
            
            if(token[0] == '/'):

                file_requested = token
                
            if('HTTP/1.1' in token):
                
                if(tokens[0] == 'GET'):
                    correct = True
                elif(tokens[0] == 'POST'):
                    correct = True

                    post[0] = True
                    post[1] = get_content_length(message)

        if(correct== False) or post[1] == -1:

            k = -1

        return file_requested, k, post

def get_content_length(message):

    length = ''
    index = message.lower().find('content-length:')
    number_location = index + len('content-length:')

    message = message[number_location:].strip(' ')

    if (index != -1):
        
        for i in range(0, len(message)):

            if(message[i] != '\r') and (message[i] != '\n'):
                length += message[i]

            else:
                break

        length.strip(' ')

        try:

            length = int(length)
        except:

            length = -1
        

    else:
        length = index

    return length


def check_format(message):

    i = 0
    header_size = len(message) - 3
    valid = True
    message = message.strip('\n')
    while (i < header_size) and valid:
            

            if(message[i].isalpha() or message[i] == '-'):
                i += 1
            else:
                if (message[i] == ':'):
                    for k in range(i+1, len(message)):

                        if(message[k] == ':'):

                            valid = False
                            break
                        elif(message[k] == '\n'):
                            break
                    i = k + 1 
                else:
                    
                    valid = False

                
    
    return valid

def generate_reply(type, file, post):

    file_contents = ''
    reply = ''
    d = datetime.datetime.today()
    
    if(type == 1):
        reply += "HTTP/1.1 200 OK\n" ;
        reply += "Date: " + d.strftime("%d-%B-%Y %H:%M:%S") + "\n"
        reply += "Server: Juan's Python Server (" + sys.platform + ")\n"
        
        if not post[0]:

            attachment = open(file, 'r')
            file_contents = attachment.read()
            reply += "Content-Length: " + str(len(file_contents.encode())) + '\n\n'
            reply += file_contents


    if(type == 0):
        reply += "HTTP/1.1 400 Bad Request\n" 
        reply += "Date: " + d.strftime("%d-%B-%Y %H:%M:%S") + "\n"
        reply += "Server: Juan's Python Server (" + sys.platform + ")\n"



    if(type == -1):
        reply += "HTTP/1.1 404 Not Found\n" 
        reply += "Date: " + d.strftime("%d-%B-%Y %H:%M:%S") + "\n"
        reply += "Server: Juan's Python Server (" + sys.platform + ")\n"

    
    return reply.encode()
server_start()