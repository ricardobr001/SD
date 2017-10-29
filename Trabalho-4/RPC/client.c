#include <stdio.h>
#include <string.h>
#include "transfere.h"

int main(int argc, char *argv[])
{
	CLIENT *cl;
	FILE *arq;
	arquivoIn in;
	arquivoOut *out;


	if (argc != 3)
	{
		printf("MODO DE USAR: ./client <nome do host> <nome do arquivo>\n");
		return 0;
	}

	cl = clnt_create(argv[1], TRANSFEREARQUIVO_PROGRAMA, TRANSFEREARQUIVO_VERSAO, "tcp");

	if (cl == NULL)
	{
		printf("ERRO!!\nNão foi possível conectar ao servidor!\n");
		return 0;
	}

	arq = fopen(argv[2], "r");

	if (arq == NULL)
	{
		printf("ERRO!!\nNão foi possível abrir o arquivo %s!\n", argv[2]);
		printf("Verificar se o arquivo existe ou se ele está no diretório do programa!\n");
		return 0;
	}

	in.nome = argv[2];
	in.tam = 0;
	in.primPedaco = 1;

	while(1)
	{
		in.tam = fread(in.dados, 1, MAXARQUIVO, arq);
		out = transfere_arq_1(&in, cl);

		if (!out->ok)
		{
			printf("Falha durante o envio!!\n");
			return 0;
		}

		if (in.tam < MAXARQUIVO)
		{
			break;
		}

		in.primPedaco = 0;
	}

	fclose(arq);
	printf("Arquivo %s enviado!\n", argv[2]);

	return 0;
}