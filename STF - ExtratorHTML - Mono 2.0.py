# from datamining import solicitar_dados_CC
from datamining import gravar_dados_no_arquivo
from datamining import esperar
# import requests
from datamining import solicitar_dados_mono


# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 1
NumeroFinal = 2483


# realiza a extração dos dados e a gravação    
for n in range (NumeroFinal-NumeroInicial+1):
    
    
    esperar(2,10,n)
    esperar(10,100,n)
    
    # define número do processo a ser buscado
    NumProcesso = str(NumeroFinal-n)
    
    print (NumProcesso)
    
    # busca dados do processo definido por classe e número, no banco do CC
    dados = solicitar_dados_mono (Classe, NumProcesso)
       
    # grava dados no arquivo definido
    gravar_dados_no_arquivo(Classe, NumProcesso,'ADImono//', dados)

