from modulos.msg_utils import enviar_mensagem, receber_mensagem
from modulos.usuarios import autenticar_usuario


def server_login(client_sock, dados, arquivo):
    user_id = dados.get('id')
    user_senha = dados.get('senha')
    usuario_autenticado = autenticar_usuario(client_sock, user_id, user_senha, arquivo)
    if usuario_autenticado:
        user_id = usuario_autenticado.get('id')
        #enviar_mensagem(client_sock, 'LOGIN_RESPOSTA', {'sucesso': user_id})
        return user_id
    else:
        #enviar_mensagem(client_sock, 'LOGIN_RESPOSTA', {'sucesso': False})
        return None
   
        