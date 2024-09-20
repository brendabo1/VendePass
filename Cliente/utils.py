import json
from msg_utils import enviar_mensagem, receber_mensagem

def login(socket):
    valido = False
    print("---------------------LOGIN---------------------\n\n")
    print("\033[31m" +"Para Sair insira 'x'" +"\033[0m")
    while not valido: 
        user_id = input("ID: ")
        if user_id == 'x' or user_id == 'X':
            return valido
        senha = input("Senha: ")
        enviar_mensagem(socket, 'LOGIN', {'id': user_id, 'senha': senha})
        receber_mensagem(socket)
        # return valido
    
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

def validar_codigo_aeroporto(codigo):
    """
    Valida se o código do aeroporto segue o padrão esperado (ex: 3 letras maiúsculas).

    Parâmetros:
    - codigo (str): Código do aeroporto a ser validado.

    Retorna:
    - bool: True se válido, False caso contrário.
    """
    return len(codigo) == 3 and codigo.isalpha() and codigo.isupper()

def menu():
    menu = True

    while menu:
        print("===== MENU =====")
        print("1- Comprar passagem")
        print("2- Sair")

        menuOption = input("Digite a opção do menu: ")
    
            
        if menuOption == '1':
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

        elif menuOption == "2":
            print("SAINDO")
            cliente.fechar_conexao()
            menu = False
        else:
            print("DIGITE UM VALOR VÁLIDO")
        
    print("FIM DO PROGRAMA")

