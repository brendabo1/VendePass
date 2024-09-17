import networkx as nx

# Criar um grafo direcionado
G = nx.DiGraph()

G.add_node("SSA", cidade="Salvador")
G.add_node("IOS", cidade="Ilhéus")
G.add_node("BPS", cidade="Porto Seguro")
G.add_node("LEC", cidade="Lençois")
G.add_node("BRA", cidade="Barreiras")
G.add_node("VDC", cidade="Vitória da Conquista")
G.add_node("PAV", cidade="Paulo Afonso")
G.add_node("FEC", cidade="Feira de Santana")
G.add_node("GNM", cidade="Guanambi")
G.add_node("TXF", cidade="Teixeira de Freitas")

# Adicionar nós e arestas
edges = [
    ('SSA', 'IOS', 33), ('SSA', 'BPS', 33), ('SSA', 'LEC', 33), ('SSA', 'BRA', 33), ('SSA', 'VDC', 33), ('SSA', 'PAV', 33), ('SSA', 'FEC', 33), ('SSA', 'GNM', 33), ('SSA', 'TXF', 33),
    ('IOS', 'SSA', 5), ('IOS', 'BPS', 3), ('IOS', 'VDC', 5),
    ('BPS', 'SSA', 3), ('BPS', 'IOS', 3), ('BPS', 'VDC', 3), ('BPS', 'TXF', 3),
    ('LEC', 'SSA', 3), ('LEC', 'BRA', 3), ('LEC', 'VDC', 5), ('LEC', 'PAV', 3), ('LEC', 'FEC', 3),('LEC', 'GNM', 3),
    ('BRA', 'SSA', 3), ('BRA', 'LEC', 3), ('BRA', 'PAV', 3), ('BRA', 'GNM', 3),('BRA', 'TXF', 3),
    ('VDC', 'SSA', 3), ('VDC', 'IOS', 3), ('VDC', 'BPS', 3), ('VDC', 'LEC', 3), ('VDC', 'FEC', 3), ('VDC', 'GNM', 3),('VDC', 'TXF', 3),
    ('PAV', 'SSA', 3), ('PAV', 'LEC', 3), ('PAV', 'BRA', 3), ('PAV', 'FEC', 3), ('PAV', 'TXF', 3),
    ('FEC', 'SSA', 3), ('FEC', 'LEC', 3), ('FEC', 'VDC', 3), ('FEC', 'PAV', 3),
    ('GNM', 'SSA', 3), ('GNM', 'LEC', 3), ('GNM', 'BRA', 3), ('GNM', 'VDC', 3),
    ('TXF', 'SSA', 3), ('TXF', 'BPS', 3), ('TXF', 'VDC', 3)
]

# Definir a propriedade 'vaga' nas arestas
for u, v, weight in G.edges:
    G[u][v]['vaga'] = 5

# Adicionar arestas ao grafo com propriedades
for u, v, weight in edges:
    G.add_edge(u, v, weight=weight, vaga=5, assentos=["1A", "1B", "2A", "2B"])

# Encontrar o caminho mais curto de A para G
caminho = nx.shortest_path(G, source='TXF', target='BRA')

comprimento = nx.shortest_path_length(G, source='TXF', target='BRA')

caminho_dijkstra = nx.dijkstra_path(G, source='TXF', target='BRA', weight='weight')

distancia_dijkstra = nx.dijkstra_path_length(G, source='TXF', target='BRA', weight='weight')

# Função para calcular o peso total de um caminho
def path_weight(graph, path):
    weight = 0
    for i in range(len(path) - 1):
        # Soma o peso da aresta entre os nós consecutivos no caminho
        weight += graph[path[i]][path[i + 1]].get('weight', 0)
    return weight

comprimento_ponderado = path_weight(G, caminho)

# Atualizar a propriedade 'vaga' ao longo do caminho
for i in range(len(caminho) - 1):
    u = caminho[i]
    v = caminho[i + 1]
    if 'vaga' in G[u][v]:
        G[u][v]['vaga'] = max(G[u][v]['vaga'] - 1, 0)  # Diminui a vaga, mas não deixa o valor negativo

# Verificar a propriedade 'vaga' nas arestas
for u, v in G.edges:
    print(f"Aresta ({G.nodes[u]['cidade']}, {G.nodes[v]['cidade']}) tem a propriedade 'vaga': {G[u][v]['vaga']}")

print(caminho)
print(comprimento)
print(comprimento_ponderado)
print(caminho_dijkstra)
print(distancia_dijkstra)

for i in range(len(caminho_dijkstra) - 1):
    u = caminho_dijkstra[i]
    v = caminho_dijkstra[i + 1]
    if 'assentos' in G[u][v]:
        G[u][v]['assentos'].remove('1A') # Diminui a vaga, mas não deixa o valor negativo
        print(f"Rota {u} à {v}, assentos disponiveis: {G[u][v]['assentos']}")
 