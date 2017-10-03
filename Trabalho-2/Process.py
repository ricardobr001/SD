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
import os

# Definindo um processo
class Processo:

    # Um processo tem um clock do processo, um id, um incremento de clock do processo
    # um vetor de acks e um vetor com as mensagens
    def __init__(self, incremento_clock, id):
        self.clock_processo = incremento_clock
        self.id = id
        self.incremento_clock = incremento_clock
        self.ok = 0
        self.vetor_msg = []
        self.usando_recurso = False
        self.requisitando_recurso = False

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
            if (int(self.vetor_msg[0].id) == int(self.vetor_ok[i].id)) & (self.vetor_ok[i].n_acks == 3):
                self.remove_msg(self.vetor_ok[i])

    # Definição do método que recebe mensagem
    def recebe_msg(self, msg):

        # Se o processo não estiver usando o recurso, e nem pretende utilizá-lo
        if not (self.usando_recurso | self.requisitando_recurso):

            # Envia um ok ao remetente
            self.envia_ok(msg.id_processo, True)

        # Caso contrário, o recurso está sendo utilizado, se estiver na região crítica
        elif self.usando_recurso:

            # Inserimos ela na fila de mensagens
            self.vetor_msg.insert(len(self.vetor_msg), msg)

            # Ordenamos o vetor pelo id da mensagem, depois pelo clock
            self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_id)
            self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_clock)

            # Respondemos ao remetente que ele deve esperar
            self.envia_ok(msg.id_processo, False)

        # Caso contrário, o recurso pode ser usado futuramente pelo receptor
        elif self.requisitando_recurso:
            # Se a requisição for do proprio processo, o vetor estará vazio, portanto ele insere a propria requisição
            if not self.vetor_msg:
                self.vetor_msg.insert(len(self.vetor_msg), msg)

            elif msg.clock_msg < self.vetor_msg[0].clock_msg:
                self.envia_ok(msg.id, True)
            else:
                self.envia_ok(msg.id, False)

                # Inserimos a requisição no vetor
                self.vetor_msg.insert(len(self.vetor_msg), msg)

                # Ordenamos o vetor pelo id da mensagem, depois pelo clock
                self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_id)
                self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_clock)

            # Verificando o clock da mensagem
            # if msg.clock_msg > self.clock_processo:
            #     self.clock_processo = msg.clock_msg + 1



            # print 'Mensagem recebida:', msg.msg

            # print '\n\nclock\tid\tpos\tconteudo'
            # for index in range(len(self.vetor_msg)):
            #     print self.vetor_msg[index].clock_msg,'\t',self.vetor_msg[index].id,'\t',index,'\t',self.vetor_msg[index].msg

            # ack = Ack(msg.id)
            # self.verifica_subir()
            # return ack

    # Definição do método que busca um id no vetor de mensagens
    def busca_id_processo(self, id):

        # Se o vetor tiver vazio, retorna -1
        if not self.vetor_msg:
            return -1

        # Se encontrar o id, retorna sua posição
        for i in range(len(self.vetor_msg)):
            if (id == self.vetor_msg[i].id):
                return i

        # Se não encontrar o id, retorna -1
        return -1

    # Definição do método que recebe um ok
    def recebe_ok(self, msg):

        # Se a mensagem, for um ok de permissão
        if msg.recurso:

            self.ok += 1

            # Se atingir 3 oks, usa o recurso e remove a requisição da lista e ostenta ok
            if (self.ok == 3)
                self.usa_recurso()
                self.remove_msg()


    # Definição do método que requisita o recurso
    def requisita_recurso(self):

        self.requisitando_recurso = True
        self.ok = 1
        self.envia_msg()

    # Definição do método que remove uma mensagem e seus acks das listas
    def remove_msg(self):

        # Removendo a minha requisição, que é a primeira
        del self.vetor_msg[0]
        self.ok = 0

        # Aqui começa a ostentação
        while (not vetor_msg):
            self.envia_ok(self.vetor_msg[0].id_processo, True)
            del vetor_msg[0]

            # Acabo a ostentação
            # if (self.vetor_msg[i].id_processo == self.id):
            #     break


    # Definição do método que simula o uso de um recurso
    def usa_recurso(self):
        print 'Processo', self.id, 'usando o recurso'
        self.usando_recurso = True
        self.requisitando_recurso = False

        time.sleep(5)

        print 'Processo', self.id, 'terminou de usar o recurso'
        self.usando_recurso = False



    # Definição do método para criar uma mensagem
    def cria_msg(self):
        clock_msg = self.clock_processo                 # Criando o clock da mensagem
        mensagem = Mensagem(clock_msg, str(self.clock_processo) + str(self.id), self.id)

        return mensagem

    # Definição do método que envia ok ao remetente
    def envia_ok(self, id, recurso):

        if not recurso:
            print 'Permissão negada ao processo', id
        else:
            print 'Enviando ok ao processo:', id
        # print 'Ok do recurso:', recurso
        # print type(id)

        # Abrindo o socket
        meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 25000 + id)
        meu_socket.connect(server_address)

        # print 'socket criado e conectado'

        # Enviando o ok para o remetente
        ok = Ok(recurso)
        ok_codificado = pickle.dumps(ok)
        meu_socket.send(ok_codificado)
        meu_socket.close()
        # print 'OK enviado'

    # Definição do método que envia uma mensagem
    def envia_msg(self):

        # Gera uma mensagem aleatória
        mensagem = self.cria_msg()

        # print 'Enviando solicitação do recurso:', mensagem.nome_recurso

        # Enviando a mensagem para todas as portas
        for i in range(0,3):

            # Abrindo o socket
            meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 25000 + i)
            meu_socket.connect(server_address)

            # Enviando a mensagem
            mensagem_codificada = pickle.dumps(mensagem)
            meu_socket.send(mensagem_codificada)
            meu_socket.close()

# Definindo uma mensagem
class Mensagem:
    def __init__(self, clock_msg, id, id_processo):
        self.clock_msg = clock_msg
        self.id = id
        self.id_processo = id_processo

    def get_clock(self):
        return self.clock_msg

    def get_id(self):
        return self.id

# Definindo um ok
class Ok:
    def __init__(self, recurso, id):
        self.recurso = recurso
        self.id = id

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

    while True:
        time.sleep(randint(1,10))

        try:
            if not (processo.requisitando_recurso | processo.usando_recurso):
                processo.requisita_recurso()

        except Exception as e:
        	# print 'Erro ao enviar', e
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

# Definindo a thread do clock
def thread_clock():
    global processo

    while True:
        processo.incrementa_clock()

        time.sleep(2)

processo = Processo(randint(0,9), int(sys.argv[2]))

# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
    thread.start_new_thread(thread_gera, ())
    thread.start_new_thread(thread_clock, ())

    signal.pause()

if __name__ == "__main__":
    sys.exit(main())
