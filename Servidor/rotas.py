# encoding: utf-8

def listar_caminhos_disponiveis(rotas):
    caminhos_disponiveis = []

    # Percorre todas as origens no grafo
    for origem, destinos in rotas.items():
        # Para cada destino a partir da origem
        for destino, voos in destinos.items():
            # Para cada voo que vai da origem ao destino
            for voo in voos:
                # Verifica se o voo está disponível
                if voo['disponivel']:
                    caminho = (f"Origem: {origem}, Destino: {destino}, "
                               f"Voo: {voo['voo']}, Assentos: {voo['assentos']}, "
                               f"Duração: {voo['duracao']}")
                    caminhos_disponiveis.append(caminho)
    
    # Exibe os caminhos disponíveis
    if caminhos_disponiveis:
        for caminho in caminhos_disponiveis:
            print(caminho)
    else:
        print("Nenhum caminho disponível.")

def gerar_caminhos(caminho, final):
    """Enumera todos os caminhos no grafo `grafo` iniciados por `caminho` e que terminam no vértice `final`."""

    # Se o caminho de fato atingiu o vértice final, não há o que fazer.
    if caminho[-1] == final:
        yield caminho
        return

    # Procuramos todos os vértices para os quais podemos avançar…
    for vizinho in rotas[caminho[-1]]:
        # …mas não podemos visitar um vértice que já está no caminho.
        if vizinho in caminho:
            continue
        # Se você estiver usando python3, você pode substituir o for
        # pela linha "yield from gerar_caminhos(grafo, caminho + [vizinho], final)"
        for caminho_maior in gerar_caminhos(rotas, caminho + [vizinho], final):
            yield caminho_maior

# Função para reservar um assento em um voo específico
def reservar_assento(rotas, origem, destino, voo_numero, assento):
    # Verifica se a origem existe no grafo de rotas
    if origem not in rotas:
        return f"Origem {origem} não encontrada."

    # Verifica se o destino existe a partir da origem
    if destino not in rotas[origem]:
        return f"Destino {destino} não encontrado a partir de {origem}."

    # Itera sobre os voos do destino para encontrar o voo específico
    for voo in rotas[origem][destino]:
        if voo['voo'] == voo_numero:
            # Verifica se o voo está disponível
            if not voo['disponivel']:
                return f"O voo {voo_numero} não está disponível."

            # Verifica se o assento está disponível
            if assento in voo['assentos']:
                # Remove o assento da lista de assentos disponíveis
                voo['assentos'].remove(assento)
                return f"Assento {assento} reservado com sucesso no voo {voo_numero}."
            else:
                return f"Assento {assento} não está disponível no voo {voo_numero}."
    
    return f"Voo {voo_numero} não encontrado de {origem} para {destino}."

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
            {"voo": "Voo AB123", "assentos": [1, 2, 3, 4, 5], "duracao": "1h30m", "disponivel": True},
            {"voo": "Voo AB456", "assentos": [1, 2, 3], "duracao": "1h20m", "disponivel": True}
        ],
        "LEC": [
            {"voo": "Voo AC789", "assentos": [1, 2, 3, 4], "duracao": "2h", "disponivel": True}
        ],
        "PAV": [
            {"voo": "Voo AC490", "assentos": [1, 2, 3, 4], "duracao": "2h", "disponivel": True}
        ],
        "GNM": [
            {"voo": "Voo AB7377", "assentos": [1, 2, 3, 4], "duracao": "2h", "disponivel": True}
        ],
        "VDC": [
            {"voo": "Voo AC364", "assentos": [1, 2, 3, 4], "duracao": "2h", "disponivel": True}
        ],
        "IOS": [
            {"voo": "Voo AB912", "assentos": [1, 2, 3, 4], "duracao": "2h", "disponivel": True}
        ]
    },
    "FEC": {
        "SSA": [
            {"voo": "Voo BA321", "assentos": [1, 2, 3, 4, 5], "duracao": "1h30m", "disponivel": True}
        ],
        "LEC": [
            {"voo": "Voo BC654", "assentos": [1, 2, 3], "duracao": "50m", "disponivel": True}
        ]
    },
    "LEC": {
        "SSA": [
            {"voo": "Voo CA987", "assentos": [1, 2, 3, 4], "duracao": "2h", "disponivel": True}
        ],
        "FEC": [
            {"voo": "Voo CB654", "assentos": [1, 2, 3], "duracao": "50m", "disponivel": True}
        ]
    }
}

# for caminho in gerar_caminhos(['FEC'], 'PAV'):
#     print(caminho)



listar_caminhos_disponiveis(rotas2)

    