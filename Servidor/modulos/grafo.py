import json
import threading

lock = threading.RLock()

ARQUIVO_GRAFO= "data/grafo_rotas.json"

# Bloqueio para sincronização de acesso aos arquivos JSON
lock = threading.Lock()

def salvar_grafo_old(rotas, arquivo):
    """
    Salva o grafo de rotas em um arquivo JSON.
    
    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    - arquivo (str): Caminho relativo ou absoluto para o arquivo JSON.
    
    Retorna:
    - None
    """
    # caminho_grafo = Path(__file__).parent.parent / arquivo
    try:
        with lock:
            with open(arquivo, 'w', encoding='utf-8') as g:
                json.dump(rotas, g, ensure_ascii=False, indent=4)
        print(f"Grafo salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar o grafo: {e}")


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