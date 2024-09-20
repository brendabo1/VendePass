import json

def enviar_mensagem(socket, tipo, dados):
    """
    Envia uma mensagem formatada para o cliente.
    """
    mensagem = json.dumps({'tipo': tipo, 'dados': dados}) 
    #+ '\n'
    try:
        socket.sendall(mensagem.encode('utf-8'))
    except socket.error as e:
        print(f"Erro ao enviar mensagem: {e}")

def receber_mensagem(socket):
    """
    Recebe uma mensagem do cliente e retorna o tipo e os dados.
    """
    try:
        mensagem = socket.recv(1024).decode()
        if not mensagem:
            return None, None
        dados = json.loads(mensagem)
        return dados.get('tipo'), dados.get('dados')
    except json.JSONDecodeError:
        print("Erro ao decodificar a mensagem recebida.")
        return None, None
    except socket.error as e:
        print(f"Erro ao receber mensagem: {e}")
        return None, None