from modulos.msg_utils import enviar_mensagem, receber_mensagem
from modulos.usuarios import autenticar_usuario


def server_login(client_sock, dados, arquivo):
    user_id = dados.get('id')
    user_senha = dados.get('senha')
    sucesso = autenticar_usuario(user_id, user_senha, arquivo)
    if sucesso:
        enviar_mensagem(client_sock, 'LOGIN_RESPOSTA', {'sucesso': sucesso})
        return True
    else:
        enviar_mensagem(client_sock, 'LOGIN_RESPOSTA', {'sucesso': False})
        return False
   
        