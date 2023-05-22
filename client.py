import socket

# Configurações do cliente
IP = '239.1.1.1'  # Endereço IP do grupo multicast
PORT = 12345  # Porta para comunicação

# Cria o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Configura o socket para permitir broadcasting
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Envia um comando para o servidor
command = "PWD"  # Comando FTP
client_socket.sendto(command.encode(), (IP, PORT))

# Aguarda a resposta do servidor
data, server_address = client_socket.recvfrom(1024)
print("Resposta do servidor: " + data.decode())

# Envia um comando para o servidor para obter a lista de arquivos
command = "LIST"
client_socket.sendto(command.encode(), (IP, PORT))

# Aguarda a resposta do servidor com a lista de arquivos
data, server_address = client_socket.recvfrom(1024)
print("Lista de arquivos do servidor:\n" + data.decode())

# Envia um comando para o servidor para baixar um arquivo
command = "GET alor.txt"
client_socket.sendto(command.encode(), (IP, PORT))

# Aguarda a resposta do servidor com o tamanho do arquivo
data, server_address = client_socket.recvfrom(1024)
file_size = int(data.decode())

if file_size != 0:
    # Cria um arquivo local para salvar os dados recebidos
    with open("arquivo_recebido.txt", 'wb')  as file:
        bytes_received = 0
        
        # Recebe os dados do arquivo em chunks de 1024 bytes
        while bytes_received < file_size:
            data, server_address = client_socket.recvfrom(1024)
            file.write(data)
            bytes_received += len(data)
        
    print("Arquivo recebido com sucesso.")
else:
    print("Arquivo não encontrado no servidor.")

# Fecha o socket do cliente
client_socket.close()
