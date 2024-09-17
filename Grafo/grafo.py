import networkx as nx

# Criar um grafo direcionado
G = nx.Graph()

G.add_node("A", cidade="Salvador")
G.add_node("B", cidade="Ilhéus")
G.add_node("C", cidade="Porto Seguro")
G.add_node("D", cidade="Lençois")
G.add_node("E", cidade="Barreiras")
G.add_node("F", cidade="Vitória da Conquista")
G.add_node("G", cidade="Paulo Afonso")
G.add_node("H", cidade="Feira de Santana")
G.add_node("I", cidade="Guanambi")
G.add_node("J", cidade="Teixeira de Freitas")

# Adicionar nós e arestas
edges = [
    ('A', 'B', 3), ('A', 'C', 3), ('A', 'D', 33), ('A', 'E', 3), ('A', 'F', 3), ('A', 'G', 3), ('A', 'H', 3), ('A', 'I', 3), ('A', 'J', 3),
    ('B', 'C', 3), ('B', 'F', 5),
    ('C', 'F', 3), ('C', 'J', 3),
    ('D', 'E', 3), ('D', 'F', 5),('D', 'G', 3), ('D', 'H', 3),('D', 'I', 3),
    ('E', 'G', 3), ('E', 'I', 3),('E', 'J', 3),
    ('F', 'H', 3), ('F', 'I', 3),('F', 'J', 3),
    ('G', 'H', 3), ('G', 'J', 3)
]

# Definir a propriedade 'vaga' nas arestas
for u, v, weight in G.edges:
    G[u][v]['vaga'] = 5

# Adicionar arestas ao grafo com propriedades
for u, v, weight in edges:
    G.add_edge(u, v, weight=weight, vaga=5, assentos=["1A", "1B", "2A", "2B"])

# Encontrar o caminho mais curto de A para G
caminho = nx.shortest_path(G, source='B', target='D')

comprimento = nx.shortest_path_length(G, source='B', target='D')

caminho_dijkstra = nx.dijkstra_path(G, source='B', target='D', weight='weight')

distancia_dijkstra = nx.dijkstra_path_length(G, source='B', target='D', weight='weight')


# Atualizar a propriedade 'vaga' ao longo do caminho
for i in range(len(caminho) - 1):
    u = caminho[i]
    v = caminho[i + 1]
    if 'vaga' in G[u][v]:
        G[u][v]['vaga'] = max(G[u][v]['vaga'] - 1, 0)  # Diminui a vaga, mas não deixa o valor negativo

# Verificar a propriedade 'vaga' nas arestas
for u, v in G.edges:
    print(f"Aresta ({G.nodes[u]['cidade']}, {G.nodes[v]['cidade']}) tem a propriedade 'vaga': {G[u][v]['vaga']}")

print(comprimento)
print(caminho_dijkstra)
print(distancia_dijkstra)

for i in range(len(caminho_dijkstra) - 1):
    u = caminho_dijkstra[i]
    v = caminho_dijkstra[i + 1]
    if 'assentos' in G[u][v]:
        G[u][v]['assentos'].remove('1A') # Diminui a vaga, mas não deixa o valor negativo
        print(f"Rota {u} à {v}, assentos disponiveis: {G[u][v]['assentos']}")
