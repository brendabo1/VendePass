import json
import re
import threading
from modulos.msg_utils import enviar_mensagem


lock = threading.RLock()


def salvar_usuarios(dados, nome_arquivo):
    with lock:
        with open(nome_arquivo, 'w') as arquivo:
            json_obj=json.dumps(dados)
            arquivo.write(json_obj)  # Salvando como JSON

# Função para carregar os usuários de um arquivo JSON
def carregar_usuarios(arquivo):
    try:
        with lock:
            with open(arquivo, 'r') as arquivo:
                return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir, estiver vazio ou mal formatado, retorna uma lista vazia
        print(f"Arquivo {arquivo} não encontrado. Criando um novo arquivo.")
        return []

def autenticar_usuario(sock, dados, nome_arquivo):
    usuarios = carregar_usuarios(nome_arquivo)
    user_id = dados['id']
    user_senha = dados['senha']
    for usuario in usuarios:
        if usuario['id'] == user_id and usuario['senha'] == user_senha:
            enviar_mensagem(sock, "LOGIN_SUCESSO", {'id': user_id, 'nome': usuario['nome']})
            return user_id # Autenticação bem-sucedida
     # Se não encontrar o usuário ou senha inválida
    enviar_mensagem(sock, "LOGIN_FALHA", {'mensagem': 'Nome de usuário ou senha incorretos.'})



# Função para gerar o próximo ID de usuário no formato USR000
def gerar_proximo_id(usuarios):
    ultimo_id = 0

    # Procurar o maior número de ID já registrado
    for usuario in usuarios:
        match = re.match(r"USR(\d+)", usuario['id'])
        if match:
            numero_id = int(match.group(1))
            if numero_id > ultimo_id:
                ultimo_id = numero_id
    
    # Incrementa o último ID encontrado
    proximo_id = ultimo_id + 1

    # Retorna o próximo ID no formato USR000
    return f"USR{proximo_id:03d}"

def cria_novo_usuario(nome, senha, arquivo):
    usuarios = carregar_usuarios(arquivo)
    novo_id = gerar_proximo_id(usuarios)

    novo_usuario = {
    "id": novo_id,
    "nome": nome,
    "senha": senha,
    "pedidos": []
    }
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios, arquivo)

    # print(f"Usuário {nome} adicionado com ID {novo_id}.")

# Função para adicionar um novo pedido ao usuário especificado
def adicionar_pedido(id, pedido, arquivo):
    usuarios = carregar_usuarios(arquivo)

    # Procura o usuário peloid
    for usuario in usuarios:
        if usuario['id'] ==id:
            # Adiciona o novo pedido à lista de pedidos do usuário
            usuario['pedidos'].append(pedido)
            break
    else:
        print(f"Usuário com ID {id} não encontrado.")
        return

    # Salva a lista de usuários atualizada
    salvar_usuarios(usuarios, arquivo)
    print(f"Pedido adicionado ao usuário {id}.")

def inicializa_usuarios(arquivo_usuarios):
    # Adicionando novos usuários
    cria_novo_usuario("João", "senha123", arquivo_usuarios)
    cria_novo_usuario("Maria", "senha456", arquivo_usuarios)
    cria_novo_usuario("Felipe", "senha123", arquivo_usuarios)
    cria_novo_usuario("Ze", "senha456", arquivo_usuarios)
    cria_novo_usuario("Ana Flavia", "senha123", arquivo_usuarios)
    cria_novo_usuario("Pedro", "senha456", arquivo_usuarios)

def anexar_pedido_usuario(usuario_id, pedido, arquivo_usuarios):
    """Anexa o pedido ao usuário com o ID fornecido."""
    usuarios = carregar_usuarios(arquivo_usuarios)
    usuario_encontrado = False
    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            usuario['pedidos'].append(pedido)
            salvar_usuarios(usuarios, arquivo_usuarios)
            #print(f"Pedido adicionado ao usuário {usuario_id}.")
            break
    if not usuario_encontrado:
        #print(f"Usuário com ID {usuario_id} não encontrado.")
        return

def pedidos_usuario(sock, usuario_id, arquivo_usuarios):
    """
    Exibe os pedidos de um usuário com base no seu ID e envia a resposta via socket.

    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao cliente.
    - usuario_id (str): O ID do usuário cujo histórico de pedidos será exibido.
    - arquivo_usuarios (str): Caminho do arquivo que contém os dados dos usuários.
    
    Retorna:
    - Envia a lista de pedidos do usuário via socket ou uma mensagem de erro caso o usuário não seja encontrado ou não tenha pedidos.
    """
    # Carrega a lista de usuários do arquivo
    usuarios = carregar_usuarios(arquivo_usuarios)
    
    # Busca o usuário pelo ID
    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            # Verifica se o usuário tem pedidos
            if usuario['pedidos']:
                # Envia a lista de pedidos via socket
                enviar_mensagem(sock, "EXIBIR_PEDIDOS", {"mensagem": f"Pedidos do usuário {usuario['nome']}", "pedidos": usuario['pedidos']})
            else:
                # Envia uma mensagem informando que o usuário não tem pedidos
                enviar_mensagem(sock, "EXIBIR_PEDIDOS", {"mensagem": f"Usuário {usuario['nome']} (ID: {usuario_id}) não tem pedidos."})
            return

    # Se o usuário não for encontrado, envia uma mensagem de erro
    enviar_mensagem(sock, "EXIBIR_PEDIDOS", {"mensagem": f"Usuário com ID {usuario_id} não encontrado."})


# inicializa_usuarios()
# usuarios_carregados = carregar_usuarios()
# print("\nUsuários carregados:")
# for u in usuarios_carregados:
#     print(u)

    

