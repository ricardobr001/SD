#coding: utf-8
#python 2.7

from socket import *
import threading

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

        # Se o ack não estiver na lista de acks
        if not ack in self.vetor_ack:

            # Conta que recebeu um determinado ack, e coloca esse ack no vetor de acks
            ack.n_acks += 1
            self.vetor_ack.insert(len(self.vetor_ack), ack)
            # self.vetor_ack = sorted(self.vetor_ack, key = Ack.get_id) ################ Testando ordenação de objetos

        else:

            # Busca o ack na lista de acks, retorna seu indíce e contabiliza mais um ack deste determinado ack
            i = self.vetor_ack.index(ack)
            self.vetor_ack[i].n_acks += 1

            # Se tiver 3 acks e a mensagem, sobe o ack para a aplicação
            if self.vetor_ack[i].n_acks == 3:
                print 'subiu para aplicação a mensagem'
                    #subir(self.vetor_ack[i])

    # Definição do método que recebe mensagem
    def recebe_msg(self, msg):

        # Se está mensagem não estiver no vetor
        if not msg in self.vetor_msg:

            # Inserimos ela no vetor de mensagens e ordenamos o vetor
            self.vetor_msg.insert(len(self.vetor_msg), msg)
            self.vetor_msg = sorted(self.vetor_msg, key = Mensagem.get_clock)

        # Caso contrário não fazemos nada

    # Definição do método para criar uma mensagem
    def cria_msg(self, msg):
        clock_msg = str(self.clock_processo) + self.id
        mensagem = Mensagem(clock_msg, msg, self.id)
        print mensagem.clock_msg

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

print 'teste'
processo = Processo(1, "23")
processo.incrementa_clock()
processo.cria_msg("MILEY BURRO")
ack = Ack("23")
processo.recebe_ack(ack)
# print processo.vetor_ack[0].id
# print processo.vetor_ack[0].n_acks
processo.recebe_ack(ack)
# print processo.vetor_ack[0].id
# print processo.vetor_ack[0].n_acks
ack_novo = Ack("12")
processo.recebe_ack(ack_novo)
ack_novo_3 = Ack("91")
processo.recebe_ack(ack_novo_3)
ack_novo_4 = Ack("17")
processo.recebe_ack(ack_novo_4)
# print processo.vetor_ack[0].id
# print processo.vetor_ack[0].n_acks
print 'id\tacks\tpos'
for index in range(len(processo.vetor_ack)):
    print processo.vetor_ack[index].id,'\t',processo.vetor_ack[index].n_acks,'\t',index




# Fila de mensagens (variavel global)
# list fila_msg

# clock_local = 1

# Função de receber mensagem
# def receber_msg(nova_msg):
#     # Atualiza clock se necessário
#     if nova_msg.clock_p > clock_local:
#         clock_local = nova_msg.clock_p
#     #insere mensagem na lista ordenada
#     i = 0
#     while fila_msg[i] < len(fila_msg):
#         if fila_msg[i].clock_p > nova_msg.clock_p:
#             fila_msg.insert(i, nova_msg)
#             i = len(fila_msg)   # sai do loop dps q insere
#         i++
#     # verifica se mensagem pode ser passada para aplicação
#     verificar_lista()
#     return true

# def receber_ack(ack):
#     # busca mensagem correspondente ao ack
#     i = 0
#     while fila_msg[i] < len(fila_msg):
#         if fila_msg[i].id == ack:
#             fila_msg[i].ack = fila_msg[i].ack + 1   # incrementa ack
#             i = len(fila_msg)   # sai do loop dps q insere
#         i++
#     # verifica se mensagem pode ser passada para aplicação
#     verificar_lista()
#     return true

# # verifica se a primeira mensagem da lista pode ser enviada para a aplicação
# def verificar_lista():
#     if fila_msg[0].acks == 2:
#         fila_msg.remove(fila_msg[0])    # envia mensagem para aplicação
#     return true

# def criar_nova_msg():
#     nova_msg.clock_p = clock_local + 1
