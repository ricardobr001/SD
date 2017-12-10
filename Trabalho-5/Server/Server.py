#coding: utf-8
# python 2.7

########################################################
# Nome: Leonardo Zaccarias              RA: 620491     #
# Nome: Ricardo Mendes Leal Junior      RA: 562262     #
########################################################

import time
import os
from watchdog.observers import Observer
from watchdog.events import *

class Server(PatternMatchingEventHandler):
    def __init__(self, host):
        super(Server, self).__init__()
        self.host = host
        self.listaArquivosServer = os.listdir(DIRETORIO)  # Recuperando a lista com o nome dos arquivos no servidor
        
    
    def inicia(self):
        obs = Observer()
        obs.schedule(self, DIRETORIO, recursive=True)
        obs.start()

        try:
            while True:
                time.sleep(5)
                self.atualiza()
        except:
            obs.stop()

        obs.join()

    def atualiza(self):
        self.enviaListaArquivos()
    
    def enviaListaArquivos(self):
        print 'Nuvem -> Clientes'

# Variável global com o nome do diretório a ser observado
PORT = 25000
DIRETORIO = 'files'
HOST = 'http://localhost:25000'

if __name__ == '__main__':
    print 'Aperte CTRL+C para parar a execução do programa'
    obs = Server(HOST)    
    obs.inicia()