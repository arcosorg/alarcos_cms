# from datamining import solicitar_dados_CC
from datamining import gravar_dados_no_arquivo
from datamining import esperar
import requests
# from datamining import solicitar_dados_presid

def solicitar_dados_presid (classe, numero):
    url = ('http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28'
           + classe 
           +'%24%2ESCLA%2E+E+'
           + numero 
           + '%2ENUME%2E%29+E+S%2EPRES%2E&base=basePresidencia')
    
    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 1
NumeroFinal = 387


# realiza a extração dos dados e a gravação    
for n in range (NumeroFinal-NumeroInicial+1):
    
    
    esperar(2,10,n)
    esperar(10,100,n)
    
    # define número do processo a ser buscado
    NumProcesso = str(NumeroFinal-n)
    
    print (NumProcesso)
    
    # busca dados do processo definido por classe e número, no banco do CC
    dados = solicitar_dados_presid (Classe, NumProcesso)
       
    # grava dados no arquivo definido
    gravar_dados_no_arquivo(Classe, NumProcesso,'ADIpresid//', dados)

