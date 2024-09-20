# encoding: utf-8

import json


def salvar_grafo(grafo, arquivo="data/grafo_rotas.json"):
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

def carregar_grafo(arquivo='rotas3.json'):
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

def listar_todas_rotas(rotas):
    """
    Lista todas as rotas do sistema, exibindo origem, destino, código do voo e duração.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    """
    # Cabeçalho da tabela
    print(f"{'Origem':<10} {'Destino':<10} {'Voo':<10} {'Duração':<10}")
    print("-" * 40)
    
    for origem, destinos in rotas.items():
        for destino, voos in destinos.items():
            for voo in voos:
                origem_str = origem
                destino_str = destino
                voo_str = voo['voo']
                duracao_str = voo['duracao']
                print(f"{origem_str:<10} {destino_str:<10} {voo_str:<10} {duracao_str:<10}")
    print("-" * 40)  # Linha de fechamento


def listar_rotas_possiveis(rotas, origem, destino):
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
                if voo['disponivel']:
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


def reservar_assento(origem, destino, cod_voo, cod_assento, arquivo="grafo_rotas.json"):
    """
    Reserva um assento para um voo específico, modificando o grafo de rotas e salvando no arquivo JSON.
    
    Parâmetros:
    - origem (str): Aeroporto de origem.
    - destino (str): Aeroporto de destino.
    - cod_voo (str): Código do voo.
    - cod_assento (str): Código do assento a ser reservado.
    - arquivo (str): Nome do arquivo JSON para salvar o grafo atualizado.
    
    Retorna:
    - None
    """
    # Carregar o grafo atual do arquivo JSON
    rotas = carregar_grafo(arquivo)

    if not rotas:
        print("Erro ao carregar o grafo.")
        return

    # Verificar se a rota existe no grafo
    if origem not in rotas or destino not in rotas[origem]:
        print(f"Rota de {origem} para {destino} não encontrada.")
        return
    
    # Buscar o voo correspondente e tentar reservar o assento
    for voo in rotas[origem][destino]:
        if voo['voo'] == cod_voo:
            # Procurar o assento disponível
            for assento in voo['assentos']:
                if assento['cod'] == cod_assento:
                    if assento['disponivel']:
                        # Reservar o assento
                        assento['disponivel'] = False
                        print(f"Assento {cod_assento} reservado com sucesso no {cod_voo}.")
                        
                        # Salvar o grafo modificado no arquivo JSON
                        salvar_grafo(rotas, arquivo)
                        return
                    else:
                        print(f"Assento {cod_assento} já está reservado.")
                        return
    
    print(f"Voo {cod_voo} ou assento {cod_assento} não encontrados.")

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


# listar_todas_rotas(rotas3)
#print(rotas2["SSA"]["FEC"])
# listar_rotas_possiveis(rotas2, "PAV", "IOS")
salvar_grafo(rotas2)

    