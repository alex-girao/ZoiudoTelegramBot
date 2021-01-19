import requests
from datetime import datetime,timezone,timedelta

class TelegramPontoBot:
  def __init__(self):
    token = "MY_TOKEN"
    self.msgHoraExataEnviada = False
    self.msgNoPrazoEnviada = False
    self.msgPerdidoEnviada = False
    self.url_base = f'https://api.telegram.org/bot{token}/'
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
    hora = self.hora_atual()
    # ta na hora
    if hora in ['08:00','12:00','13:00','17:00'] and not self.msgHoraExataEnviada:
      self.responder('Oh u PONTO!', chat_id)
      self.zerarVariaveisMsg()
      self.msgHoraExataEnviada = True
    # falta pouco
    if hora in ['08:12','12:12','13:12','17:12'] and not self.msgNoPrazoEnviada:
      self.responder('Borá mah, ainda da tempo de bater', chat_id)
      self.zerarVariaveisMsg()
      self.msgNoPrazoEnviada = True
    # perdeu
    if hora in ['08:15','12:15','13:15','17:15'] and not self.msgPerdidoEnviada:
      self.responder('Quem bateu, bateu, quem não bateu, não bate mais...', chat_id)
      self.zerarVariaveisMsg()
      self.msgPerdidoEnviada = True

  def hora_atual(self):
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data_e_hora_atuais = datetime.now()
    data_hora_brasilia = data_e_hora_atuais.astimezone(fuso_horario)
    return data_hora_brasilia.strftime('%H:%M')
  
  def zerarVariaveisMsg(self):
    self.msgHoraExataEnviada = False
    self.msgNoPrazoEnviada = False
    self.msgPerdidoEnviada = False
    
  def IniciarPonto(self):
    while True:
      self.verificaPonto('ID_GROUP')

# Iniciando o bot
bot = TelegramPontoBot()

#FC
grupo = 'ID_GROUP'
bot.responder('E ai negada!', grupo)
bot.IniciarPonto()
