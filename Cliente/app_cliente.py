import socket
import json
from utils import login, exibe_todas_rotas, listar_rota, reservar_assento
from msg_utils import enviar_mensagem, receber_mensagem

class Cliente:
    def __init__(self, host='127.0.0.1', port=12345):
        self.__server_ip = host
        self.__port = port
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def method(self):
        menu = True
        autenticado = login(self.__client_socket)
        while menu:
            print("--------------------- MENU ---------------------\n\n")
            print("1- Listar Todas as Rotas")
            print("2- Escolher Rota")
            print("3- Sair")

            menuOption = input("Digite a opção do menu: ")
            if menuOption == '1':
                all_rotas = exibe_todas_rotas(self.__client_socket)

            elif menuOption == "2":
                rota_escolhida = listar_rota(self.__client_socket)
                if rota_escolhida:
                    origem = rota_escolhida['itinerario'][0]
                    destino = rota_escolhida['itinerario'][-1]
                    reservar_assento(self.__client_socket, origem, destino, rota_escolhida)
                
            elif menuOption == "3":
                print("Saindo...")
                enviar_mensagem(socket, 'LOGOUT', None)
                cliente.fechar_conexao()
                menu = False
            else:
                print("Opção inválida. Por favor, escolha novamente.\n")
            
        #print("FIM DO PROGRAMA")
            # if not autenticado:
            #     print("nao autenticado")
            # else:
            #     print("autenticado")

        # except Exception as e:
        #     print("Erro na conexão com o servidor ", e.args)
        # finally:
        #     self.fechar_conexao()

    
    def fechar_conexao(self):
        self.__client_socket.close()

    def conectar(self):
        endpoint = (self.__server_ip, self.__port)
        try:
            self.__client_socket.connect(endpoint)
            print(f"Conexao realizada com sucesso em {self.__server_ip}:{self.__port}")
            self.method()
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor. Certifique-se de que o servidor está em execução.")
        except Exception as e:
            print("Erro na conexão com o servidor ", e.args, e)
            self.fechar_conexao()


if __name__ == "__main__":
    cliente = Cliente()
    cliente.conectar()


    # # Solicitar rotas disponíveis
    # rotas = cliente.solicitar_rotas()
    # print("Rotas disponíveis:")
    # for rota in rotas:
    #     status = "Disponível" if rota["disponivel"] else "Indisponível"
    #     print(f'{rota["origem"]} -> {rota["destino"]}: {status} - Preço: {rota["preco"]}')

    # # Solicitar compra de passagem
    # origem = input("Escolha a origem: ")
    # destino = input("Escolha o destino: ")
    # assento = input("Escolha o assento: ")

    # resposta_final = cliente.comprar_passagem(origem, destino, assento)
    # print(resposta_final["mensagem"])
    # if resposta_final["status"] == "sucesso":
    #     print(f"Preço: {resposta_final['preco']}")

    #cliente.fechar_conexao()