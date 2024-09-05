import socket
import json

class Cliente:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def conectar(self):
        self.client_socket.connect((self.host, self.port))
    
    def solicitar_rotas(self):
        requisicao = {"tipo": "listar_rotas"}
        self.client_socket.sendall(json.dumps(requisicao).encode())
        rotas = json.loads(self.client_socket.recv(1024).decode())
        return rotas
    
    def comprar_passagem(self, origem, destino, assento):
        requisicao = {"tipo": "comprar_passagem", "origem": origem, "destino": destino}
        self.client_socket.sendall(json.dumps(requisicao).encode())

        resposta = json.loads(self.client_socket.recv(1024).decode())
        if resposta["status"] == "sucesso":
            print(resposta["mensagem"])
            print("Assentos disponíveis: ", resposta["assentos_disponiveis"])

            requisicao_assento = {"assento": assento}
            self.client_socket.sendall(json.dumps(requisicao_assento).encode())
            
            resposta_final = json.loads(self.client_socket.recv(1024).decode())
            return resposta_final
        else:
            return resposta

    def fechar_conexao(self):
        self.client_socket.close()

if __name__ == "__main__":
    cliente = Cliente()
    cliente.conectar()

    # Solicitar rotas disponíveis
    rotas = cliente.solicitar_rotas()
    print("Rotas disponíveis:")
    for rota in rotas:
        status = "Disponível" if rota["disponivel"] else "Indisponível"
        print(f'{rota["origem"]} -> {rota["destino"]}: {status} - Preço: {rota["preco"]}')

    # Solicitar compra de passagem
    origem = input("Escolha a origem: ")
    destino = input("Escolha o destino: ")
    assento = input("Escolha o assento: ")

    resposta_final = cliente.comprar_passagem(origem, destino, assento)
    print(resposta_final["mensagem"])
    if resposta_final["status"] == "sucesso":
        print(f"Preço: {resposta_final['preco']}")

    cliente.fechar_conexao()