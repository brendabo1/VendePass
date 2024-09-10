# encoding: utf-8

def gerar_caminhos(grafo, caminho, final):
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
        for caminho_maior in gerar_caminhos(grafo, caminho + [vizinho], final):
            yield caminho_maior

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

for caminho in gerar_caminhos(rotas, ['FEC'], 'PAV'):
    print(caminho)

    