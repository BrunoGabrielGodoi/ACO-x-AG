"""// ConsoleApplication4.cpp : define o ponto de entrada para o aplicativo do console.
//



//A = 0
//B = 1750(n tenho certeza)
//C = 125

#include "stdafx.h"

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <math.h>
#include <bitset>

#define MAXPOP 25000
#define KILLPOP 1000
#define GENERATIONS 999999
#define PRINT 50 // de quantas em quanats gerações dar print nas informações

using namespace std;

struct Cromossomo {
	int a, af, b, bf, c, cf;
	float colocacao = 0;
};

void GerarPop(Cromossomo *array) {
	srand((unsigned)time(NULL));
	for (int i = 0; i<MAXPOP; i++) {
		array[i].a = rand() % 2049;
		array[i].b = rand() % 2049;
		array[i].c = rand() % 2049;

	}

	for (int i = 0; i<MAXPOP; i++) {
		array[i].af = rand() % 16;
		array[i].bf = rand() % 16;
		array[i].cf = rand() % 16;

	}

}


void Testar(Cromossomo *array) {


	for (int i = 0; i<MAXPOP; i++) {
		if (array[i].colocacao == 0)
		{


			//cout << (array[i].a + (array[i].af / 10.)) << " B- " << (array[i].b + (array[i].bf / 10.)) << " C- " << (2*(array[i].c + (array[i].cf / 10.))) << " TOTAL " << (array[i].a + (array[i].af / 10.)) + (array[i].b + (array[i].bf / 10.)) + (2*(array[i].c + (array[i].cf / 10.))) << endl;
			if ((array[i].a + (array[i].af / 10.)) + (array[i].b + (array[i].bf / 10.)) + (2 * (array[i].c + (array[i].cf / 10.))) > 2000) {
				array[i].colocacao = 1;
			}
			else if ((3 * (array[i].a + (array[i].af / 10.))) + (4.5*(array[i].b + (array[i].bf / 10.))) + ((array[i].c + (array[i].cf / 10.))) > 8000) {
				array[i].colocacao = 1;
			}
			else {
				array[i].colocacao = (5 * (array[i].a + (array[i].af / 10.))) + (7 * (array[i].b + (array[i].bf / 10.))) + (8 * (array[i].c + (array[i].cf / 10.)));
			}
		}
	}

	int n = MAXPOP;
	int k, j;
	Cromossomo aux;
	for (k = 0; k < n; k++) {
		for (j = 0; j < n - 1; j++) {
			if (array[j].colocacao > array[j + 1].colocacao) {
				aux = array[j];
				array[j] = array[j + 1];
				array[j + 1] = aux;
			}
		}
	}

}

Cromossomo Reproduzir(Cromossomo X, Cromossomo Y) {
	srand(time(NULL));
	Cromossomo filho;
	bitset<5> fracao[6], resultadof[3];
	bitset<11> inteiro[6], resultadoi[3];
	string sfracao[6], sinteiro[6];

	fracao[0] = X.af;
	fracao[1] = X.bf;
	fracao[2] = X.cf;
	fracao[3] = Y.af;
	fracao[4] = Y.bf;
	fracao[5] = Y.cf;
	
	inteiro[0] = X.a;
	inteiro[1] = X.b;
	inteiro[2] = X.c;
	inteiro[3] = Y.a;
	inteiro[4] = Y.b;
	inteiro[5] = Y.c;
	
	//for (size_t i = 0; i < 6; i++)
	//{
	//	sfracao[i] = fracao[i].to_string();
	//	sinteiro[i] = inteiro[i].to_string();
	//}
	for (int j = 0; j < 3; j++)
	{
		for (int i = 0; i < 5; i++)
		{
			int test = rand() % 2;
			resultadof[j][i] = (test == 0) ? fracao[j][i] : fracao[j+3][i];
			if ((rand() % 25 ) +1 == 2)
			{
				//cout << "mutou" << endl;
				if (resultadof[j][i] == 0)
				{
					resultadof[j][i] = 1;
				}
				else {
					resultadof[j][i] = 0;
				}
			}
		}
	}
	for (int j = 0; j < 3; j++)
	{
		for (int i = 0; i < 11; i++)
		{
			int test = rand() % 2;
			resultadoi[j][i] = (test == 0) ? inteiro[j][i] : inteiro[j + 3][i];
			if ((rand() % 25) + 1 == 2)
			{
				//cout << "mutou" << endl;
				if (resultadoi[j][i] == 0)
				{
					resultadoi[j][i] = 1;
				}
				else {
					resultadoi[j][i] = 0;
				}
			}
		}
	}
	// mutação--------------------------------------
	/*for (int i = 0; i < 3; i++)
	{
		fracao[i] = bitset<5>(resultadof[i]);
		inteiro[i] = bitset<11>(resultadoi[i]);
	}*/
	
	filho.a = resultadoi[0].to_ulong();
	filho.b = resultadoi[1].to_ulong();
	filho.c = resultadoi[2].to_ulong();

	filho.af = resultadof[0].to_ulong();
	filho.bf = resultadof[1].to_ulong();
	filho.cf = resultadof[2].to_ulong();

	filho.colocacao = 0;

	return filho;
}

void Reproducao(Cromossomo *array) {

	float somatoria = 0;
	int p1 = 0, p2 = 0;
	for (int i = KILLPOP; i < MAXPOP - 1; i++)
	{
		somatoria += array[i].colocacao;
	}
	somatoria = somatoria / 1000;

	for (int i = 0; i < KILLPOP; i++)
	{

		p1 = 0;
		for (int j = 0; j < 2; j++)
		{


			int sorteio = rand() % (int)(ceil(somatoria));
			//cout << (int)(floor(somatoria)) <<" = "<< sorteio <<endl;

			int k = MAXPOP -1;
			for (; sorteio > 0; k--)
			{
				sorteio -= array[k].colocacao / 1000;
				if (k == 0) k = MAXPOP-1;
			}
			
			

			if (p1 == 0)
			{
				p1 = k;
			}
			else
			{
				p2 = k;
			}
		}
		
	
		array[i] = Reproduzir(array[p1], array[p2]);

	}

}



void Show(Cromossomo *array) {

	cout << endl << "MELHORES ---" << endl;
	for (int i = 5999; i > 5970; i--)
	{
		cout << array[i].colocacao << "*-*";
	}
	cout << endl <<  "PIORES ---" << endl;
	for (int i = 0; i < 30; i++)
	{
		cout << array[i].colocacao << "*-*";
	}
}
float oldA,oldB,oldC,oldL;
void DesvioPadrao(Cromossomo *array) {

	float mediaa = 0, mediab = 0, mediac = 0, lucro = 0;
	float finalmediaa = 0, finalmediab = 0, finalmediac = 0, finallucro = 0,tempmedia = 0;
	for (int i = 0; i < MAXPOP; i++)
	{
		mediaa += array[i].a;
		mediab += array[i].b;
		mediac += array[i].c;
		lucro += array[i].colocacao;
	}

	mediaa = mediaa / MAXPOP;
	mediab = mediab / MAXPOP;
	mediac = mediac / MAXPOP;
	lucro = lucro / MAXPOP;
	for (int i = 0; i < MAXPOP; i++)
	{
		finalmediaa += pow((double)(array[i].a + mediaa), 2);
		finalmediab += pow((double)(array[i].b + mediab), 2);
		finalmediac += pow((double)(array[i].c + mediac), 2);
		finallucro += pow((double)(array[i].colocacao + lucro), 2);
	}
	
	finalmediaa = sqrt((finalmediaa / MAXPOP));
	
	cout << endl << " Desvio a = " << finalmediaa;
	if (finalmediaa > oldA) cout << " Aumentando" ;
	else if (finalmediaa == oldA) cout << " Igual" ;
	else cout << " Diminuindo" ;
	cout << " " << finalmediaa - oldA << endl;
	
	finalmediab = sqrt((finalmediab / MAXPOP));
	cout << " Desvio b = " << finalmediab;
	if (finalmediab > oldB) cout << " Aumentando" ;
	else if (finalmediab == oldB) cout << " Igual" ;
	else cout << " Diminuindo" ;
	cout << " " << finalmediab - oldB << endl;
	
	finalmediac = sqrt((finalmediac / MAXPOP));
	cout << " Desvio c = " << finalmediac;
	if (finalmediac > oldC) cout << " Aumentando" ;
	else if (finalmediac == oldC) cout << " Igual" ;
	else cout << " Diminuindo" ;
	cout << " " << finalmediac - oldC << endl;
	
	finallucro = sqrt((finallucro / MAXPOP));
	cout<< " Desvio Lucro = " << finallucro;
	if (finallucro > oldL) cout << " Aumentando" ;
	else if (finallucro == oldL) cout << " Igual" ;
	else cout << " Diminuindo" ;
	cout << " " << finallucro - oldL << endl;

	oldA = finalmediaa;
	oldB = finalmediab;
	oldC = finalmediac;
	oldL = finallucro;
}


int main() {

	
	Cromossomo inteiro[MAXPOP];
	GerarPop(inteiro);
	Testar(inteiro);
	for (int i = 0; i < GENERATIONS; i++)
	{	
		Reproducao(inteiro);
		Testar(inteiro);
		//Show(inteiro);
		cout << ".";
		if (i % PRINT == 0)
		{
			cout << endl << "MELHOR -- GER " <<i << endl
				<< "classificação = " << inteiro[MAXPOP - 1].colocacao << endl
				<< "a / af =" << inteiro[MAXPOP - 1].a << "/" << inteiro[MAXPOP - 1].af << endl
				<< "b / bf =" << inteiro[MAXPOP - 1].b << "/" << inteiro[MAXPOP - 1].bf << endl
				<< "c / cf =" << inteiro[MAXPOP - 1].c << "/" << inteiro[MAXPOP - 1].cf << endl;
			cout << endl << "PIOR -- GER " << i << endl
				<< "classificação = " << inteiro[0].colocacao << endl
				<< "a / af =" << inteiro[0].a << "/" << inteiro[0].af << endl
				<< "b / bf =" << inteiro[0].b << "/" << inteiro[0].bf << endl
				<< "c / cf =" << inteiro[0].c << "/" << inteiro[0].cf << endl;
			DesvioPadrao(inteiro);
		}
	}
	
	cout << endl << "MELHOR --" << endl
		<< "classificação = " << inteiro[MAXPOP - 1].colocacao << endl
		<< "a / af =" << inteiro[MAXPOP - 1].a << "/" << inteiro[MAXPOP - 1].af << endl
		<< "b / bf =" << inteiro[MAXPOP - 1].b << "/" << inteiro[MAXPOP - 1].bf << endl
		<< "c / cf =" << inteiro[MAXPOP - 1].c << "/" << inteiro[MAXPOP - 1].cf << endl;

	

	system("pause");
	
}"""








