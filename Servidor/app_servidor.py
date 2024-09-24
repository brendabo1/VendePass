import socket
import threading
import json
#from modulos.rotas import gerar_caminhos, listar_caminhos_disponiveis
from modulos.msg_utils import enviar_mensagem, receber_mensagem
from modulos.usuarios import autenticar_usuario
from modulos.utils import server_login
from modulos.rotas import listar_todas_rotas, buscar_rotas2, buscar_assentos_disponiveis, tratar_reserva_assentos
from modulos.grafo import carregar_grafo

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
                    print(f"Conexão com {addr} encerrada.")
                    conn.close()
                    break

                if tipo == 'LOGIN':
                    autenticado = server_login(conn, dados, ARQUIVO_USERS)
                
                elif tipo == 'LISTAR_TODAS_ROTAS':
                    if not autenticado:
                        enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária para listar rotas.'})
                        continue
                    grafo = carregar_grafo(ARQUIVO_GRAFO)
                    all_rotas = listar_todas_rotas(grafo)
                    enviar_mensagem(conn, 'TODAS_ROTAS_RESP', all_rotas)
                
                elif tipo == 'LISTA_ROTA':
                    if not autenticado:
                        enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária para listar rotas.'})
                        continue
                    origem = dados.get('origem')
                    destino = dados.get('destino')
                    if origem and destino:
                        grafo = carregar_grafo(ARQUIVO_GRAFO)
                        rotas_possiveis = buscar_rotas2(origem, destino, grafo)
                    enviar_mensagem(conn, 'LISTA_ROTA_RESP', {'rotas': rotas_possiveis})
                
                elif tipo == 'LISTA_ASS':
                    if not autenticado:
                        enviar_mensagem(conn, 'ERROR', {'mensagem': 'Autenticação necessária para reservar assentos.'})
                        continue
                    voos_selecionados = dados.get("voos", [])
                    grafo = carregar_grafo(ARQUIVO_GRAFO)
                    assentos_disponiveis = buscar_assentos_disponiveis(grafo, voos_selecionados)
                    print(assentos_disponiveis)
                    enviar_mensagem(conn, 'LISTA_ASS_RESP', {"assentos": assentos_disponiveis})
                elif tipo == "RESERVAR_ASSENTOS":
                    grafo = carregar_grafo(ARQUIVO_GRAFO)
                    print(tratar_reserva_assentos(conn, dados, grafo, ARQUIVO_GRAFO))
            
                elif tipo == 'LOGOUT':
                    print(f"Usuário {addr} solicitou logout.")
                    enviar_mensagem(conn, 'LOGOUT_RESP', {'sucesso': True})
                    on = False
                    break
                else:
                    enviar_mensagem(conn, "ERRO", {"mensagem": "Tipo de requisição desconhecido."})
        except socket.error as e:
            print(f"Erro na conexão com {addr}: {e}")
        except Exception as e:
            print(f"Erro na conexão com {addr}: {e}")
        finally:
            conn.close()
            print(f"Conexão com {addr} encerrada.")
            

    def fechar_conexao_servidor(self):
        self._tcp.close()
    
    def start(self):
        """Inicia a execução do serviço"""

        endpoint = (self._host, self._port)
        self._tcp.bind(endpoint)
        self._tcp.listen()
        while True:
            try:
                print("O servidor foi iniciado em ", self._host, self._port)
                connection, client = self._tcp.accept()  #aguarda a conexao do cliente
                self._threadPool[client] =  threading.Thread(target=self.handle_client, args=(connection,client))
                self._threadPool[client].start()
                print(f"Atendendo {client} em uma nova thread.")
            except KeyboardInterrupt:
                print("Servidor desligando...")
                self.fechar_conexao_servidor()
                break
            except Exception as e:
                print("Erro: ", e.args)
            
    
if __name__ == "__main__":
    host = '127.0.0.1'  # Localhost
    port = 12345        # Porta de conexão
    servidor = Servidor(host, port)
    servidor.start()
