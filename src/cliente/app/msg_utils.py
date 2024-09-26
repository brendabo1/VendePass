    
import json
import socket

def enviar_mensagem(sock, tipo, dados):
    """
    Envia uma mensagem JSON para o servidor, terminando com um delimitador de nova linha.
    
    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    - tipo (str): Tipo da mensagem (e.g., 'LOGIN', 'LIST_ROUTES').
    - dados (dict): Dados associados à mensagem.
    
    Retorna:
    - None
    """
    mensagem = json.dumps({'tipo': tipo, 'dados': dados}) + '\n'
    try:
        sock.sendall(mensagem.encode('utf-8'))
    except socket.error as e:
        print(f"Erro ao enviar mensagem: {e}")
    except Exception as a:
        print(a)

def receber_mensagem(sock):
    """
    Recebe uma mensagem JSON do servidor. A função espera até que uma nova linha '\n' seja recebida.
    
    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    
    Retorna:
    - tuple: (tipo, dados) se a mensagem for recebida com sucesso.
    - (None, None) se a conexão for fechada ou ocorrer um erro.
    """
    buffer = ''
    while True:
        try:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                # Conexão fechada pelo servidor
                return None, None
            buffer += data
            if '\n' in buffer:
                mensagem, buffer = buffer.split('\n', 1)
                dados = json.loads(mensagem)
                tipo = dados.get('tipo')
                conteudo = dados.get('dados')
                return tipo, conteudo
        except json.JSONDecodeError:
            print("Erro ao decodificar a mensagem recebida.")
            return None, None
        except socket.error as e:
            print(f"Erro ao receber mensagem: {e}")
            return None, None
        except Exception as a:
            print(a)
