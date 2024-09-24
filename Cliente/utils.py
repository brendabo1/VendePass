import json
from msg_utils import enviar_mensagem, receber_mensagem
import re

def login(socket):
    valido = False
    print('=' * 22 +  "LOGIN " + '=' * 22 +"\n\n" )
    print("\033[31m" +"Para Sair ID: 'x'" +"\033[0m")
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
                if assento.get('avaliable'):  # Verifica se a chave 'disponivel' existe e é True
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


def buscar_rotas_cliente(sock):
    """
    Função no lado do cliente que solicita ao servidor as rotas possíveis entre a origem e o destino.

    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.

    Retorna:
    - None: Apenas exibe as rotas recebidas.
    """
    legenda_aeroportos()
    print('=' * 44 + " Listar Rotas" + '=' * 44 +"\n\n")
    invalido = True
    while invalido:
        print("\033[31m" +"Para Sair insira 'x'" +"\033[0m")
        origem = input("Digite o código do aeroporto de origem (3 letras maiúsculas): ").strip().upper()
        if origem == 'x':
            return None
        elif not validar_codigo_aeroporto(origem):
            print("Código de aeroporto inválido. Deve conter 3 letras maiúsculas.\n")
            continue

        destino = input("Digite o código do aeroporto de destino (3 letras maiúsculas): ").strip().upper()
        if destino == 'x':
            return None
        elif not validar_codigo_aeroporto(destino):
            print("Código de aeroporto inválido. Deve conter 3 letras maiúsculas.\n")
            continue
       
        invalido = False
        break

    # Enviar a solicitação de busca de rotas para o servidor
    enviar_mensagem(sock, "LISTA_ROTA", {"origem": origem, "destino": destino})

    # Aguardar a resposta do servidor
    tipo, resposta = receber_mensagem(sock)

    if tipo == "LISTA_ROTA_RESP":
        rotas = resposta.get("rotas", [])
        
        if not rotas:
            print(f"Nenhuma rota encontrada de {origem} para {destino}.")
            return

        print(f"Rotas disponíveis de {origem} para {destino}:\n")
        
        # Listar todas as rotas encontradas
        for idx, rota in enumerate(rotas, 1):
            print(f"Rota {idx}:")
            aeroportos = [origem]  # A lista de aeroportos da rota começa pela origem
            for trecho in rota:
                aeroportos.append(trecho['next_dest'])
                print(f"    - {trecho['voo']}, Duração: {trecho['duracao']}")

            print(f"  Itinerário: {' -> '.join(aeroportos)}\n")

        # Opcional: Permitir ao usuário escolher uma rota para continuar com o processo
        on = True
        while on:
            try:
                escolha = int(input(f"Escolha uma rota (1-{len(rotas)}) ou {len(rotas) + 1} para Cancelar: "))
                if 1 <= escolha <= len(rotas):
                    rota_escolhida = rotas[escolha - 1]
                    voos_selecionados = []
                    current_origem = origem
                    for trecho in rota_escolhida:
                        voo_info = {
                            'voo': trecho['voo'],
                            'duracao': trecho['duracao'],
                            'origem': current_origem,  # Adiciona a origem atual ao trecho
                            'next_dest': trecho['next_dest']
                        }
                        voos_selecionados.append(voo_info)
                        current_origem = trecho['next_dest']  # Atualiza a origem para o próximo trecho
                    

                    print(f"\nVocê escolheu a Rota {escolha}:")
                    for trecho in rota_escolhida:
                        print(f"    - {trecho['voo']}, Duração: {trecho['duracao']}")
                    print("")
                    return voos_selecionados
                elif escolha == len(rotas) + 1:
                    print("Cancelando a escolha de rota...")
                    break
                else:
                    print(f"Por favor, insira um número entre 1 e {len(rotas) + 1}.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número válido.")
    else:
        print("Erro: Resposta inesperada do servidor.")
        return None

def reservar_assentos_cliente(sock, voos_selecionados):
    """
    Função no lado do cliente para visualizar os assentos disponíveis para cada voo e permitir a reserva.

    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    - voos_selecionados (list): Lista de voos da rota selecionada pelo usuário.
    """
    # Enviar a solicitação para obter os assentos disponíveis
    enviar_mensagem(sock, "LISTA_ASS", {"voos": voos_selecionados})

    # Receber a resposta com os assentos disponíveis
    tipo, resposta = receber_mensagem(sock)

    if tipo == "LISTA_ASS_RESP":
        assentos_disponiveis = resposta.get("assentos", {})
        assentos_escolhidos = {}

        # Mostrar assentos disponíveis para cada voo e permitir escolha
        for trecho in voos_selecionados:
            voo = trecho['voo']
            origem = trecho['origem']
            destino = trecho['next_dest']
            assentos = assentos_disponiveis.get(voo, [])

            if assentos:
                print(f"\nAssentos disponíveis para o {voo} de {origem} para {destino}: {', '.join(assentos)}")
                while True:
                    assento_escolhido = input(f"Escolha um assento para o voo {voo} (ou 'cancelar' para desistir): ")
                    if assento_escolhido in assentos:
                        assentos_escolhidos[voo] = assento_escolhido
                        break
                    elif assento_escolhido.lower() == 'cancelar':
                        print("Cancelando a escolha de assentos...")
                        return
                    else:
                        print("Assento inválido. Por favor, escolha novamente.")

        # Confirmar reserva dos assentos
        enviar_mensagem(sock, "RESERVAR_ASSENTOS", {"voos": voos_selecionados, "assentos": assentos_escolhidos})

        # Receber a confirmação da reserva
        tipo, resposta = receber_mensagem(sock)

        if tipo == "RESERVA_CONFIRMADA":
            print(resposta["mensagem"])
        elif tipo == "RESERVA_ERRO":
            print(resposta["mensagem"])

    else:
        print("Erro ao receber a lista de assentos disponíveis.")