import socket
import os

# Configurações do servidor
IP = '239.1.1.1'  # Endereço IP do grupo multicast
PORT = 12345  # Porta para comunicação

# Cria o socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Configura o socket para permitir múltiplas conexões na mesma porta
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Liga o socket ao endereço IP e porta
server_socket.bind(('', PORT))

# Adiciona o socket ao grupo multicast
mreq = socket.inet_aton(IP) + socket.inet_aton('0.0.0.0')
server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print('Servidor FTP iniciado em {}:{}'.format(IP, PORT))

while True:
    # Aguarda a recepção de dados
    data, address = server_socket.recvfrom(1024)
    command = data.decode().strip().split(" ")
    
    # Lógica para processar os comandos FTP
    if command[0] == "PWD":
        server_socket.sendto(os.getcwd().encode(), address)
        
    elif command[0] == "LIST":
        files = os.listdir()
        file_list = "\n".join(files)
        server_socket.sendto(file_list.encode(), address)
        
    elif command[0] == "GET" and len(command) == 2:
        filename = command[1]
        if os.path.isfile(filename):
            file_size = os.path.getsize(filename)
            server_socket.sendto(str(file_size).encode(), address)
            
            with open(filename, 'rb') as file:
                while True:
                    chunk = file.read(1024)
                    if not chunk:
                        break
                    server_socket.sendto(chunk, address)
        else:
            server_socket.sendto("File not found".encode(), address)
    
    elif command[0] == "QUIT":
        server_socket.sendto("221 Goodbye.".encode(), address)
        break

# Fecha o socket do servidor
server_socket.close()
