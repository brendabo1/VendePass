# encoding: utf-8
import json
import threading
from modulos.msg_utils import enviar_mensagem


lock = threading.RLock()

def salvar_grafo_old(grafo, arquivo):
    """
    Salva o grafo de rotas em um arquivo JSON.
    
    Parâmetros:
    - grafo (dict): Estrutura do grafo de rotas com voos e assentos.
    - arquivo (str): Nome do arquivo JSON onde o grafo será salvo. Padrão: 'rotas3.json'.
    
    Retorna:
    - None
    """
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(grafo, f, ensure_ascii=False, indent=4)
        print(f"Grafo salvo com sucesso em '{arquivo}'.")
    except Exception as e:
        print(f"Erro ao salvar o grafo em '{arquivo}': {e}")

def carregar_grafo_old(arquivo):
    """
    Carrega o grafo de rotas a partir de um arquivo JSON.
    
    Parâmetros:
    - arquivo (str): Nome do arquivo JSON de onde o grafo será carregado. Padrão: 'rotas3.json'.
    
    Retorna:
    - dict: Estrutura do grafo de rotas carregada.
    - None: Se ocorrer um erro ou o arquivo não existir.
    """
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            rotas = json.load(f)
        print(f"Grafo carregado com sucesso a partir de '{arquivo}'.")
        return rotas
    except Exception as e:
        print(f"Erro ao carregar o grafo de '{arquivo}': {e}")
        return None

def carregar_grafo_lock(arquivo):
    """
    Carrega o grafo de rotas a partir de um arquivo JSON.
    
    Retorna:
    - dict: O grafo de rotas carregado do arquivo.
    """
    with lock:  # Garantir que apenas um thread carregue o grafo por vez
        try:
            with open(arquivo, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Arquivo de rotas não encontrado.")
            return {}
        except json.JSONDecodeError:
            print("Erro ao carregar o grafo de rotas (arquivo corrompido ou inválido).")
            return {}


def salvar_grafo_lock(rotas, arquivo):
    """
    Salva o grafo de rotas em um arquivo JSON.
    
    Parâmetros:
    - rotas (dict): O grafo de rotas a ser salvo.
    """
    with lock:  # Garantir que apenas um thread escreva no arquivo por vez
        with open(arquivo, 'w') as f:
            json.dump(rotas, f, indent=4)

def listar_todas_rotas(grafo):
    """
    Lista todas as rotas do sistema, exibindo origem, destino, código do voo e duração.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    """
    #grafo = carregar_grafo(arquivo_grafo)
    rotas_encontradas = []
    
    for origem, destinos in grafo.items():
        for destino, voos in destinos.items():
            for voo in voos:
                rota = {
                    'origem': origem,
                    'destino': destino,
                    'voo': voo['voo'],
                    'duracao': voo['duracao']
                }
                rotas_encontradas.append(rota)
    return rotas_encontradas

def buscar_rotas_possiveis(rotas, origem, destino):
    """
    Lista todas as rotas possíveis do aeroporto de origem até o destino.
    Permite que o usuário escolha uma das rotas listadas.
    
    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.
    
    Retorna:
    - list: Rota escolhida pelo usuário (lista de voos).
    """
    #rotas = carregar_grafo(arquivo_grafo)
    caminhos = []  # Lista para armazenar todas as rotas encontradas

    def dfs(current, target, path, visited):
        """
        Função auxiliar para realizar a busca em profundidade.

        Parâmetros:
        - current (str): Aeroporto atual.
        - target (str): Aeroporto de destino.
        - path (list): Lista de tuplas (voo, next_dest) que compõem a rota atual.
        - visited (set): Conjunto de aeroportos já visitados na rota atual.
        """
        if current == target:
            caminhos.append(list(path))  # Adiciona uma cópia da rota encontrada
            return

        if current not in rotas:
            return  # Aeroporto atual não possui voos de saída

        for next_dest, voos in rotas[current].items():
            if next_dest in visited:
                continue  # Evita ciclos

            for voo in voos:
                if voo['avaliable']:
                    # Adiciona o voo e o próximo destino à rota atual
                    path.append((voo, next_dest))
                    visited.add(next_dest)

                    # Chama recursivamente para o próximo destino
                    dfs(next_dest, target, path, visited)

                    # Remove o voo e o destino do conjunto de visitados após retornar
                    path.pop()
                    visited.remove(next_dest)

    # Inicia a busca em profundidade
    dfs(origem, destino, [], set([origem]))

    # Exibe os resultados
    if not caminhos:
        print(f"\nNenhuma rota encontrada de '{origem}' para '{destino}'.\n")
        return None

    # Lista todas as rotas encontradas
    print(f"\nRotas de '{origem}' para '{destino}':\n")
    for idx, caminho in enumerate(caminhos, 1):
        # Reconstrói a lista de aeroportos
        airports = [origem]
        for (voo, next_dest) in caminho:
            airports.append(next_dest)

        # Exibe o número da rota e o itinerário
        print(f"{idx}. Itinerário: {' -> '.join(airports)}")
        print("  Voos:")
        for voo, _ in caminho:
            print(f"    - {voo['voo']}, Duração: {voo['duracao']}")
        print("")  # Linha em branco para separar as rotas

    # Solicita ao usuário que escolha uma rota
    while True:
        try:
            limite = len(caminhos)
            escolha = int(input(f"Escolha uma rota (1-{limite}) ou {limite + 1} para Cancelar: "))
            if 1 <= escolha <= limite:
                rota_escolhida = []
                rota_escolhida = caminhos[escolha - 1]
                print(f"\nVocê escolheu a Rota {escolha}:")
                
                # Reconstrói a lista de aeroportos para a rota escolhida
                airports = [origem]
                for (voo, next_dest) in rota_escolhida:
                    airports.append(next_dest)
                
                print(f"  Itinerário: {' -> '.join(airports)}")
                print("  Voos:")
                for voo, _ in rota_escolhida:
                    print(f"    - {voo['voo']}, Duração: {voo['duracao']}")
                print("")  # Linha em branco

                break
            elif escolha == limite + 1:
                print("Saindo...")
                break
            else:
                print(f"Por favor, insira um número entre 1 e {limite + 1}.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    # Retorna a rota escolhida para ações futuras
    return rota_escolhida


def checa_disponibilidade_voo(origem, destino, cod_voo, arquivo_grafo):
    rotas = carregar_grafo_lock(arquivo_grafo)
    
    for voo in rotas[origem][destino]:
        if voo['voo'] == cod_voo:
            for assento in voo['assentos']:
                if not assento['avaliable']:
                    # Voo esgotado
                    return False
                continue
    return True

def buscar_rotas2(origem, destino, rotas):
    """
    Busca todas as rotas possíveis, incluindo conexões intermediárias,
    entre origem e destino no grafo de rotas.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.

    Retorna:
    - list: Lista de todas as rotas possíveis, onde cada rota é uma sequência de voos.
    """
    # rotas = carregar_grafo_lock(arquivo)
    caminhos = []  # Lista para armazenar todas as rotas encontradas

    def dfs(current, target, path, visited):
        """
        Realiza uma busca em profundidade para encontrar todas as rotas possíveis.
        
        Parâmetros:
        - current (str): Aeroporto atual no percurso.
        - target (str): Aeroporto de destino.
        - path (list): Lista de dicionários (voo, próximo destino) que compõem a rota atual.
        - visited (set): Conjunto de aeroportos já visitados, para evitar ciclos.
        """
        if current == target:
            caminhos.append(list(path))  # Adiciona uma cópia da rota encontrada
            return

        if current not in rotas:
            return  # Aeroporto atual não possui voos de saída

        for next_dest, voos in rotas[current].items():
            if next_dest in visited:
                continue  # Evita ciclos

            for voo in voos:
                if voo['avaliable']:
                    # Adiciona o voo e o próximo destino à rota atual
                    path.append({"voo": voo['voo'], "duracao": voo['duracao'], "next_dest": next_dest})
                    visited.add(next_dest)

                    # Continua a busca recursiva para o próximo destino
                    dfs(next_dest, target, path, visited)

                    # Remove o voo e o destino após a busca para outras rotas
                    path.pop()
                    visited.remove(next_dest)

    # Inicia a busca em profundidade a partir do aeroporto de origem
    dfs(origem, destino, [], set([origem]))

    # Retorna a lista de todas as rotas encontradas
    return caminhos


def tratar_reserva_assentos(sock, dados, rotas, arquivo):
    """
    Trata a solicitação de reserva de assentos.

    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao cliente.
    - dados (dict): Dados da mensagem recebida com voos selecionados e assentos escolhidos.
    """
    voos_selecionados = dados.get("voos", [])
    assentos_escolhidos = dados.get("assentos", {})

    with lock:  # Bloqueia para garantir que as operações de leitura/escrita sejam seguras
        #rotas = carregar_grafo_lock(arquivo)
        sucesso = True

        for trecho in voos_selecionados:
            voo_selecionado = trecho['voo']
            origem = trecho['origem']
            destino = trecho['next_dest']
            assento_escolhido = assentos_escolhidos.get(voo_selecionado)

            if origem in rotas and destino in rotas[origem]:
                for voo in rotas[origem][destino]:
                    if voo['voo'] == voo_selecionado:
                        for assento in voo['assentos']:
                            if assento['cod'] == assento_escolhido and assento['avaliable']:
                                assento['avaliable'] = False  # Reserva o assento
                                break
                        else:
                            sucesso = False
                        break

        # Salvar o grafo atualizado após a alteração dos assentos
        salvar_grafo_lock(rotas, arquivo)

    # Envia uma mensagem de confirmação ou erro ao cliente
    if sucesso:
        enviar_mensagem(sock, "RESERVA_CONFIRMADA", {"mensagem": "Reserva realizada com sucesso!"})
    else:
        enviar_mensagem(sock, "RESERVA_ERRO", {"mensagem": "Erro ao reservar os assentos."})


def buscar_assentos_disponiveis(rotas, voos_selecionados):
    """
    Busca os assentos disponíveis para cada voo em uma rota selecionada.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    - voos_selecionados (list): Lista de voos selecionados na rota.

    Retorna:
    - dict: Um dicionário com os assentos disponíveis para cada voo.
    """
    assentos_disponiveis = {}

    print(f"Voos selecionados recebidos: {voos_selecionados}")
    for trecho in voos_selecionados:
        voo_selecionado = trecho['voo']
        origem = trecho['origem']
        destino = trecho['next_dest']
        print(f"Verificando voo {voo_selecionado} de {origem} para {destino}")

        if origem in rotas and destino in rotas[origem]:
            for voo in rotas[origem][destino]:
                if voo['voo'] == voo_selecionado:
                    assentos = [assento['cod'] for assento in voo['assentos'] if assento['avaliable']]
                    assentos_disponiveis[voo_selecionado] = assentos
                    break
        else:
            print(f"Rota de {origem} para {destino} não encontrada.")
            return None

    return assentos_disponiveis



    