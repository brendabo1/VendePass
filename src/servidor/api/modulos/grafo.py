import json
import threading

lock = threading.RLock()


# Bloqueio para sincronização de acesso aos arquivos JSON
lock = threading.Lock()

def salvar_grafo(rotas, arquivo):
    """
    Salva o grafo de rotas em um arquivo JSON.
    
    Parâmetros:
    - rotas (dict): O grafo de rotas a ser salvo.
    """
    with lock:  # Garantir que apenas um thread escreva no arquivo por vez
        with open(arquivo, 'w') as f:
            json.dump(rotas, f, indent=4)

def carregar_grafo(arquivo):
    """
    Carrega o grafo de rotas a partir de um arquivo JSON.
    
    Parâmetros:
    - arquivo (str): Caminho relativo ou absoluto para o arquivo JSON.
    
    Retorna:
    - dict: Grafo de rotas carregado.
    - None: Se ocorrer um erro.
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