import socket
import threading
import json
from rotas import gerar_caminhos, listar_caminhos_disponiveis

class Rota:
    def __init__(self, origem, destino, disponivel, preco, assentos):
        self.origem = origem
        self.destino = destino
        self.disponivel = disponivel
        self.preco = preco
        self.assentos = assentos
    
    def reservar_assento(self, assento):
        if assento in self.assentos:
            self.assentos.remove(assento)
        if len(self.assentos) == 0:
            self.disponivel = False
            return False
        return True
    
    def to_dict(self):
        return {
            "origem": self.origem,
            "destino": self.destino,
            "disponivel": self.disponivel,
            "preco": self.preco,
            "assentos": self.assentos
        }

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
                self.__threadPool[client] =  threading.Thread(target=self.handle_client, args=(connection,client))
                self.__threadPool[client].start()

                #self.handle_client(connection, client)
        except Exception as e:
            print("Erro: ", e.args)

        
    def handle_client(self, conn, addr):
        print("Nova conexao: ", addr)
        while True:
            try:
                data = conn.recv(1024).decode()
                print(data)
                if not data:
                    break
                requisicao = json.loads(data)
                print(requisicao)
                conn.close()
                print(f"Conexão encerrada com {addr}")

                if requisicao["tipo"] == "listar_rotas":
                    self.enviar_rotas(conn)
                elif requisicao["tipo"] == "comprar_passagem":
                    self.processar_compra(conn, requisicao)
            except OSError as e:
                print("erro na conexão ", addr, e.args)
                return
            except Exception as e:
                print(f"Erro nos dados recebidos do cliente: {addr}, {e.args}")
                conn.send(bytes("erro"))
                break
        conn.close()
        print(f"Conexão encerrada com {addr}")

    def reservar_assento(self, assento):
        # self._lock.acquire()
        # self._lock.release()
        pass

    def encontrar_rota(self, origem, destino):
        for rota in gerar_caminhos(origem, destino):
            return rota
        return None
    
    def enviar_rotas(self, conn):
        rotas_dict = [rota.to_dict() for rota in self.rotas]
        conn.sendall(json.dumps(rotas_dict).encode())
    
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

    
if __name__ == "__main__":
    host = '127.0.0.1'  # Localhost
    port = 12345        # Porta de conexão
    servidor = Servidor(host, port)
    servidor.start()
