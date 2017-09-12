#coding: utf-8
#python 2.7

from socket import *
from random import *
import string
import thread
import pickle

HOST = 'localhost'
PORTS = [25000, 25001, 25002]

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

                if self.vetor_ack[i].n_acks != 3:
                    self.vetor_ack[i].n_acks += 1       # Contamos que recebemos mais um ack

                # Se tiver 3 acks e a mensagem, sobe o ack para a aplicação
                if self.vetor_ack[i].n_acks == 3:
                    print 'entrou no ifzera'
                    self.remove_msg(self.vetor_ack[i])
                    break

                # self.vetor_ack = sorted(self.vetor_ack, key = Ack.get_id) ################ Testando ordenação de objetos

        # Se não encontramos o ack
        if not flag:

            # inserimos o novo ack no vetor de acks
            ack.n_acks += 1
            self.vetor_ack.insert(len(self.vetor_ack), ack)


                    #subir(self.vetor_ack[i])

    # Definição do método que recebe mensagem
    def recebe_msg(self, msg):

        # Se está mensagem não estiver no vetor
        if not msg in self.vetor_msg:

            # Inserimos ela no vetor de mensagens e ordenamos o vetor
            self.vetor_msg.insert(len(self.vetor_msg), msg)
            # print 'tipo do vetor'
            # print self.vetor_msg
            self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_clock)

        # Caso contrário não fazemos nada

    # Definição do método que remove uma mensagem e seus acks das listas
    def remove_msg(self, ack):

        # Primeiramente andamos a lista procurando se a mensagem com o respectivo id está no vetor de mensagens
        for i in range(len(self.vetor_ack)):

            # Se estiver, removemos ambos, caso contrário não fazemos nada
            if self.vetor_msg[i].id == ack.id:
                print 'subiu para aplicação a mensagem:', '"',self.vetor_msg[i].msg,'"'
                del self.vetor_msg[i]
                self.vetor_ack.remove(ack)
                break


    # Definição do método para criar uma mensagem
    def cria_msg(self, msg):
        clock_msg = str(self.clock_processo) + self.id      # Criando o clock da mensagem
        mensagem = Mensagem(clock_msg, msg, self.id)
        self.recebe_msg(mensagem)                           # A mensagem criada já é adicionada no vetor de mensagens
        ack = Ack(self.id)                                  # E seu respectivo ack também é criado
        self.recebe_ack(ack)

        return mensagem, ack
        # print 'Clock_msg:', self.vetor_msg[0].clock_msg
        # print 'Id_mensagem:', self.vetor_msg[0].id
        # print 'Mensagem:', self.vetor_msg[0].msg,'\n'
        # print 'Id do ack:', self.vetor_ack[0].id
        # print 'Qtd de acks:', self.vetor_ack[0].n_acks,'\n'

    # Definição do método que envia uma mensagem
    def envia_msg(self):

        mensagem, ack = self.cria_msg(choice(string.letters))

        # Criando meu socket
        meu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectando com os outros processos
        meu_socket.connect((HOST, 25000))

        # Enviando a mensagem e o ack para os outros processos
        meu_socket.send(mensagem)
        meu_socket.send(ack)


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

# Definindo um ack
class Ack:
    def __init__(self, id):
        self.id = id
        self.n_acks = 0

    def get_id(self):
        return self.id

# Definindo a nossa nova thread
def minha_thread(conn, addr):

    # Recebendo os dados dos outros processos e os decodifica
    data = conn.recv(1024)
    decodificada = pickle.loads(data)

    if isinstance(decodificada, (Mensagem)):
        print 'Recebendo mensagem da máquina', addr
        # print 'mensagem'
        # print 'Clock_msg:', decodificada.clock_msg
        # print 'Id_msg:', decodificada.id
        # print 'Mensagem:', decodificada.msg

    elif isinstance(decodificada, (Ack)):
        print 'Recebendo ack da máquina', addr
        # print 'Ack'
        # print 'ID_Ack:', decodificada.id
        # print 'N_acks:', decodificada.n_acks

    conn.close()

# Criando meu socket
meu_socket = socket(AF_INET, SOCK_STREAM)

# Conectando com os outros processos
meu_socket.bind((HOST, 25000))
meu_socket.listen(10)

while True:
    conn, addr = meu_socket.accept()
    thread.start_new_thread(minha_thread, (conn, addr, ))
    # thread = Thread(target = minha.recebendo_dados(conn, addr))
    # thread.start()
    #thread.join()
