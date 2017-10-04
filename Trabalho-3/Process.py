#coding: utf-8
# python 2.7
# Desenvolvido apenas para 3 processos, rodando nas portas 25000, 25001 e 25002
# Com os IDs sendo 0, 1 e 2 respectivamente
# Executar o programa passando no argumento a porta e o seu ID
# Ex: python Process.py 25000 1
# Ou iniciar o start.py (Necessário sistema linux)


########################################################
# Nome: Leonardo Zaccarias              RA: 620491     #
# Nome: Ricardo Mendes Leal Junior      RA: 562262     #
########################################################


from random import *
import socket
import string
import thread
import pickle
import sys
import signal
import time
# import os

# Definindo um processo
class Processo:

    # Um processo tem um clock do processo, um id, um incremento de clock do processo
    # um vetor de acks e um vetor com as mensagens
    def __init__(self, incremento_clock, id):
        self.clock_processo = incremento_clock
        self.clock_eleicao = incremento_clock
        self.id = id
        self.incremento_clock = incremento_clock
        self.valentao = False
        self.ativo = True
        self.eleicao = False
        self.vetor_msg = []
        self.vetor_resposta = []
        self.coordenador_atual = 5

    def incrementa_clock(self):
        self.clock_processo += self.incremento_clock

        if not self.eleicao:
            self.clock

    # Definição do método que recebe mensagem
    def recebe_msg(self, msg):

        #verifica se é uma mensagem de coordenador eleito
        if msg.coordenador:
            self.coordenador_atual = msg.id_processo

        #se for requisição de eleição
        else:
            # verifica qual o id maior, se o recebido for maior, envia ok
            if msg.id_processo > self.id:
                self.envia_ok(msg.id_processo)
            # se o processo atual é maior, convoca eleição
            else:
                self.convoca_eleicao()

    # Definição do método que recebe um ok
    def recebe_ok(self, msg):
        if msg.flag == 'E':
            print 'Sou um bosta mermao'
        else:
            processo.coordenador_atual = msg.id

    # Definição do método para criar uma mensagem
    def cria_msg(self, flag):
        mensagem = Mensagem(self.id, flag)
        return mensagem

    # Definição do método que envia ok ao remetente
    def envia_ok(self, id):

        # Abrindo o socket
        meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 25000 + id)
        meu_socket.connect(server_address)

        # Enviando o ok para o remetente
        ok = Ok(id)
        ok_codificado = pickle.dumps(ok)
        meu_socket.send(ok_codificado)
        meu_socket.close()

    # Definição do método que envia uma mensagem
    def envia_msg(self, mensagem):

        #se for uma mensagem de coordenador envia para todos os processos
        if mensagem.flag == 'C':
            i = 0
        #se for eleicao envia apenas para os maiores
        elif mensagem.flag == 'E':
            i = self.id+1
        else:
            i = mensagem.flag

        # Enviando a mensagem para processos
        while i < 5:
            # Abrindo o socket
            meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 25000 + i)
            meu_socket.connect(server_address)

            # Enviando a mensagem
            mensagem_codificada = pickle.dumps(mensagem)
            meu_socket.send(mensagem_codificada)
            meu_socket.close()

            i += 1


    def convoca_eleicao(self):
        # cria uma mensagem do tipo eleicao
        mensagem = self.cria_msg(self.id, 'E')

        #envia mensagem de eleicao
        self.envia_msg(mensagem)

        #Timeout de resposta


        #Se der timeout, envia mensagem de coordenador
        mensagem.set_coordenador()
        self.envia_msg(mensagem)

# Definindo uma mensagem
class Mensagem:
    def __init__(self, id_processo, flag):
        self.id_processo = id_processo
        self.flag = flag    # E = mensagem de eleição, C = mensagem de definição de coordenador
                            # T = e a mensagem de teste para ver se o coordenador vive

    def set_coordenador(self):
        self.flag = 'C'

# Definindo um ok
class Ok:
    def __init__(self, id, flag):
        self.id = id
        self.flag = flag # E = Ok pra eleição T = ack da msg enviado ao coordenador


# Definindo a thread que recebe dados
def thread_recebe():
    global processo

    while True:
        serverPort = int(sys.argv[1])

        # Criando o socket
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:

            # O socket fica ouvindo o meio
            serverSocket.bind(('',serverPort))
            serverSocket.listen(1)

            while True:

                # Se o processo estiver marcado como inativo, dorme
                if not processo.ativo:
                    time.sleep(50000)

                # Aceita uma conexão
                connectionSocket, addr = serverSocket.accept()

                try:

                    # Recebe os dados e os decodifica
                    data = connectionSocket.recv(1024)
                    decodificada = pickle.loads(data)

                    if isinstance(decodificada, (Mensagem)):
                        processo.recebe_msg(decodificada)

                    elif isinstance(decodificada, (Ok)):
                        processo.recebe_ok(decodificada)

                except Exception as e:
                    print 'Erro ao receber:', e
                    # exc_type, exc_obj, exc_tb = sys.exc_info()
                    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno)

        except Exception as e:
            print 'Erro ao abrir o socket:', e
            time.sleep(5)

# Definindo a thread que gera as mensagens
def thread_gera():
    global processo

    time.sleep(processo.id * 2)

    while True:
        try:
            # If para o coordenador nao mandar msg pra ele msm
            if processo.coordenador_atual != processo.id & processo.ativo:
                # Envia msg pro coordenador
                mensagem = processo.cria_msg(processo.id, 'T')
                processo.coordenador_atual = -1
                processo.envia_msg(mensagem)
                # espera 1 segundo de time out para ver se recebe ok do coordenador
                time.sleep(1)
                if processo.coordenador_atual == -1:
                    processo.convoca_eleicao()

        except Exception as e:
        	print 'Erro ao enviar', e
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)

        # O processo ira requisitar o recurso em tempos aleatórios
        time.sleep(9)

# Definindo a thread do clock
def thread_clock():
    global processo

    while True:
        processo.incrementa_clock()

        time.sleep(2)

# Definindo a thread que detecta Timeout
def thread_timeout():
    global processo

    while True:
        if processo.clock_processo - processo.clock_eleicao > 20:
            print 'timeout!!!'

# Definindo a thread que interage com o usuário
def thread_input():
    global processo

    while True:
        entrada = raw_input()

        if entrada == 'kill':
            processo.ativo = False

processo = Processo(randint(0,9), int(sys.argv[2]))
print 'Processo:', sys.argv[2]

# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
    thread.start_new_thread(thread_gera, ())
    thread.start_new_thread(thread_clock, ())

    signal.pause()

if __name__ == "__main__":
    sys.exit(main())
