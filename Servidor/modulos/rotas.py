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

# def gerar_caminhos(grafo, caminho, final):
#     """Enumera todos os caminhos no grafo `grafo` iniciados por `caminho` e que terminam no vértice `final`."""

#     # Se o caminho de fato atingiu o vértice final, não há o que fazer.
#     if caminho[-1] == final:
#         yield caminho
#         return

#     # Procuramos todos os vértices para os quais podemos avançar…
#     for vizinho in grafo[caminho[-1]]:
#         # …mas não podemos visitar um vértice que já está no caminho.
#         if vizinho in caminho:
#             continue
#         # Se você estiver usando python3, você pode substituir o for
#         # pela linha "yield from gerar_caminhos(grafo, caminho + [vizinho], final)"
#         for caminho_maior in gerar_caminhos(grafo, caminho + [vizinho], final):
#             yield caminho_maior


# def reservar_assento(origem, destino, cod_voo, cod_assento, arquivo="grafo_rotas.json"):
#     """
#     Reserva um assento para um voo específico, modificando o grafo de rotas e salvando no arquivo JSON.
    
#     Parâmetros:
#     - origem (str): Aeroporto de origem.
#     - destino (str): Aeroporto de destino.
#     - cod_voo (str): Código do voo.
#     - cod_assento (str): Código do assento a ser reservado.
#     - arquivo (str): Nome do arquivo JSON para salvar o grafo atualizado.
    
#     Retorna:
#     - None
#     """
#     # Carregar o grafo atual do arquivo JSON
#     rotas = carregar_grafo(arquivo)

#     if not rotas:
#         print("Erro ao carregar o grafo.")
#         return

#     # Verificar se a rota existe no grafo
#     if origem not in rotas or destino not in rotas[origem]:
#         print(f"Rota de {origem} para {destino} não encontrada.")
#         return
    
#     # Buscar o voo correspondente e tentar reservar o assento
#     for voo in rotas[origem][destino]:
#         if voo['voo'] == cod_voo:
#             # Procurar o assento disponível
#             for assento in voo['assentos']:
#                 if assento['cod'] == cod_assento:
#                     if assento['disponivel']:
#                         # Reservar o assento
#                         assento['disponivel'] = False
#                         print(f"Assento {cod_assento} reservado com sucesso no {cod_voo}.")
                        
#                         # Salvar o grafo modificado no arquivo JSON
#                         salvar_grafo(rotas, arquivo)
#                         return
#                     else:
#                         print(f"Assento {cod_assento} já está reservado.")
#                         return
    
#     print(f"Voo {cod_voo} ou assento {cod_assento} não encontrados.")

"""
(SSA) Salvador - Aeroporto Deputado Luís Eduardo Magalhães 
(IOS) Ilhéus - Aeroporto de Ilhéus - Jorge Amado 
(BPS) Porto Seguro - Aeroporto de Porto Seguro 
(LEC) Lençóis - Aeroporto Horácio de Mattos 
(PAV) Paulo Afonso- Aeroporto de Paulo Afonso 
(BRA) Barreiras - Aeroporto de Barreiras 
(FEC) Feira de Santana - Aeroporto João Durval Carneiro 
(VAL) Valença - Aeroporto de Valença 
(GNM) Guanambi - Aeroporto de Guanambi 
(TXF) Teixeira de Freitas - Aeroporto de Teixeira de Freitas 
(VDC) Vitória da Conquista - Aeroporto Glauber de Andrade Rocha 
"""
rotas = {'SSA': ['FEC', 'LEC', 'PAV', 'GNM', 'VDC', 'IOS'], 
         'FEC': ['SSA', 'LEC', 'PAV', 'VDC'], 
         'LEC': ['SSA', 'FEC'],
         'PAV': ['SSA', 'FEC', 'BRA'], 
         'BRA': ['FEC', 'PAV', 'GNM'], 
         'GNM': ['SSA', 'BRA', 'VDC'], 
         'VDC': ['SSA', 'FEC', 'GNM', 'TXF'], 
         'IOS': ['SSA', 'BPS'], 
         'BPS': ['IOS', 'TXF'],  
         'TXF': ['VDC', 'BPS']}

rotas2 = {
    "SSA": {
        "FEC": [
            {
                "voo": "Voo AB123",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False},
                    {"cod": "2C", "disponível": True}
                ],
                "duracao": "1h30m",
                "disponivel": True
            },
            {
                "voo": "Voo AB456",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False}
                ],
                "duracao": "1h20m",
                "disponivel": True
            }
        ],
        "LEC": [
            {
                "voo": "Voo AC789",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False}
                ],
                "duracao": "2h",
                "disponivel": True
            }
        ],
        "PAV": [
            {
                "voo": "Voo AC490",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": False},
                    {"cod": "2A", "disponível": True},
                    {"cod": "2B", "disponível": False}
                ],
                "duracao": "2h",
                "disponivel": True
            }
        ],
        "GNM": [
            {
                "voo": "Voo AB7377",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False}
                ],
                "duracao": "2h",
                "disponivel": True
            }
        ],
        "VDC": [
            {
                "voo": "Voo AC364",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False}
                ],
                "duracao": "2h",
                "disponivel": True
            }
        ],
        "IOS": [
            {
                "voo": "Voo AB912",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False}
                ],
                "duracao": "2h",
                "disponivel": True
            }
        ]
    },
    "FEC": {
        "SSA": [
            {
                "voo": "Voo BA321",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False},
                    {"cod": "2C", "disponível": True}
                ],
                "duracao": "1h30m",
                "disponivel": True
            }
        ],
        "LEC": [
            {
                "voo": "Voo BC654",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False}
                ],
                "duracao": "50m",
                "disponivel": True
            }
        ]
    },
    "LEC": {
        "SSA": [
            {
                "voo": "Voo CA987",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False},
                    {"cod": "2B", "disponível": False}
                ],
                "duracao": "2h",
                "disponivel": True
            }
        ],
        "FEC": [
            {
                "voo": "Voo CB654",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponível": False}
                ],
                "duracao": "50m",
                "disponivel": True
            }
        ]
    }
}

def buscar_rotas(origem, destino, arquivo_grafo):
    """
    Busca todas as rotas possíveis de origem até destino.
    
    Parâmetros:
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.
    
    Retorna:
    - list: Lista de rotas encontradas.
    """
    rotas = carregar_grafo(arquivo_grafo)
    if not rotas:
        print("Nenhuma rota carregada.")
        return None
    rotas_encontradas = []
    if origem in rotas and destino in rotas[origem]:
        for voo in rotas[origem][destino]:
            if voo['disponivel']:
                rota = {
                    'itinerario': [origem, destino],
                    'voos': [{
                        'voo': voo['voo'],
                        'assentos':voo['assentos'],
                        'duracao': voo['duracao']
                    }],
                    'id': voo['voo']  # Usaremos o código do voo como ID único da rota
                }
                rotas_encontradas.append(rota)
    else:
        print(f"Rota de '{origem}' para '{destino}' não encontrada.")
    return rotas_encontradas

def checa_disponibilidade_voo(origem, destino, cod_voo, arquivo_grafo):
    rotas = carregar_grafo_lock(arquivo_grafo)
    
    for voo in rotas[origem][destino]:
        if voo['voo'] == cod_voo:
            for assento in voo['assentos']:
                if not assento['disponivel']:
                    # Voo esgotado
                    return False
                continue
    return True

def reservar_assento(origem, destino, cod_voo, cod_assento, rotas):
    """
    Reserva um assento específico em um voo e salva o grafo atualizado.
    
    Parâmetros:
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.
    - cod_voo (str): Código do voo.
    - cod_assento (str): Código do assento a ser reservado.
    - arquivo (str): Caminho para o arquivo JSON de rotas.
    
    Retorna:
    - dict: Resultado da operação com status e mensagem.
    """
    #rotas = carregar_grafo(arquivo_grafo)
    if not rotas:
        #logging.error("Erro ao carregar rotas para reserva.")
        return {'sucesso': False, 'mensagem': 'Erro ao carregar rotas.'}
    
    if origem not in rotas:
        #logging.warning(f"Origem '{origem}' não encontrada.")
        return {'sucesso': False, 'mensagem': f"Origem '{origem}' não encontrada."}
    if destino not in rotas[origem]:
        #logging.warning(f"Destino '{destino}' não encontrado a partir de '{origem}'.")
        return {'sucesso': False, 'mensagem': f"Destino '{destino}' não encontrado a partir de '{origem}'."}
    
    for voo in rotas[origem][destino]:
        if voo['voo'] == cod_voo:
            for assento in voo['assentos']:
                if assento['cod'] == cod_assento:
                    if assento['disponivel']:
                        assento['disponivel'] = False
                        salvar_grafo_lock(rotas, arquivo_grafo)
                        return {'sucesso': True, 'mensagem': f"Assento '{cod_assento}' reservado com sucesso no voo '{cod_voo}'."}
                    else:
                        return {'sucesso': False, 'mensagem': f"Assento '{cod_assento}' já está reservado no voo '{cod_voo}'."}
    return {'sucesso': False, 'mensagem': f"Voo '{cod_voo}' ou assento '{cod_assento}' não encontrado."}

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

def buscar_assentos_disponiveis_old(rotas, voos_selecionados):
    """
    Busca os assentos disponíveis para cada voo em uma rota selecionada.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    - voos_selecionados (list): Lista de voos selecionados na rota.

    Retorna:
    - dict: Um dicionário com os assentos disponíveis para cada voo.
    """
    assentos_disponiveis = {}

    for trecho in voos_selecionados:
        voo_selecionado = trecho['voo']
        origem = trecho['origem']
        destino = trecho['next_dest']

        # Verifica se o voo existe entre os aeroportos de origem e destino
        if origem in rotas and destino in rotas[origem]:
            for voo in rotas[origem][destino]:
                if voo['voo'] == voo_selecionado:
                    # Adiciona os assentos disponíveis ao dicionário
                    assentos_disponiveis[voo_selecionado] = [assento['cod'] for assento in voo['assentos'] if assento['disponivel']]
                    break

    return assentos_disponiveis


def tratar_reserva_assentos_sem_lock(sock, dados, grafo):
    """
    Trata a solicitação de reserva de assentos.

    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao cliente.
    - dados (dict): Dados da mensagem recebida com voos selecionados e assentos escolhidos.
    """
    voos_selecionados = dados.get("voos", [])
    assentos_escolhidos = dados.get("assentos", {})

    # Atualizar o status dos assentos no grafo de rotas (rotas3)
    sucesso = True
    for trecho in voos_selecionados:
        voo_selecionado = trecho['voo']
        origem = trecho['origem']
        destino = trecho['next_dest']
        assento_escolhido = assentos_escolhidos.get(voo_selecionado)

        if origem in grafo and destino in grafo[origem]:
            for voo in grafo[origem][destino]:
                if voo['voo'] == voo_selecionado:
                    for assento in voo['assentos']:
                        if assento['cod'] == assento_escolhido and assento['disponivel']:
                            assento['disponivel'] = False  # Reserva o assento
                            break
                    else:
                        sucesso = False
                    break

    # Envia uma mensagem de confirmação ou erro ao cliente
    if sucesso:
        enviar_mensagem(sock, "RESERVA_CONFIRMADA", {"mensagem": "Reserva realizada com sucesso!"})
    else:
        enviar_mensagem(sock, "RESERVA_ERRO", {"mensagem": "Erro ao reservar os assentos."})

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
                    # assentos = [
                    #         assento['cod'] for assento in voo['assentos'] 
                    #         if assento.get('disponivel', False)  # Usamos get() para evitar erro caso a chave não exista
                    #     ]
                        
                    # # Verifica se há assentos disponíveis para este voo
                    # if assentos:
                    #     assentos_disponiveis[voo_selecionado] = assentos
                    # else:
                    #     assentos_disponiveis[voo_selecionado] = "Sem assentos disponíveis"
                    # break
                    #assentos = [assento['cod'] for assento in voo['assentos'] if assento['disponivel']]
                    #assentos_disponiveis[voo_selecionado] = assentos
                    print(assentos_disponiveis)
                    #assentos_disponiveis[voo_selecionado] = [assento['cod'] for assento in voo['assentos'] if assento['disponivel']]
                    break
        else:
            print(f"Rota de {origem} para {destino} não encontrada.")
            return None

    return assentos_disponiveis

#print(rotas2["SSA"]["FEC"])
#listar_rotas_possiveis(rotas2, "SSA", "IOS")


    