import json
from msg_utils import enviar_mensagem, receber_mensagem
import re

def login(socket):
    valido = False
    print('=' * 44 +  "LOGIN " + '=' * 44 +"\n\n" )
    print("\033[31m" +"Para Sair insira 'x'" +"\033[0m")
    while not valido: 
        user_id = input("ID: ")
        if user_id == 'x' or user_id == 'X':
            enviar_mensagem(socket, 'LOGOUT', None)
            break
        senha = input("Senha: ")
        if not user_id or not senha:
            print("Usuário e senha não podem estar vazios.") 
        else: 
            valido = autentica(socket, user_id, senha)  
        
    return valido

def autentica(socket, user, senha):  
    enviar_mensagem(socket, 'LOGIN', {'id': user, 'senha': senha})
    # Recebe a resposta do servidor
    tipo, dados = receber_mensagem(socket)
    if tipo == 'LOGIN_RESPOSTA':
        if dados.get('sucesso'):
            print("Login bem-sucedido.\n")
            return True   
        else:
            print("ID e senha incorretos\n")
            return False

def legenda_aeroportos():
    print("                 Legenda AEROPORTOS\n"
        "(SSA) Salvador - Aeroporto Deputado Luís Eduardo Magalhães\n" + 
        "(IOS) Ilhéus - Aeroporto de Ilhéus - Jorge Amado\n" +
        "(BPS) Porto Seguro - Aeroporto de Porto Seguro\n" +
        "(LEC) Lençóis - Aeroporto Horácio de Mattos\n"  +
        "(PAV) Paulo Afonso- Aeroporto de Paulo Afonso\n" +
        "(BRA) Barreiras - Aeroporto de Barreiras\n" +
        "(FEC) Feira de Santana - Aeroporto João Durval Carneiro\n" +
        "(VAL) Valença - Aeroporto de Valença\n" +
        "(GNM) Guanambi - Aeroporto de Guanambi\n" 
        "(TXF) Teixeira de Freitas - Aeroporto de Teixeira de Freitas\n" +
        "(VDC) Vitória da Conquista - Aeroporto Glauber de Andrade Rocha\n")

def exibe_todas_rotas(socket):
    enviar_mensagem(socket, "LISTAR_TODAS_ROTAS", None)
    tipo, dados = receber_mensagem(socket)
    
    if tipo == 'TODAS_ROTAS_RESP':
        if not dados:
            print(f"Nenhuma rota encontrada.\n")
            return None
        
        print('=' * 44 + " ROTAS " + '=' * 44 +"\n\n")
        print(f"{'Origem':<10} {'Destino':<10} {'Voo':<15} {'Duração':<10}")
        print('-' * 44)
        for rota in dados:
            origem_str = str(rota['origem'])
            destino_str = str(rota['destino'])
            voo_str = str(rota['voo'])
            duracao_str = str(rota['duracao'])
            print(f"{origem_str:<10} {destino_str:<10} {voo_str:<15} {duracao_str:<10}")
        #print('-' * 44)
        legenda_aeroportos()
        return True
    else:
        mensagem = dados.get('mensagem')
        print(mensagem)
        return None

def validar_codigo_assento(codigo):
    """
    Valida se o código do assento segue o padrão esperado (Número seguido de Letra).
    
    Parâmetros:
    - codigo (str): Código do assento a ser validado.
    
    Retorna:
    - bool: True se válido, False caso contrário.
    """
    return bool(re.fullmatch(r'\d+[A-Z]', codigo))


def validar_codigo_aeroporto(codigo):
    """
    Valida se o código do aeroporto segue o padrão esperado (ex: 3 letras maiúsculas).

    Parâmetros:
    - codigo (str): Código do aeroporto a ser validado.

    Retorna:
    - bool: True se válido, False caso contrário.
    """
    return len(codigo) == 3 and codigo.isalpha() and codigo.isupper()


def listar_rota(sock):
    """
    Solicita e exibe todas as rotas possíveis de uma origem até um destino.
    
    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    
    Retorna:
    - dict: Dados da rota selecionada pelo usuário.
    """
    legenda_aeroportos()
    print('=' * 44 + " Listar Rotas" + '=' * 44 +"\n\n")
    invalido = True
    while invalido:
        print("\033[31m" +"Para Sair insira 'x'" +"\033[0m")
        origem = input("Digite o código do aeroporto de origem (3 letras maiúsculas): ").strip().upper()
        if not validar_codigo_aeroporto(origem):
            print("Código de aeroporto inválido. Deve conter 3 letras maiúsculas.\n")
            continue
        destino = input("Digite o código do aeroporto de destino (3 letras maiúsculas): ").strip().upper()
        if not validar_codigo_aeroporto(destino):
            print("Código de aeroporto inválido. Deve conter 3 letras maiúsculas.\n")
            continue
        if origem == 'x' or destino == 'x':
            return None
        invalido = False
        break
    
    if not invalido:
        # Envia a solicitação de listagem de rotas
        enviar_mensagem(sock, 'LISTA_ROTA', {'origem': origem, 'destino': destino})

    # Recebe a resposta do servidor
    tipo, dados = receber_mensagem(sock)

    if tipo == 'LISTA_ROTA_RESP':
        rotas = dados.get('rotas', [])
        if not rotas:
            print(f"Nenhuma rota encontrada de '{origem}' para '{destino}'.\n")
            return None
        
        print(f"\nRotas de '{origem}' para '{destino}':\n")
        for idx, rota in enumerate(rotas, 1):
            print(f"{idx}. Itinerário: {' -> '.join(rota['itinerario'])}")
            print("  Voos:")
            for voo in rota['voos']:
                print(f"    - {voo['voo']}, Duração: {voo['duracao']}")
            print("")  # Linha em branco para separar as rotas
        
        while True:
            try:
                escolha = int(input(f"Escolha uma rota para reservar (1-{len(rotas)}): "))
                if 1 <= escolha <= len(rotas):
                    rota_escolhida = rotas[escolha - 1]
                    print(f"\nVocê escolheu a Rota {escolha}:")
                    print(f"  Itinerário: {' -> '.join(rota_escolhida['itinerario'])}")
                    print("  Voos:")
                    for voo in rota_escolhida['voos']:
                        print(f"    - {voo['voo']}, Duração: {voo['duracao']}")
                    print("")  # Linha em branco
                    return rota_escolhida
                else:
                    print(f"Por favor, insira um número entre 1 e {len(rotas)}.\n")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número válido.\n")
    else:
        mensagem = dados.get('mensagem', 'Falha ao listar rotas.')
        print(f"Erro ao listar rotas: {mensagem}\n")
        return None

def reservar_assento(sock, origem, destino, rota):
    """
    Solicita a reserva de um assento específico em uma rota escolhida.
    
    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.
    - rota (dict): Detalhes da rota escolhida.
    
    Retorna:
    - bool: True se a reserva for bem-sucedida, False caso contrário.
    """
    print('=' * 44 + " Reservar Assento " + '=' * 44 +"\n\n" )
    voos = rota.get('voos', [])
    if not voos:
        print("Nenhum voo encontrado na rota escolhida.\n")
        return False

    # Exibe os voos disponíveis na rota
    print("\nVoos na rota escolhida:")
    for idx, voo in enumerate(voos, 1):
        print(f"{idx}. {voo['voo']} - Duração: {voo['duracao']}")
        for assento in voo['assentos']:
            # Verificar se o assento é um dicionário
            if isinstance(assento, dict):
                if assento.get('disponivel'):  # Verifica se a chave 'disponivel' existe e é True
                    print(assento['cod'])
    # for idx, voo in enumerate(voos, 1):
    #     print(f"{idx}. {voo['voo']} - Duração: {voo['duracao']}")
    #     for assento in voo['assentos']:
    #         for cadeira in assento:
    #             if cadeira['disponivel']:
    #                 print(cadeira['cod'])
    while True:
        try:
            escolha_voo = int(input(f"Escolha um voo para reservar (1-{len(voos)}): "))
            if 1 <= escolha_voo <= len(voos):
                voo_selecionado = voos[escolha_voo - 1]['voo']
                break
            else:
                print(f"Por favor, insira um número entre 1 e {len(voos)}.\n")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.\n")
    
    while True:
        assento = input("Digite o código do assento que deseja reservar (ex: 1A): ").strip().upper()
        if not validar_codigo_assento(assento):
            print("Código de assento inválido. Deve seguir o formato 'NúmeroLetra' (ex: 1A).\n")
            continue
        break

    # Envia a solicitação de reserva de assento
    enviar_mensagem(sock, 'RESERVA', {
        'origem': origem,
        'destino': destino,
        'cod_rota': rota['id'],  # 'id' corresponde ao 'cod_rota' esperado pelo servidor
        'cod_voo': voo_selecionado,
        'cod_assento': assento
    })

    # Recebe a resposta do servidor
    tipo, dados = receber_mensagem(sock)

    if tipo == 'RESERVA_RESP':
        if dados.get('sucesso'):
            print(f"Assento '{assento}' reservado com sucesso no voo '{voo_selecionado}'.\n")
            return True
        else:
            mensagem = dados.get('mensagem', 'Falha na reserva.')
            print(f"Falha na reserva: {mensagem}\n")
            return False
    else:
        mensagem = dados.get('mensagem', 'Falha ao reservar assento.')
        print(f"Erro ao reservar assento: {mensagem}\n")
        return False

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

