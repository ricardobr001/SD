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
import sys
import requests
import shutil
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
    
    def enviaRemovido(self, nomeArquivo):
        print 'Removendo o arquivo %s...        EFETUAR CONEXÃO COM O SERVER' % (nomeArquivo)

    def on_modified(self, event):
        if not event.src_path == 'files':   # Ignora quando o diretório foi modificado
            self.upload(event.src_path)

    def on_deleted(self, event):
        if not event.src_path == 'files':   # Ignora quando o diretório foi modificado
            self.enviaRemovido(event.src_path.split('/')[1])
            self.listaArquivos = os.listdir(DIRETORIO)  # Atualiza a lista de arquivos no diretório

    def atualiza(self):
        self.listaArquivosLocal = os.listdir(DIRETORIO)      # Sempre atualiza a lista de arquivos
        self.recebeListaArquivos()
        
    def recebeListaArquivos(self):
        r = requests.get(HOST + 'ListaArquivos')
        if not r.text == '':    # Se tiver arquivos no server
            self.listaArquivosNuvem = r.text.split('/') # Separando a lista recebida 
            self.decodifica()   # Decodifando a lista

            for i in range(len(self.listaArquivosNuvem)):   # Andando a lista de arquivos da nuvem
                if not str(self.listaArquivosNuvem[i]) in self.listaArquivosLocal:  # Se encontrar um arquivo da nuvem que não está no local
                    self.download(self.listaArquivosNuvem[i])   # Efetua o download

        elif len(self.listaArquivosLocal) > 0:  # Se tiver arquivos no local
            for i in range(len(self.listaArquivosLocal)):   # Andando a lista de arquivos local
                if not str(self.listaArquivosLocal[i]) in self.listaArquivosNuvem:  # Se encontrar um arquivod local que não está na nuvem
                    self.upload(self.listaArquivosLocal[i])   # Efetua o upload
        else:
            print 'Nenhum arquivo salvo na nuvem e no diretório local'
    
    def download(self, nomeArquivo):
        r = requests.get(HOST + 'Download/' + nomeArquivo, stream=True) # Recebendo o arquivo pelo método get
        print 'Efetuando download do arquivo %s...' % (nomeArquivo)
        with open(DIRETORIO + '/' + nomeArquivo, 'wb') as out_file:     # Recebe os dados do stream criado
            shutil.copyfileobj(r.raw, out_file)     # Escreve os dados no arquivo
        del r
    
    def upload(self, nomeArquivo):
        print 'Enviando o arquivo %s...' % (nomeArquivo)
        file_ = {'file': (nomeArquivo, open('files/' + nomeArquivo))}   # Abrindo o arquivo
        r = requests.post(HOST + 'ReceberArquivo', files=file_)         # Enviando o arquivo pelo metódo post ao server
        print r.text    # Imprimindo a respota do server
        del r

    def decodifica(self):
        for i in range(len(self.listaArquivosNuvem)):
            self.listaArquivosNuvem[i] = self.listaArquivosNuvem[i].encode('utf8')

if len(sys.argv) > 1:
    HOST = sys.argv[1]
else:
    HOST = 'http://127.0.0.1:5000/'

DIRETORIO = 'files'

if __name__ == '__main__':
    print 'Aperte CTRL+C para parar a execução do programa'
    d = Dropbox()
    d.inicia()
