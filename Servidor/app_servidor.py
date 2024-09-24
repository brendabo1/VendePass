import socket
import threading
import json
#from modulos.rotas import gerar_caminhos, listar_caminhos_disponiveis
from modulos.msg_utils import enviar_mensagem, receber_mensagem
from modulos.usuarios import autenticar_usuario
from modulos.utils import server_login
from modulos.rotas import listar_todas_rotas, buscar_rotas, reservar_assento

ARQUIVO_USERS= "data/usuarios.json"
ARQUIVO_GRAFO= "data/grafo_rotas.json"

class Servidor():
    
    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._threadPool = {}
        self._lock = threading.Lock()


    def handle_client(self, conn, addr):
        print("Nova conexao funcao handle: ", addr)
        on = True
        autenticado = False
        try:
            while on:
                tipo, dados = receber_mensagem(conn)
                if not tipo:
                    print(f"Conexão com {addr} encerrada condicional de tipo.")
                    break

                if tipo == 'LOGIN':
                    autenticado = server_login(conn, dados, ARQUIVO_USERS)
                
                elif tipo == 'LISTAR_TODAS_ROTAS':
                    if not autenticado:
                        enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária para listar rotas.'})
                        continue
                    all_rotas = listar_todas_rotas(ARQUIVO_GRAFO)
                    enviar_mensagem(conn, 'TODAS_ROTAS_RESP', all_rotas)
                
                elif tipo == 'LISTA_ROTA':
                    if not autenticado:
                        enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária para listar rotas.'})
                        continue
                    origem = dados.get('origem')
                    destino = dados.get('destino')
                    rotas = buscar_rotas(origem, destino, ARQUIVO_GRAFO)
                    enviar_mensagem(conn, 'LISTA_ROTA_RESP', {'rotas': rotas})
                
                elif tipo == 'RESERVA':
                    self._lock.acquire()
                    if not autenticado:
                        enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária para reservar assentos.'})
                        continue
                    origem = dados.get('origem')
                    destino = dados.get('destino')
                    cod_voo = dados.get('cod_voo')
                    cod_assento = dados.get('cod_assento')
                    resultado = reservar_assento(origem, destino, cod_voo, cod_assento, ARQUIVO_GRAFO)
                    enviar_mensagem(conn, 'RESERVA_RESP', resultado)
                    self._lock.release()
            
                elif tipo == 'LOGOUT':
                    print(f"Usuário {addr} solicitou logout.")
                    enviar_mensagem(conn, 'LOGOUT_RESP', {'sucesso': True})
                    on = False
                    break
        except Exception as e:
            print(f"Erro na conexão com {addr}: {e}")
        finally:
        # conn.close()
        # print(f"Conexão com {addr} encerrada.")
            pass
        

            # elif tipo == 'LIST_ROUTES':
            #     if not autenticado:
            #         enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária.'})
            #         continue
            #     origem = dados.get('origem')
            #     destino = dados.get('destino')
            #     rotas = buscar_rotas(origem, destino)
            #     enviar_mensagem(conn, 'LIST_ROUTES_RESP', {'rotas': rotas})

            # elif tipo == 'RESERVE_SEAT':
            #     if not autenticado:
            #         enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária.'})
            #         continue
            #     origem = dados.get('origem')
            #     destino = dados.get('destino')
            #     cod_voo = dados.get('cod_voo')
            #     cod_assento = dados.get('cod_assento')
            #     resultado = reservar_assento(origem, destino, cod_voo, cod_assento)
            #     enviar_mensagem(conn, 'RESERVE_SEAT_RESP', resultado)


        # else:
        #     print(f"Tipo de mensagem desconhecido: {tipo}")
        #     enviar_mensagem(conn, 'ERROR', {'mensagem': 'Tipo de mensagem desconhecido.'})

        
        # while True:
        #     try:
        #         data = receber_mensagem
        #         data = conn.recv(1024).decode()
        #         print(data)
        #         if not data:
        #             break
        #         requisicao = json.loads(data)
        #         print(requisicao)
        #         conn.close()
        #         print(f"Conexão encerrada com {addr}")

        #         if requisicao["tipo"] == "listar_rotas":
        #             self.enviar_rotas(conn)
        #         elif requisicao["tipo"] == "comprar_passagem":
        #             self.processar_compra(conn, requisicao)
        #     except OSError as e:
        #         print("erro na conexão ", addr, e.args)
        #         return
        #     except Exception as e:
        #         print(f"Erro nos dados recebidos do cliente: {addr}, {e.args}")
        #         conn.send(bytes("erro"))
        #         break
        # conn.close()
        # print(f"Conexão encerrada com {addr}")

    def reservar_assento(self, assento):
        # self._lock.acquire()
        # self._lock.release()
        pass


    
    def processar_compra(self, conn, requisicao):
        origem = requisicao["origem"]
        destino = requisicao["destino"]

        rota = self.encontrar_rota(origem, destino)
        if rota and rota.disponivel:
            resposta = {
                "status": "sucesso",
                "mensagem": "Rota encontrada, escolha um assento",
                "assentos_disponiveis": rota.assentos
            }
            conn.sendall(json.dumps(resposta).encode())

            data = conn.recv(1024).decode()
            requisicao_assento = json.loads(data)
            assento_escolhido = requisicao_assento["assento"]

            if rota.reservar_assento(assento_escolhido):
                resposta_final = {
                    "status": "sucesso",
                    "mensagem": f"Compra realizada com sucesso! Assento {assento_escolhido} reservado.",
                    "preco": rota.preco
                }
            else:
                resposta_final = {"status": "falha", "mensagem": "Assento indisponível."}
            
            conn.sendall(json.dumps(resposta_final).encode())
        else:
            resposta = {"status": "falha", "mensagem": "Rota indisponível ou inexistente"}
            conn.sendall(json.dumps(resposta).encode())

    def fechar_conexao_servidor(self):
        self._tcp.close()
    
    def start(self):
        """Inicia a execução do serviço"""

        endpoint = (self._host, self._port)
        try:
            self._tcp.bind(endpoint)
            self._tcp.listen()
            print("O servidor foi iniciado em ", self._host, self._port)
            while True:
                connection, client = self._tcp.accept()  #aguarda a conexao do cliente
                # thread handle client
                self._threadPool[client] =  threading.Thread(target=self.handle_client, args=(connection,client))
                self._threadPool[client].start()
                print(f"Atendendo {client} em uma nova thread.")

                #self.handle_client(connection, client)
        except Exception as e:
            print("Erro: ", e.args)
        finally:
            connection.close()
            # for client_thread in self._threadPool:
            #     client_thread.join()
    
if __name__ == "__main__":
    host = '127.0.0.1'  # Localhost
    port = 12345        # Porta de conexão
    servidor = Servidor(host, port)
    servidor.start()
