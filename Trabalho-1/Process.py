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
        self.id = id
        self.incremento_clock = incremento_clock
        self.vetor_ack = []
        self.vetor_msg = []

    def incrementa_clock(self):
        self.clock_processo += self.incremento_clock

    # Definiçaõ do método que recebe um ack
    def recebe_ack(self, ack):

        # flag que marca se encontrou ou não determinado ack
        flag = False

        # Se o ack estiver na lista de acks
        for i in range(len(self.vetor_ack)):
            if ack.id == self.vetor_ack[i].id:

                flag = True                         # Marcamos na flag que encontramos o ack

                self.vetor_ack[i].n_acks += 1       # Contamos que recebemos mais um ack
                print 'Ack recebido:', ack.id

            # Se tiver 3 acks e a mensagem, sobe o ack para a aplicação
            self.verifica_subir()

        # Se não encontramos o ack
        if not flag:

            # inserimos o novo ack no vetor de acks
            print 'Ack recebido:', ack.id
            ack.n_acks += 1
            self.vetor_ack.insert(len(self.vetor_ack), ack)

        # print '\n\nid\tacks\tpos'
        # for index in range(len(self.vetor_ack)):
        #     print self.vetor_ack[index].id,'\t',self.vetor_ack[index].n_acks,'\t',index

    # Definição do método que verifica se pode subir a mensagem
    def verifica_subir(self):

        # print 'id_msg\tid_ack\tn_acks'
        for i in range(len(self.vetor_ack)):

            # Se tiver 3 acks e existir a mensagem, a remove
            if (int(self.vetor_msg[0].id) == int(self.vetor_ack[i].id)) & (self.vetor_ack[i].n_acks == 3):
                self.remove_msg(self.vetor_ack[i])

    # Definição do método que recebe mensagem
    def recebe_msg(self, msg):

        # Se está mensagem não estiver no vetor
        if not msg in self.vetor_msg:

            # Verificando o clock da mensagem
            if msg.clock_msg > self.clock_processo:
                self.clock_processo = msg.clock_msg + 1

            # Inserimos ela no vetor de mensagens e ordenamos o vetor
            self.vetor_msg.insert(len(self.vetor_msg), msg)

            # Ordenamos o vetor pelo id da mensagem, depois pelo clock
            self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_id)
            self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_clock)

            print 'Mensagem recebida:', msg.msg

            # print '\n\nclock\tid\tpos\tconteudo'
            # for index in range(len(self.vetor_msg)):
            #     print self.vetor_msg[index].clock_msg,'\t',self.vetor_msg[index].id,'\t',index,'\t',self.vetor_msg[index].msg

            ack = Ack(msg.id)
            self.verifica_subir()
            return ack

        # Caso contrário não fazemos nada

    # Definição do método que remove uma mensagem e seus acks das listas
    def remove_msg(self, ack):

        print 'subiu para aplicação a mensagem:', '"',self.vetor_msg[0].msg,'"'
        del self.vetor_msg[0]
        self.vetor_ack.remove(ack)
        # break


    # Definição do método para criar uma mensagem
    def cria_msg(self, msg):
        clock_msg = self.clock_processo                 # Criando o clock da mensagem
        mensagem = Mensagem(clock_msg, msg, str(self.clock_processo) + str(self.id))

        return mensagem

    # Definição do método que envia uma mensagem
    def envia_msg(self):

        # Gera uma mensagem aleatória
        mensagem = self.cria_msg(choice(string.letters))

        print 'Enviando a mensagem:', mensagem.msg

        # Enviando a mensagem para todas as portas
        for i in range(0,3):

            # Abrindo o socket
            meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 25000 + i)
            meu_socket.connect(server_address)

            # Enviando a mensagem e o ack para os outros processos
            mensagem_codificada = pickle.dumps(mensagem)
            meu_socket.send(mensagem_codificada)
            meu_socket.close()

    # Definição do método que envia um ack
    def envia_ack(self, ack):

        # Enviando para todas as portas
        for i in range(0,3):

            # Abrindo o socket
            meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 25000 + i)
            meu_socket.connect(server_address)

            # Enviando o ack
            ack_codificado = pickle.dumps(ack)
            meu_socket.send(ack_codificado)
            meu_socket.close()

# Definindo uma mensagem
class Mensagem:
    def __init__(self, clock_msg, msg, id):
        self.clock_msg = clock_msg
        self.id = id
        self.msg = msg

    def get_clock(self):
        return self.clock_msg

    def get_id(self):
        return self.id

# Definindo um ack
class Ack:
    def __init__(self, id):
        self.id = id
        self.n_acks = 0

    def get_id(self):
        return self.id

# Definindo a thread que recebe dados
def thread_recebe():

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

                try:

                    # Recebe os dados e os decodifica
                    data = connectionSocket.recv(1024)
                    decodificada = pickle.loads(data)

                    if isinstance(decodificada, (Mensagem)):
                        ack = processo.recebe_msg(decodificada)
                        processo.envia_ack(ack)

                    elif isinstance(decodificada, (Ack)):
                        processo.recebe_ack(decodificada)

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

    while True:
        time.sleep(10)

        try:
            processo.envia_msg()
        except Exception as e:
        	print 'Erro ao enviar', e
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)

# Definindo a thread do clock
def thread_clock():
    global processo

    while True:
        processo.incrementa_clock()

        time.sleep(2)

processo = Processo(randint(0,9), sys.argv[2])

# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
    thread.start_new_thread(thread_gera, ())
    thread.start_new_thread(thread_clock, ())

    signal.pause()

if __name__ == "__main__":
    sys.exit(main())
