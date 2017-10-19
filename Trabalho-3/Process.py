#coding: utf-8
# python 2.7
# Desenvolvido apenas para 5 processos, rodando nas portas 25000, 25001, 25002, 25003 e 25004
# Com os IDs sendo 0, 1, 2, 3 e 4 respectivamente
# Executar o programa passando no argumento a porta e o seu ID
# Ex: python Process.py 25000 0
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
        self.id = id
        self.incremento_clock = incremento_clock
        self.ativo = True
        self.eleicao = False
        self.coordenador_atual = 4

    def incrementa_clock(self):
        self.clock_processo += self.incremento_clock

    # Definição do método que recebe mensagem
    def recebe_msg(self, msg):

        # Verifica se é uma mensagem de coordenador eleito
        if msg.flag == 'C':
            self.eleicao = False

            self.coordenador_atual = msg.id_processo

        # Se for mensagem de teste, responde com ok, que o coordenador está vivo
        elif msg.flag == 'T':
            ok = self.cria_ok(self.id, msg.flag)
            self.envia_ok(msg.id_processo, ok)

        # Se for requisição de eleição
        elif msg.flag == 'E':
            self.eleicao = True

            # Verifica qual o id maior, se o recebido for maior, envia ok
            if msg.id_processo < self.id:
                ok = self.cria_ok(self.id, msg.flag)
                self.envia_ok(msg.id_processo, ok)
                self.convoca_eleicao()

    # Definição do método que recebe um ok
    def recebe_ok(self, msg):

        # Se for um ok de eleição, eu perdi
        if msg.flag == 'E':
            self.eleicao = False
            print 'Perdi a eleição =('
            self.coordenador_atual = -2

        # Se for ok do coordenador, o coordenador está vivo
        else:
            processo.coordenador_atual = msg.id_processo
            print 'Coordenador ', processo.coordenador_atual, 'está operante'

    # Definição do método para criar uma mensagem
    def cria_msg(self, id, flag):
        mensagem = Mensagem(id, flag)
        return mensagem

    # Definição do método que cria um ok
    def cria_ok(self, id, flag):
        ok = Ok(id, flag)
        return ok

    # Definição do método que envia ok ao remetente
    def envia_ok(self, id, ok):

        print 'Ok:',ok.flag,'\tPara ->',id

        # Abrindo o socket
        meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 25000 + id)
        meu_socket.connect(server_address)

        # Enviando o ok para o remetente
        ok_codificado = pickle.dumps(ok)
        meu_socket.send(ok_codificado)
        meu_socket.close()

    # Definição do método que envia uma mensagem
    def envia_msg(self, mensagem):

        # Se for uma mensagem de coordenador envia para todos os processos
        if mensagem.flag == 'C':
            self.eleicao = False
            i = 0

        # Se for eleicao envia apenas para os maiores
        elif mensagem.flag == 'E':
            self.eleicao = True

            i = self.id+1

        # Se for um teste de coordenador
        elif mensagem.flag == 'T':
            i = mensagem.coordenador_atual
            print 'Enviando mensagem para o coordenador (', i, ')'

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

            if mensagem.flag == 'T':
                i = 54454

            i += 1


    def convoca_eleicao(self):


        # Cria uma mensagem do tipo eleicao
        mensagem = self.cria_msg(self.id, 'E')

        self.coordenador_atual = -1
        self.eleicao = True

        # Envia mensagem de eleicao
        self.envia_msg(mensagem)

        # Timeout de resposta de 1 segundo
        i = 1
        while i >= 0:

            i -= 0.1

        # Se o coordenador atual continuar -1, serei o novo coordenador
        if self.coordenador_atual == -1:
            self.coordenador_atual = self.id
            mensagem.flag = 'C'

            #Se der timeout, envia mensagem de coordenador
            self.envia_msg(mensagem)
            self.eleicao = False

# Definindo uma mensagem
class Mensagem:
    def __init__(self, id_processo, flag):
        self.id_processo = id_processo
        self.flag = flag    # E = mensagem de eleição, C = mensagem de definição de coordenador
                            # T = e a mensagem de teste para ver se o coordenador vive
        self.coordenador_atual = -1

    def set_coordenador(self):
        self.flag = 'C'

# Definindo um ok
class Ok:
    def __init__(self, id_processo, flag):
        self.id_processo = id_processo
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

                # Aceita uma conexão
                connectionSocket, addr = serverSocket.accept()

                # Se o processo estiver marcado como inativo, dorme
                if not processo.ativo:
                    time.sleep(50000)

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

    time.sleep(processo.id * 3 + 3)

    while True:
        try:
            # Se o processo estiver marcado como inativo, dorme
            if not processo.ativo:
                time.sleep(50000)

            # If para o coordenador nao mandar msg pra ele msm
            if (processo.coordenador_atual != processo.id) & processo.ativo & (not processo.eleicao):

                mensagem = processo.cria_msg(processo.id, 'T')
                mensagem.coordenador_atual = processo.coordenador_atual
                processo.coordenador_atual = -1
                processo.envia_msg(mensagem)

                # Espera 1 segundo de time out para ver se recebe ok do coordenador
                time.sleep(1)
                if processo.coordenador_atual == -1:
                    processo.convoca_eleicao()

        except Exception as e:
        	print 'Erro ao enviar', e
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)

        # O processo ira requisitar o recurso em tempos aleatórios
        time.sleep(15)

# Definindo a thread que interage com o usuário
def thread_input():
    global processo

    while True:
        entrada = raw_input()

        if entrada == 'kill':
            processo.ativo = False

        print 'Morri x.x'

processo = Processo(randint(0,9), int(sys.argv[2]))
print 'Processo:', sys.argv[2]

# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
    thread.start_new_thread(thread_gera, ())
    thread.start_new_thread(thread_input, ())

    signal.pause()

if __name__ == "__main__":
    sys.exit(main())
