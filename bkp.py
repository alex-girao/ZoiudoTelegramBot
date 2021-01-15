import requests
import json
from datetime import datetime,timezone,timedelta

class TelegramBot:
  def __init__(self):
    token = '1541293521:AAESNWV-b0pOJPdCTawrBGVUoRvo8Q3elAs'
    self.url_base = f'https://api.telegram.org/bot{token}/'
  # Iniciar o bot
  def Iniciar(self):
    update_id = None
    while True:
      # pegando as ultimas mensagens
      atualizacao = self.obter_mensagens(update_id)
      # extraindo as mensagens
      mensagens = atualizacao['result']
      # caso existam mensagens
      if mensagens:
        # percorrendo as mesagens
        for mensagem in mensagens:
          # reculperando pelo update_id
          update_id = mensagem['update_id']
          # pegando o ID de quem enviou, para responder
          chat_id = mensagem['message']['from']['id']
          #criar resposta
          resposta = self.criar_resposta()
          self.responder(resposta, chat_id)
          # verificando o Ponto
          self.verificaPonto(chat_id)
  # Obter mensagens
  def obter_mensagens(self,update_id):
    print('obterMensagens')
    # pegando as mensagens a cada timeout=segundos
    link_requisicao = f'{self.url_base}getUpdates?timeout=100'
    # se houver update_id
    if update_id:
      #pegando a ultima mensagem
      link_requisicao = f'{link_requisicao}&offset={update_id+1}'
    resultado = requests.get(link_requisicao)
    print('-- resultado: ')
    print(json.loads(resultado.content))
    print('== resultado: ')
    return json.loads(resultado.content)
  # Crirar uma resposta
  def criar_resposta(self):
    return 'Olá Bem vindo ao nosso grupo!'
  # Responder
  def responder(self, resposta, chat_id):
    print('responder')
    print(resposta)
    print(chat_id)
    print('==========')
    # enviar
    link_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
    requests.get(link_envio)
  # aviso do ponto
  def verificaPonto(self, chat_id):
    print('verificaPonto')
    hora = self.hora_atual()
    # ta na hora
    if hora in ['08:00','12:00','13:00','17:00','16:29']:
      self.responder('Oh u PONTO!', chat_id)
    # falta pouco
    if hora in ['08:12','12:12','13:12','17:12','16:30']:
      self.responder('Borá mah, ainda da tempo de bater', chat_id)
    # perdeu
    if hora in ['08:15','12:15','13:15','17:15','16:31']:
      self.responder('Quem bateu, bateu, quem não bateu, não bate mais...', chat_id)

  def hora_atual(self):
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data_e_hora_atuais = datetime.now()
    data_hora_brasilia = data_e_hora_atuais.astimezone(fuso_horario)
    return data_hora_brasilia.strftime('%H:%M')
    
  def IniciarPonto(self):
    while True:
      self.verificaPonto('-382360320')

# Iniciando o bot
bot = TelegramBot()
bot.IniciarPonto()
