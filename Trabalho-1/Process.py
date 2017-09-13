#coding: utf-8
#python 2.7

from random import *
import socket
import string
import thread
import pickle
import sys
import signal
import time
import struct
import operator

# Definindo um processo
class Processo:
    # Um processo tem um clock do processo, um id, um incremento de clock do processo
    # um vetor de acks e um vetor com as mensagens
    def __init__(self, incremento_clock, id):
        self.clock_processo = incremento_clock
        self.id = id # os.getpid()
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

            # Se tiver 3 acks e a mensagem, sobe o ack para a aplicação
            self.verifica_subir()


                # self.vetor_ack = sorted(self.vetor_ack, key = Ack.get_id) ################ Testando ordenação de objetos

        # Se não encontramos o ack
        if not flag:

            # inserimos o novo ack no vetor de acks
            ack.n_acks += 1
            self.vetor_ack.insert(len(self.vetor_ack), ack)

        print '\n\nid\tacks\tpos'
        for index in range(len(self.vetor_ack)):
            print self.vetor_ack[index].id,'\t',self.vetor_ack[index].n_acks,'\t',index


                    #subir(self.vetor_ack[i])

    def verifica_subir(self):

        for i in range(len(self.vetor_ack)):
            if int(self.vetor_msg[0].id) == int(self.vetor_ack[i].id) & self.vetor_ack[i].n_acks == 3:
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
            # print 'tipo do vetor'
            # print self.vetor_msg
            self.vetor_msg = sorted(self.vetor_msg, key = lambda mensagem: (Mensagem.get_clock, Mensagem.get_id))

            print '\n\nclock\tid\tpos\tconteudo'
            for index in range(len(self.vetor_msg)):
                print self.vetor_msg[index].clock_msg,'\t',self.vetor_msg[index].id,'\t',index,'\t',self.vetor_msg[index].msg

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
        # self.recebe_msg(mensagem)                           # A mensagem criada já é adicionada no vetor de mensagens
        # ack = Ack(self.id)                                  # E seu respectivo ack também é criado
        # self.recebe_ack(ack)

        return mensagem
        # print 'Clock_msg:', self.vetor_msg[0].clock_msg
        # print 'Id_mensagem:', self.vetor_msg[0].id
        # print 'Mensagem:', self.vetor_msg[0].msg,'\n'
        # print 'Id do ack:', self.vetor_ack[0].id
        # print 'Qtd de acks:', self.vetor_ack[0].n_acks,'\n'

    # Definição do método que envia uma mensagem
    def envia_msg(self):

        global PORT
        global GRUPO

        mensagem = self.cria_msg(choice(string.letters))

        infoaddr = socket.getaddrinfo(GRUPO, None)[0]

    	meu_socket = socket.socket(infoaddr[0], socket.SOCK_DGRAM)
    	ttl = struct.pack('@i', TTL)

        meu_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # Enviando a mensagem e o ack para os outros processos
        # print 'Enviando a mensagem'
        mensagem_codificada = pickle.dumps(mensagem)
        meu_socket.sendto(mensagem_codificada, (infoaddr[4][0], PORT))
        meu_socket.close()

    # Definição do método que envia um ack
    def envia_ack(self, ack):

        global PORT
        global GRUPO

        infoaddr = socket.getaddrinfo(GRUPO, None)[0]

    	meu_socket = socket.socket(infoaddr[0], socket.SOCK_DGRAM)
    	ttl = struct.pack('@i', TTL)

        meu_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # Enviando o ack
        # print 'Enviando o ack'
        ack_codificado = pickle.dumps(ack)
        meu_socket.sendto(ack_codificado, (infoaddr[4][0], PORT))
        # meu_socket.close()

    def mostra_processo(self):
        print 'clock_processo: ', self.clock_processo
        print 'id: ', self.id
        print 'incremento do clock: ', self.incremento_clock, "\n"

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

# def compara_clocks():
#     if msg1.clock_msg > msg2.clocm_msg:
#         return msg.get_clock
#     else:
#         return msg.get_id


# Definindo a thread que recebe dados
def thread_recebe():
    global processo
    global PORT
    global GRUPO

    while True:
        infoaddr = socket.getaddrinfo(GRUPO, None)[0]

        meu_socket = socket.socket(infoaddr[0], socket.SOCK_DGRAM)

        meu_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        meu_socket.bind(('0.0.0.0', PORT))

        grupo_b = socket.inet_pton(infoaddr[0], infoaddr[4][0])

        grupo_assoc = grupo_b + struct.pack('=I', socket.INADDR_ANY)
        meu_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, grupo_assoc)

        # Recebendo os dados dos outros processos e os decodifica
        data, addr = meu_socket.recvfrom(1024)
        decodificada = pickle.loads(data)

        if isinstance(decodificada, (Mensagem)):
            # print 'Recebendo mensagem da máquina', addr,'\n'
            ack = processo.recebe_msg(decodificada)
            processo.envia_ack(ack)
            # print 'mensagem'
            # print 'Clock_msg:', decodificada.clock_msg
            # print 'Id_msg:', decodificada.id
            # print 'Mensagem:', decodificada.msg

        if isinstance(decodificada, (Ack)):
            # print 'Recebendo ack da máquina', addr,'\n'
            processo.recebe_ack(decodificada)
            # print 'Ack'
            # print 'ID_Ack:', decodificada.id
            # print 'N_acks:', decodificada.n_acks

        # conn.close()

# Definindo a thread que gera as mensagens
def thread_gera():
    global processo

    while True:
        time.sleep(10)

        mensagem = processo.cria_msg(choice(string.letters))
        processo.envia_msg()

# Definindo a thread do clock
def thread_clock():
    global processo

    while True:
        processo.incrementa_clock()

        time.sleep(2)

processo = Processo(randint(0,9), sys.argv[2])
HOST = 'localhost'
GRUPO = "224.0.27.1"
TTL = 1
PORT = 15214


# Main
def main():
    PORT = sys.argv[1]
    thread.start_new_thread(thread_recebe, ())
        # thread_recebe_dados.start()
    thread.start_new_thread(thread_gera, ())
    thread.start_new_thread(thread_clock, ())

    signal.pause()

if __name__ == "__main__":
    sys.exit(main())

    # thread_gera_msg.start()
    # thread = Thread(target = minha.recebendo_dados(conn, addr))
    # thread.start()
    #thread.join()

# processo = Processo(1, "23")
# processo.envia_msg()
# processo = Processo(1, "23")
# # processo.mostra_processo()
# processo.incrementa_clock()
# # processo.mostra_processo()
# processo.cria_msg("Teste")
# #ack = Ack("23")
# #processo.recebe_ack(ack)
# # print processo.vetor_ack[0].id
# # print processo.vetor_ack[0].n_acks
# #processo.recebe_ack(ack)
# # print processo.vetor_ack[0].id
# # print processo.vetor_ack[0].n_acks
# ack_novo = Ack("12")
# processo.recebe_ack(ack_novo)
# ack_novo_3 = Ack("91")
# processo.recebe_ack(ack_novo_3)
# ack_novo_4 = Ack("17")
# processo.recebe_ack(ack_novo_4)
# # print processo.vetor_ack[0].id
# # print processo.vetor_ack[0].n_acks
# print 'id\tacks\tpos'
# for index in range(len(processo.vetor_ack)):
#     print processo.vetor_ack[index].id,'\t',processo.vetor_ack[index].n_acks,'\t',index
#
# ack_novo_5 = Ack("23")
# processo.recebe_ack(ack_novo_5)
# ack_novo_6 = Ack("23")
# processo.recebe_ack(ack_novo_6)
#
# print '\n\nid\tacks\tpos'
# for index in range(len(processo.vetor_ack)):
#     print processo.vetor_ack[index].id,'\t',processo.vetor_ack[index].n_acks,'\t',index
#
# print 'Testando rand'
# print(randint(0,9))
#
# print '\n\nTestando rand letras'
# print choice(string.letters)
