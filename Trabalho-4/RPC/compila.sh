#!/bin/sh

#Compilando transfere.x
rpcgen -a transfere.x

#Compilando o client.c
cc -c client.c -o client.o
cc -c transfere_clnt.c -o transfere_clnt.o
cc -c transfere_xdr.c -o transfere_xdr.o
cc -o client client.o transfere_clnt.o transfere_xdr.o -lnsl

#Compilando o server.c
cc -c server.c -o server.o
cc -c transfere_svc.c -o transfere_svc.o
cc -o server server.o transfere_svc.o transfere_xdr.o -lnsl

#Limpando arquivos inuteis
rm *.o
rm -f transfere_xdr.c transfere_svc.c transfere.h transfere_clnt.c transfere_client.c transfere_server.c
rm Makefile.transfere