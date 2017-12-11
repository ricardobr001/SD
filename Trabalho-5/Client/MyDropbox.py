#coding: utf-8

'''
    python 2.7
    Dropbox cliente

    Nome: Leonardo Zaccarias              RA: 620491
    Nome: Ricardo Mendes Leal Junior      RA: 562262

    Necessário API watchdog

    Caso não instalada -- pip install watchdog
'''

import time
import os
import requests
from watchdog.observers import Observer
from watchdog.events import *


class Dropbox(PatternMatchingEventHandler):
    def __init__(self, host):
        super(Dropbox, self).__init__()
        self.host = host
        self.listaArquivosLocal = os.listdir(DIRETORIO)  # Recuperando a lista com o nome dos arquivos no computador local
        self.listaArquivosNuvem = []
        self.enviando = False

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

    def enviaArquivo(self, nomeArquivo):
        arquivo = open(nomeArquivo, 'r')
        conteudo = arquivo.read()
        self.enviando = True
        print 'Enviando o arquivo %s...      EFETUAR CONEXÃO COM SERVER' % (nomeArquivo.split('/')[1])
        self.enviando = False
    
    def enviaRemovido(self, nomeArquivo):
        print 'Removendo o arquivo %s...        EFETUAR CONEXÃO COM O SERVER' % (nomeArquivo)
        
    def on_created(self, event):
        if (not event.src_path) == 'files' & (not self.enviando):   # Ignora quando o diretório foi modificado
            self.enviaArquivo(event.src_path)

    def on_modified(self, event):
        if (not event.src_path) == 'files' & (not self.enviando):   # Ignora quando o diretório foi modificado
            self.enviaArquivo(event.src_path)

    def on_deleted(self, event):
        if (not event.src_path) == 'files' & (not self.enviando):   # Ignora quando o diretório foi modificado
            self.enviaRemovido(event.src_path.split('/')[1])
            self.listaArquivos = os.listdir(DIRETORIO)  # Atualiza a lista de arquivos no diretório
            print self.listaArquivos

    def atualiza(self):
        # self.listaArquivos = os.listdir(DIRETORIO)      # Sempre atualiza a lista de arquivos
        # self.recebeListaArquivos()
        
        # r = requests.get('http://127.0.0.1:5000/ListaArquivos')                   # FUNCIONA    
        # print r.text
        
        # r = requests.get('http://127.0.0.1:5000/EnviarArquivo/'+'teste.txt')      # FUNCIONA
        # print r.text
        
        # file_ = {'file': ('enviar.txt', open('files/enviar.txt'))}                # FUNCIONA
        # r = requests.post('http://127.0.0.1:5000/ReceberArquivo', files=file_)
        # print r.text

        
    def recebeListaArquivos(self):
        print 'Fazer -> RECEBE LISTA DE ARQUIVOS'
        self.listaArquivosNuvem = ['nuvem.txt']

        if self.listaArquivosLocal != self.listaArquivosNuvem:
            print 'Atualiza a lista de arquivos local'

            for i in range(len(self.listaArquivosNuvem)):
                if not self.listaArquivosNuvem[i] in self.listaArquivosLocal:
                    self.download(self.listaArquivosNuvem[i])
    
    def download(self, nomeArquivo):
        print 'Efetuando download do arquivo %s...' % (nomeArquivo)

DIRETORIO = 'files'
HOST = 'http://localhost:25000/'

if __name__ == '__main__':
    print 'Aperte CTRL+C para parar a execução do programa'
    d = Dropbox(HOST)
    d.inicia()
