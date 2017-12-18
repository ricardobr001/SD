#coding: utf-8

'''
    python 2.7
    Dropbox server

    Nome: Leonardo Zaccarias              RA: 620491
    Nome: Ricardo Mendes Leal Junior      RA: 562262

    Necessário framework Flask

    Caso não instalado -- pip install Flask

    Exportar o server -- export FLASK_APP=Server.py
    Executando -- flask run

'''

import time
import os
from flask import Flask, request, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename

DIRETORIO = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DIRETORIO

@app.route('/ListaArquivos')
def listaArquivos():
    if not os.path.exists(DIRETORIO):   # Se não existe o diretório
        os.makedirs(DIRETORIO)  # Cria o diretorio
    return str('/'.join(os.listdir(DIRETORIO)))

@app.route('/download/<path:nome>', methods=['GET', 'POST'])    # Do server para o cliente
def download(nome):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=nome)    # Retorna o arquivo para o cliente

@app.route('/upload', methods=['GET', 'POST'])  # Do cliente para o server
def upload():    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            arquivo = open('removidos.txt')     # Abrindo o arquivo especial de removidos
            conteudo = arquivo.read().split('\n')   # Pega linha por linha
            arquivo.close()

            arquivo = open('removidos.txt', 'w')    # Sobrescreve o arquivo especial
            for i in range(len(conteudo)):
                if conteudo[i] == filename or conteudo[i] == '\n':  # Se for um arquivo ja removido e está inserindo novamente
                    pass    # Não escreve no arquivo especial
                else:
                    arquivo.write(conteudo[i] + '\n')   # Se não escreve
                    
            return 'Arquivo ' + filename + ' salvo'

@app.route('/RemoverArquivo/<string:nome>')
def removeArquivo(nome):
    os.remove('files/'+nome)    # Remove o arquivo
    arquivo = open('removidos.txt', 'a')    # Anota o arquivo no arquivo especial
    arquivo.write(nome + '\n')
    arquivo.close()
    return 'Arquivo ' + nome + ' removido'

@app.route('/Removidos')
def removidos():
    arquivo = open('removidos.txt')
    conteudo = arquivo.read()
    arquivo.close()
    return str(conteudo)    # Retorna a lista de arquivos removidos

@app.route('/AtualizaRemovidos', methods=['GET', 'POST'])
def atualizaRemovidos():
    if request.method == 'POST':
        file = request.files['file']
        arquivo = open('removidos.txt', 'w')
        conteudo = arquivo.write()
        arquivo.close()
        return 'success'