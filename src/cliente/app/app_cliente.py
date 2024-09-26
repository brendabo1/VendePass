import socket
import os
from utils import login, exibe_todas_rotas, buscar_rotas_cliente, reservar_assentos_cliente, exibir_pedidos
from msg_utils import enviar_mensagem

class Cliente:
    def __init__(self, host, port=12345):
        self.__server_ip = host
        self.__port = port
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def sistema(self):
        
        try:
            autenticado = login(self.__client_socket)
            while autenticado:
                os.system('cls')
                
                print("--------------------- MENU ---------------------\n\n")
                print("1- Listar Todas as Rotas")
                print("2- Escolher Rota")
                print("3- Meus Pedidos")
                print("4- Sair")

                menuOption = input("Digite a opção do menu: ")
                if menuOption == '1':
                    all_rotas = exibe_todas_rotas(self.__client_socket)

                elif menuOption == "2":
                    os.system('cls')
                    voos_selecionados =  buscar_rotas_cliente(self.__client_socket) 
                    if voos_selecionados:
                        reservar_assentos_cliente(self.__client_socket, voos_selecionados, autenticado)
                        
                elif menuOption == "3": 
                    os.system('cls')
                    exibir_pedidos(self.__client_socket, autenticado)

                elif menuOption == "4":
                    os.system('cls')
                    print("Saindo...")
                    enviar_mensagem(self.__client_socket, 'LOGOUT', None)
                    autenticado = False
                    break
                else:
                    print("Opção inválida. Por favor, escolha novamente.\n")
                
        except socket.error as e:
            print(f"Erro de conexão: {e}")
    
        finally:
            self.fechar_conexao()
            print("Conexão encerrada")
    
    def fechar_conexao(self):
        self.__client_socket.close()

    def conectar(self):
        endpoint = (self.__server_ip, self.__port)
        try:
            self.__client_socket.connect(endpoint)
            #print(f"Conexao realizada com sucesso em {self.__server_ip}:{self.__port}")
            self.sistema()
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor. Certifique-se de que o servidor está em execução.")
        except Exception as e:
            print("Erro na conexão com o servidor ", e.args, e)
            self.fechar_conexao()
        except KeyboardInterrupt:
            print("Desligando...")
            self.fechar_conexao()


if __name__ == "__main__":
    ip = input("Insira o IP do Servidor: ")
    cliente = Cliente(host=ip)
    cliente.conectar()
