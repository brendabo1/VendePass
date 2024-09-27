# encoding: utf-8
import threading
from modulos.msg_utils import enviar_mensagem
from modulos.grafo import salvar_grafo, carregar_grafo
from modulos.usuarios import carregar_usuarios, anexar_pedido_usuario

lock = threading.RLock()


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


def atualizar_disponibilidade_voo(rotas, origem, destino, voo_selecionado):
    """
    Atualiza a disponibilidade de um voo com base na disponibilidade dos assentos.
    
    Se todos os assentos estiverem ocupados (avaliable = False), o voo será marcado como indisponível.
    Caso haja ao menos um assento disponível, o voo será marcado como disponível.

    Parâmetros:
    - rotas (dict): Dicionário contendo as rotas e voos disponíveis.
    - origem (str): Cidade de origem do voo.
    - destino (str): Cidade de destino do voo.
    - voo_selecionado (str): Identificação do voo a ser atualizado.
    """
    if origem in rotas and destino in rotas[origem]:
        for voo in rotas[origem][destino]:
            if voo['voo'] == voo_selecionado:
                # Verifica se há ao menos um assento disponível
                voo_disponivel = any(assento['avaliable'] for assento in voo['assentos'])
                
                # Atualiza o status do voo com base na disponibilidade dos assentos
                voo['avaliable'] = voo_disponivel
                break


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


def tratar_reserva_assentos(sock, dados, rotas, user_id, arquivo_rotas, arquivo_usuarios):
    """
    Trata a solicitação de reserva de assentos e anexa o pedido ao usuário.

    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao cliente.
    - dados (dict): Dados da mensagem recebida com voos selecionados e assentos escolhidos.
    - rotas (dict): Grafo das rotas e voos disponíveis.
    - arquivo_rotas (str): Caminho do arquivo que contém o grafo de rotas.
    - arquivo_usuarios (str): Caminho do arquivo que contém os dados dos usuários.
    """
    voos_selecionados = dados.get("voos", [])
    assentos_escolhidos = dados.get("assentos", {})

    with lock:  # Bloqueia para garantir que as operações de leitura/escrita sejam seguras
        sucesso = True
        pedidos_usuario = []

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
                                # Cria o pedido para o trecho
                                pedido_trecho = {
                                    'origem': origem,
                                    'destino': destino,
                                    'voo': voo_selecionado,
                                    'assento': assento_escolhido
                                }
                                
                                pedidos_usuario.append(pedido_trecho)
                                break
                        else:
                            sucesso = False
                            break
                
                # Após a reserva, atualiza a disponibilidade do voo
                atualizar_disponibilidade_voo(rotas, origem, destino, voo_selecionado)

        # Salvar o grafo atualizado após a alteração dos assentos
        salvar_grafo(rotas, arquivo_rotas)

        if sucesso:   
            #atualizar_disponibilidade_voo(origem, destino, voo_selecionado, arquivo_rotas)
            # Carregar usuários e anexar o pedido ao usuário
            pedido_completo = {
                'voos': pedidos_usuario
            }
            anexar_pedido_usuario(user_id, pedido_completo, arquivo_usuarios)



    # Envia uma mensagem de confirmação ou erro ao cliente
    if sucesso:
        enviar_mensagem(sock, "RESERVA_CONFIRMADA", {"mensagem": "Reserva realizada com sucesso!"})
    else:
        enviar_mensagem(sock, "RESERVA_ERRO", {"mensagem": "Não foi possível reservar estes assentos. Tente novamente."})


def buscar_assentos_disponiveis(rotas, voos_selecionados, arquivo_grafo):
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
        # print(f"Verificando voo {voo_selecionado} de {origem} para {destino}")

        if origem in rotas and destino in rotas[origem]:
            for voo in rotas[origem][destino]:
                if voo['voo'] == voo_selecionado:
                    # if checa_disponibilidade_voo(origem, destino, voo['voo'], rotas, arquivo_grafo):
                    assentos = [assento['cod'] for assento in voo['assentos'] if assento['avaliable']]
                    assentos_disponiveis[voo_selecionado] = assentos
                    break
                else:
                    continue
            else:
                    return None
        else:
            return None

    return assentos_disponiveis



    