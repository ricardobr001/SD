#include <stdio.h>
#include "transfere.h"

arquivoOut *transfere_arq_1_svc(arquivoIn *in, struct svc_req *rqstp)
{
	static arquivoOut out;

	FILE *arq;

	if (in->primPedaco)
	{
		arq = fopen(in->nome, "w");
		printf("Criando o arquivo %s...\n", in->nome);
	}
	else
	{
		arq = fopen(in->nome, "a");
		printf("Recebendo dados do arquivo %s...\n", in->nome);
	}

	if (arq == NULL)
	{
		printf("Problema para abrir ou criar o arquivo %s!\n", in->nome);
		out.ok = 0;
		return &out;
	}

	fwrite(in->dados, 1, in->tam, arq);
	fclose(arq);

	out.ok = 1;
	return &out;
}