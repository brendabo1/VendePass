# Estrutura de rotas3 atualizada
rotas3 = {
    "SSA": {
        "FEC": [
            {
                "voo": "Voo AB123",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False},
                    {"cod": "2C", "disponivel": True}
                ],
                "duracao": "1h30m",
                "disponivel": True
            },
            {
                "voo": "Voo AB456",
                "assentos": [
                    {"cod": "1A", "disponivel": True},
                    {"cod": "1B", "disponivel": True},
                    {"cod": "2A", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False}
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
                    {"cod": "2A", "disponivel": True},
                    {"cod": "2B", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False},
                    {"cod": "2C", "disponivel": True}
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
                    {"cod": "2A", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False},
                    {"cod": "2B", "disponivel": False}
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
                    {"cod": "2A", "disponivel": False}
                ],
                "duracao": "50m",
                "disponivel": True
            }
        ]
    }
}

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
    paths = []  # Lista para armazenar todas as rotas encontradas

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
            paths.append(list(path))  # Adiciona uma cópia da rota encontrada
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
    if not paths:
        print(f"\nNenhuma rota encontrada de '{origem}' para '{destino}'.\n")
        return None

    # Lista todas as rotas encontradas
    print(f"\nRotas de '{origem}' para '{destino}':\n")
    for idx, path in enumerate(paths, 1):
        # Reconstrói a lista de aeroportos
        airports = [origem]
        for (voo, next_dest) in path:
            airports.append(next_dest)

        # Determina os aeroportos de escala (excluindo origem e destino)
        layovers = airports[1:-1] if len(airports) > 2 else []

        # Exibe o número da rota e o itinerário
        print(f"{idx}.")
        print(f"  Itinerário: {' -> '.join(airports)}")
        if layovers:
            print(f"  Aeroportos de Escala: {', '.join(layovers)}")
        else:
            print(f"  Aeroportos de Escala: Nenhum (Voo Direto)")

        # Exibe os voos da rota
        print("  Voos:")
        for voo, _ in path:
            print(f"    - {voo['voo']}, Duração: {voo['duracao']}")
        print("")  # Linha em branco para separar as rotas

    # Solicita ao usuário que escolha uma rota
    while True:
        try:
            escolha = int(input(f"Escolha uma rota (1-{len(paths)}): "))
            if 1 <= escolha <= len(paths):
                rota_escolhida = paths[escolha - 1]
                print(f"\nVocê escolheu a Rota {escolha}:")
                
                # Reconstrói a lista de aeroportos para a rota escolhida
                airports = [origem]
                for (voo, next_dest) in rota_escolhida:
                    airports.append(next_dest)
                
                print(f"  Itinerário: {' -> '.join(airports)}")
                layovers = airports[1:-1] if len(airports) > 2 else []
                if layovers:
                    print(f"  Aeroportos de Escala: {', '.join(layovers)}")
                else:
                    print(f"  Aeroportos de Escala: Nenhum (Voo Direto)")

                print("  Voos:")
                for voo, _ in rota_escolhida:
                    print(f"    - {voo['voo']}, Duração: {voo['duracao']}")
                print("")  # Linha em branco

                break
            else:
                print(f"Por favor, insira um número entre 1 e {len(paths)}.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    # Retorna a rota escolhida para ações futuras
    return rota_escolhida

# Função para reservar um assento específico (já atualizada anteriormente)
def reservar_assento(rotas, origem, destino, voo_numero, assento_cod):
    """
    Reserva um assento específico em um voo.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas.
    - origem (str): Código do aeroporto de origem.
    - destino (str): Código do aeroporto de destino.
    - voo_numero (str): Identificador do voo.
    - assento_cod (str): Código do assento a ser reservado.

    Retorna:
    - str: Mensagem indicando o resultado da operação.
    """
    # Verifica se a origem existe no grafo de rotas
    if origem not in rotas:
        return f"Origem '{origem}' não encontrada."

    # Verifica se o destino existe a partir da origem
    if destino not in rotas[origem]:
        return f"Destino '{destino}' não encontrado a partir de '{origem}'."

    # Itera sobre os voos do destino para encontrar o voo específico
    for voo in rotas[origem][destino]:
        if voo['voo'] == voo_numero:
            # Verifica se o voo está disponível
            if not voo['disponivel']:
                return f"O voo '{voo_numero}' não está disponível."

            # Itera sobre os assentos para encontrar o assento específico
            for assento in voo['assentos']:
                if assento['cod'] == assento_cod:
                    if assento['disponivel']:
                        # Reserva o assento
                        assento['disponivel'] = False
                        return f"Assento '{assento_cod}' reservado com sucesso no voo '{voo_numero}'."
                    else:
                        return f"Assento '{assento_cod}' já está reservado no voo '{voo_numero}'."

            # Se o assento não foi encontrado
            return f"Assento '{assento_cod}' não encontrado no voo '{voo_numero}'."

    # Se o voo não foi encontrado
    return f"Voo '{voo_numero}' não encontrado de '{origem}' para '{destino}'."

# Exemplo de Uso Interativo
if __name__ == "__main__":
    print("Bem-vindo ao Sistema de Rotas Aéreas!\n")
    # Solicita ao usuário a origem e o destino
    origem_input = input("Digite o código do aeroporto de origem: ").strip().upper()
    destino_input = input("Digite o código do aeroporto de destino: ").strip().upper()

    # Chama a função para listar rotas possíveis
    rota_selecionada = listar_rotas_possiveis(rotas3, origem_input, destino_input)

    if rota_selecionada:
        print("Você pode prosseguir para reservar assentos na rota escolhida.")
        # Exemplificação de reserva para cada voo na rota escolhida
        for voo, _ in rota_selecionada:
            print(f"\nReservando assentos para o {voo['voo']} (Duração: {voo['duracao']})")
            print("Assentos disponíveis:")
            assentos_disponiveis = [assento['cod'] for assento in voo['assentos'] if assento['disponivel']]
            if not assentos_disponiveis:
                print("  Nenhum assento disponível neste voo.")
                continue
            for assento in assentos_disponiveis:
                print(f"  - {assento}")

            # Verifica se o assento está disponível
            assento_found = False
            while not assento_found:
                assento_escolhido = input("Digite o código do assento que deseja reservar (ou 'pular' para o próximo voo): ").strip().upper()
                if assento_escolhido.lower() == 'pular':
                    break
                
                for assento in voo['assentos']:
                    if assento['cod'] == assento_escolhido and assento['disponivel']:
                        assento_found = True
                        assento['disponivel'] = False
                        print(f"Assento '{assento_escolhido}' reservado com sucesso no voo '{voo['voo']}'.")
                        break
                if not assento_found:
                    print(f"Assento '{assento_escolhido}' não encontrado ou já reservado.")
