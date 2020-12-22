from datamining import extrair
from datamining import solicitar_dados_AP
from datamining import gravar_dados_no_arquivo
from datamining import solicitar_utf8
from datamining import solicitar_dados_CC
from datamining import esperar

 
# Definição dos parâmetros de busca
Classe = "HC"
NumeroInicial = 175090
NumeroFinal = 175794
dominio = 'http://portal.stf.jus.br/processos/'

#iterador para buscar os processos
for vezes in range (NumeroFinal-NumeroInicial+1):
    
    esperar(4,5,vezes)
    esperar(60,700,vezes)
    
    NumProcesso = str(NumeroFinal-vezes)
    print (Classe+NumProcesso)
           
    # Extração das informações
    html = solicitar_dados_AP(Classe, NumProcesso)
    
    # extrai campo incidente do html
    incidente = extrair(html,'id="incidente" value="', '">')

    # extrai dados dos URLs
    
    partes          = solicitar_utf8(dominio,
                                     'abaPartes.asp?incidente=', 
                                     incidente)
    
    informacoes     = solicitar_utf8(dominio, 
                                     'abaInformacoes.asp?incidente=', 
                                     incidente)
    
    andamentos      = solicitar_utf8(dominio,
                                     'abaAndamentos.asp?incidente=', 
                                     (incidente +'&imprimir=1'))
    
    pauta           = solicitar_utf8(dominio,
                                     'abaPautas.asp?incidente=',
                                     incidente)
    
    sessao          = solicitar_utf8(dominio, 
                                     'abaSessao.asp?incidente=', 
                                     incidente)
    
    decisoes        = solicitar_utf8(dominio, 
                                     'abaDecisoes.asp?incidente=', 
                                     incidente)
    
    deslocamentos   = solicitar_utf8(dominio, 
                                     'abaDeslocamentos.asp?incidente=', 
                                     incidente)
    
    peticoes        = solicitar_utf8(dominio, 
                                     'abaPeticoes.asp?incidente=', 
                                     incidente)
    
    recursos         = solicitar_utf8(dominio, 
                                      'abaRecursos.asp?incidente=', 
                                      incidente)
    
    if (Classe == 'ADI' 
        or Classe == 'ADPF' 
        or Classe == 'ADO' 
        or Classe == 'ADC'):
        cc = solicitar_dados_CC(Classe, NumProcesso)
    else:
        cc = 'NA'
    
    # define dados a serem gravados
    dados = ('incidente=' + incidente + 'fonte>>>>' +html + 
             'partes>>>>' + partes + 'informacoes>>>>' + informacoes + 
             'andamentos>>>>' + andamentos + 'pauta>>>>' + pauta + 
             'sessao>>>>' + sessao + 'decisoes>>>>' + decisoes + 
             'deslocamentos>>>>' + deslocamentos + 'peticoes>>>>' + 
             peticoes + 'recursos>>>>' + recursos + 'cc>>>>' + cc)
             
    # função de gravação
    gravar_dados_no_arquivo (Classe, NumProcesso, 'HCtotal\\', dados)
    
    print (f'Gravado arquivo {Classe+NumProcesso}')   
    