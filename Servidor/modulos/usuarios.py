import json
import re


def salvar_usuarios(dados, nome_arquivo):
    with open(nome_arquivo, 'w+') as arquivo:
        json_obj=json.dumps(dados)
        arquivo.write(json_obj)  # Salvando como JSON

# Função para carregar os usuários de um arquivo JSON
def carregar_usuarios(arquivo):
    try:
        with open(arquivo, 'r') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir, estiver vazio ou mal formatado, retorna uma lista vazia
        print(f"Arquivo {arquivo} não encontrado. Criando um novo arquivo.")
        return []

def autenticar_usuario(iduser, senha, nome_arquivo):
    usuarios = carregar_usuarios(nome_arquivo)
    for usuario in usuarios:
        if usuario['id'] == iduser and usuario['senha'] == senha:
            return usuario  # Autenticação bem-sucedida
    return None  # Autenticação falhou

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

    print(f"Usuário {nome} adicionado com ID {novo_id}.")

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

# novo_pedido = {
#     "numero": 103,
#     "voo": "CD789",
#     "assento": 20,
#     "data": "2023-11-10"
# }

# Adicionando um pedido para o usuário 'USR001'
#adicionar_pedido('USR002', novo_pedido, arquivo_usuarios)
# inicializa_usuarios()
# usuarios_carregados = carregar_usuarios()
# print("\nUsuários carregados:")
# for u in usuarios_carregados:
#     print(u)

    

