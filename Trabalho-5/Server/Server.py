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
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

DIRETORIO = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DIRETORIO

@app.route('/ListaArquivosServer')
def listaArquivos():
    return ';'.join(os.listdir(DIRETORIO))

@app.route('/EnviarArquivo/<string:nome>')
def enviaArquivo(nome):
    arquivo = open('files/'+nome)
    conteudo = arquivo.read()
    return conteudo

@app.route('/ReceberArquivo', methods=['GET', 'POST'])
def recebeArquivo():
    if request.method == 'POST':
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'Arquivo ' + filename + ' salvo'