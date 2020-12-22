import os
from datamining import extrair_da_lista
from datamining import extrair
from datamining import write_csv_line
from datamining import write_csv_header
from datamining import limpar
from datamining import limpar2

path = 'ADIhtml\\' # usar duas contra-barras depois do nome
lista = os.listdir(path)

for n in range (len(lista)):
    
    # extrai nome e conteúdo do último arquivo da lista
    nomedoarquivo, html = extrair_da_lista(lista, path)
    
    # extrai campo incidente
    incidente = extrair(html, 'verProcessoAndamento.asp?incidente=', '">')
    
    # extrai campos classe + liminar + numero
    cln = extrair(html, '<div><h3><strong>','</strong>')
        
    # extrai campo numero
    numero = extrair(cln, ' - ', "")
    # tratamento do campo numero
    numero = numero.replace('<FONT COLOR=RED><B>1</B></FONT>','1')
    numero = "0"*(4-len(numero))+numero
 
    # extrai campo liminar
    if 'Liminar' in cln:
        liminar = 'sim'
    else:
        liminar = 'não'
    
    # extrai campo classe
    classe = extrair(cln, '', ' - ')
    classe = extrair(classe, '', ' (') 
    
    ## tratamento do campo classe
    classe = classe.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
    classe = classe.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
    
## definição de campo: origem     
    origem = extrair(html,'Origem:</td><td><strong>','</strong>')
    
           
    ## definição de campo: incidente
    entrada = extrair(html,'Entrada no STF:</td><td><strong>','</strong>')
    
    ## definição de campo: relator
    relator = extrair(html,'Relator:</td><td><strong>','</strong>')
    relator = relator.replace('MINISTRO','')
    relator = relator.replace('MINISTRA','')
    
    
    ## definição de campo: distribuição
    distribuicao = extrair(html,'Distribuído:</td><td><strong>','</strong>')
    
    
    ## definição de campo: requerente
    requerente = extrair(html,'Requerente: <strong>','</strong>')
    if '(CF 103, ' in requerente:
        requerentesplit = requerente.split('(CF 103, ')
        requerente = requerentesplit[0]
        requerente = requerente.strip()
        requerentetipo = requerentesplit[1]
        requerentetipo = requerentetipo.replace(')','')
        requerentetipo = requerentetipo.replace('0','')
    else:
        requerentetipo = 'NA'
    
    ## definição de campo: requerido
    requerido = extrair(html,
                        'Requerido :<strong>',
                        '</strong>')
    
    ## definição de campo: dispositivo questionado
    dispositivoquestionado = extrair(html,
                                     'Dispositivo Legal Questionado</b></strong><br /><pre>',
                                     '</pre>')
    dispositivoquestionado = limpar(dispositivoquestionado)
    
    ## definição de campo: resultado da liminar
    resultadoliminar = extrair(html,
                               'Resultado da Liminar</b></strong><br /><br />',
                               '<br />')
    
    ## definição de campo: resultado final
    resultadofinal = extrair(html,
                             'Resultado Final</b></strong><br /><br />',
                             '<br />')
    
    ## definição de campo: decisão monocrática final
    if 'Decisão Monocrática Final</b></strong><br /><pre>' in html:
        decisaomonofinal = extrair(html,
                                   'Decisão Monocrática Final</b></strong><br /><pre>',
                                   '</pre>')
        decisaomonofinal = limpar(decisaomonofinal)
    else: 
        decisaomonofinal = 'NA'
         
    ## definição de campo: fundamento    
    if 'Fundamentação Constitucional</b></strong><br /><pre>' in html:
        fundamento = extrair(html,
                             'Fundamentação Constitucional</b></strong><br /><pre>',
                             '</pre>')
        fundamento = limpar2(fundamento)
    else:
        fundamento = 'NA'
    
    ## definição de campo: fundamento
    if 'Indexação</b></strong><br /><pre>' in html:
        indexacao = extrair(html,
                            'Indexação</b></strong><br /><pre>',
                            '</pre>')
        indexacao = limpar2(indexacao)        
    else:
        indexacao = 'NA'
    
    ### criação da variável dados extraídos, com uma lista de dados
    dados = [classe, numero, incidente, liminar, origem, entrada, relator,
             distribuicao, requerente, requerentetipo, requerido, 
             dispositivoquestionado, resultadoliminar, resultadofinal, 
             decisaomonofinal, fundamento, indexacao]
    campos = '''classe, numero, incidente, liminar, origem, entrada, relator, 
                distribuicao, requerente, requerentetipo, requerido, 
                dispositivoquestionado, resultadoliminar, resultadofinal, 
                decisaomonofinal, fundamento, indexacao'''
    #inserir aqui o conteúdo da lista acima, trocando [] por ''

    
    write_csv_header('ADI.csv',campos, n)
    write_csv_line('ADI.csv',dados)
    
    print (nomedoarquivo)