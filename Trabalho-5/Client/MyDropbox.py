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
    def __init__(self):
        super(Dropbox, self).__init__()
        self.listaArquivosLocal = os.listdir(DIRETORIO)  # Recuperando a lista com o nome dos arquivos no computador local
        self.listaArquivosNuvem = []
        self.enviarArquivos = []

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
        print 'Enviando o arquivo %s...' % (nomeArquivo.split('/')[1])
        file_ = {'file': (nomeArquivo, open('files/' + nomeArquivo))}
        r = requests.post(HOST + 'ReceberArquivo', files=file_)
        print r.text
    
    def enviaRemovido(self, nomeArquivo):

        print 'Removendo o arquivo %s...        EFETUAR CONEXÃO COM O SERVER' % (nomeArquivo)
        
    def on_created(self, event):
        if not event.src_path == 'files':   # Ignora quando o diretório foi modificado
            print 'Criado:',event.src_path.split('/')[1]
            # self.enviaArquivo(event.src_path)

    def on_modified(self, event):
        if not event.src_path == 'files':   # Ignora quando o diretório foi modificado
            print 'Modificado:',event.src_path.split('/')[1]
            # self.enviaArquivo(event.src_path)

    def on_deleted(self, event):
        if not event.src_path == 'files':   # Ignora quando o diretório foi modificado
            self.enviaRemovido(event.src_path.split('/')[1])
            self.listaArquivos = os.listdir(DIRETORIO)  # Atualiza a lista de arquivos no diretório

    def atualiza(self):
        self.listaArquivosLocal = os.listdir(DIRETORIO)      # Sempre atualiza a lista de arquivos
        self.recebeListaArquivos()
        
        
        # r = requests.get('http://127.0.0.1:5000/EnviarArquivo/'+'teste.txt')      # FUNCIONA
        # print r.text
        
        # file_ = {'file': ('enviar.txt', open('files/enviar.txt'))}                # FUNCIONA
        # r = requests.post('http://127.0.0.1:5000/ReceberArquivo', files=file_)
        # print r.text

        
    def recebeListaArquivos(self):
        r = requests.get(HOST + 'ListaArquivos')
        if not r.text == '':
            self.listaArquivosNuvem = r.text.split('/')
            self.decodifica()
            print 'Lista de arquivos local:', self.listaArquivosLocal
            print 'Lista de arquivos nuvem:', self.listaArquivosNuvem

            for i in range(len(self.listaArquivosNuvem)):
                if not str(self.listaArquivosNuvem[i]) in self.listaArquivosLocal:
                    self.download(self.listaArquivosNuvem[i])
        else:
            print 'Nenhum arquivo salvo na nuvem'
    
    def download(self, nomeArquivo):
        r = requests.get(HOST + 'Download/' + nomeArquivo)
        print 'Efetuando download do arquivo %s...' % (nomeArquivo)
        arquivo = open('files/' + nomeArquivo, 'w')
        arquivo.write(r.text.encode('utf8'))

    def decodifica(self):
        for i in range(len(self.listaArquivosNuvem)):
            self.listaArquivosNuvem[i] = self.listaArquivosNuvem[i].encode('utf8')
DIRETORIO = 'files'
HOST = 'http://127.0.0.1:5000/'

if __name__ == '__main__':
    print 'Aperte CTRL+C para parar a execução do programa'
    d = Dropbox()
    d.inicia()
