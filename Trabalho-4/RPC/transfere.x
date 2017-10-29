#define MAXNOME 1024
const MAXARQUIVO = 1048576;

typedef string nomeArquivo<MAXNOME>;

typedef opaque conteudoArquivo[MAXARQUIVO];

struct arquivoIn 
{
	nomeArquivo nome;
	int tam;
	int primPedaco;
	conteudoArquivo dados;
};

struct arquivoOut
{
	long ok;
};

program TRANSFEREARQUIVO_PROGRAMA
{
	version TRANSFEREARQUIVO_VERSAO
	{
		arquivoOut transfere_arq(arquivoIn *) = 1;
	} = 1;
} = 0x31230000;