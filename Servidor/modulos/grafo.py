import json
from pathlib import Path
import threading
import logging

ARQUIVO_GRAFO= "data/grafo_rotas.json"

# Bloqueio para sincronização de acesso aos arquivos JSON
lock = threading.Lock()

def salvar_grafo(rotas, arquivo):
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

def carregar_grafo(arquivo):
    """
    Carrega o grafo de rotas a partir de um arquivo JSON.
    
    Parâmetros:
    - arquivo (str): Caminho relativo ou absoluto para o arquivo JSON.
    
    Retorna:
    - dict: Grafo de rotas carregado.
    - None: Se ocorrer um erro.
    """
    # caminho_grafo = Path(__file__).parent.parent / arquivo
    # if not caminho_grafo.exists():
    #     logging.error(f"Arquivo '{caminho_grafo}' não encontrado.")
    #     return {}
    try:
        with lock:
            with open(arquivo, 'w', encoding='utf-8') as g:
                rotas = json.load(g)
        #logging.debug(f"Grafo carregado com sucesso a partir de '{caminho_grafo}'.")
        return rotas
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar o arquivo.")
        return {}
    except Exception as e:
        logging.error(f"Erro ao carregar o grafo: {e}")
        return {}