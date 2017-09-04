#coding: utf-8

from socket import *
import threading

class Processo:
    def __init__(self, incremento_clock, id):
        self.clock_processo = incremento_clock
        self.id = id # os.getpid()
        self.incremento_clock = incremento_clock
        self.vetor_ack = []
        self.vetor_msg = []

    def incrementa_clock(self):
        self.clock_processo += self.incremento_clock

    def recebe_ack(self, ack):
        i = self.busca_ack(ack.id)

        if i != -1:
            self.vetor_ack[i].n_acks += 1

            if self.vetor_ack[i].acks == 3:
                print 'teste'
                #subir(self.vetor_ack[i])
        else:
            ack.n_acks += 1
            self.vetor_ack.insert(len(self.vetor_ack), ack)


    def busca_ack(self, valor):
        i = 0

        while i < (len(self.vetor_ack)):
            if self.vetor_ack[i].id == valor:
                return i
        return -1

    # def subir_msg(self, msg, ack):
    #     #if
    #         self.vetor_msg.remove(msg)
    #         self.vetor_ack.remove(ack)

    def cria_msg(self, msg):
        clock_msg = str(self.clock_processo) + self.id
        mensagem = Mensagem(clock_msg, msg)
        print mensagem.clock_msg

class Mensagem:
    def __init__(self, clock_msg, msg, id):
        self.clock_msg = clock_msg
        self.id = id
        self.msg = msg

class Ack:
    def __init__(self, id):
        self.id = id
        self.n_acks = 0

print 'teste'
processo = Processo(1, "23")
processo.incrementa_clock()
processo.cria_msg("MILEY BURRO")
ack = Ack("23")
processo.recebe_ack(ack)
print processo.vetor_ack[0].id
print processo.vetor_ack[0].n_acks
processo.recebe_ack(ack)
print processo.vetor_ack[0].id
print processo.vetor_ack[0].n_acks




#Fila de mensagens (variavel global)
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
