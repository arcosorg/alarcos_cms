import requests 

# Definição dos parâmetros de busca
Classe = "RE"
NumeroInicial = 1
NumeroFinal = 1108778

for n in range (NumeroFinal-NumeroInicial+1):
    
    # Módulo de geração de URLs
    NumProcesso = str(NumeroFinal-n)
    url = 'http://portal.stf.jus.br/processos/listarProcessos.asp?classe=&numeroProcesso='+ NumProcesso
    print (url)
    
    # Módulo básico de extração
    html = requests.get(url).text
    
    inicio = html.find('detalhe.asp?')
    if inicio == -1:
        print ("Não há processo")
        nomedoarquivo = 'REvazios.txt'
        arquivo = open(nomedoarquivo, 'a', encoding='utf-8')
        arquivo.write(NumProcesso +',')
        arquivo.close()
    else:    
        inicio = html.find('detalhe.asp?')
        fim = html.find('</a>',inicio)
        html = html[inicio:fim]
        html2 = html.split('">')
        html3 = html2[1].split(' ')
        incidente = html2[0].split('=')[1]
        
        htmlinformacoes = requests.get('http://portal.stf.jus.br/processos/abaInformacoes.asp?incidente='+incidente).text
        
        htmlandamentos = requests.get('http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente='+incidente+'&imprimir=1').text
        
        htmlpauta = requests.get('http://portal.stf.jus.br/processos/abaPautas.asp?incidente='+incidente).text
        
        htmlsessao = requests.get('http://portal.stf.jus.br/processos/abaSessao.asp?incidente='+incidente).text
        
        urldecisoes = requests.get('http://portal.stf.jus.br/processos/abaDecisoes.asp?incidente='+incidente).text
        
        htmldeslocamentos = requests.get('http://portal.stf.jus.br/processos/abaDeslocamentos.asp?incidente='+incidente).text
        
        htmlpeticoes = requests.get('http://portal.stf.jus.br/processos/abaPeticoes.asp?incidente='+incidente).text
        
        htmlrecursos = requests.get('http://portal.stf.jus.br/processos/abaRecursos.asp?incidente='+incidente).text
        
        # Módulo básico de gravação
        nomedoarquivo = 'REhtml2\\' + Classe + NumProcesso + '.html'
        arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
        arquivo.write(html3[0]+','+html3[1]+ ',' + html2[0] + '\n' + htmlinformacoes + '>>>>' + htmlandamentos + '>>>>' + htmlpauta + '>>>>' + htmlsessao + '>>>>' + urldecisoes + '>>>>' + htmldeslocamentos + '>>>>' + htmlpeticoes + '>>>>' + htmlrecursos)
        arquivo.close()