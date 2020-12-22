from datamining import (extrair, 
                        extrair_da_lista, 
                        extrair_campo_lista,
                        write_csv_header, 
                        write_csv_lines,
                        # carregar_arquivo,
                        # carregar_arquivo_nome,
                        limpar, 
                        limpar2,
                        extrai_acordaos_da_string,
                        extrai_mono_da_string,
                        limpar_decisao,
                        remover_acentos)

from andamentos import extrair_andamentos
import os


path = 'ADItotal\\' # usar duas contra-barras depois do nome
lista = os.listdir(path)
# lista = lista[:5000]


partes = []
dados_csv = []
inexistentes_csv = []
andamentos = []
html = ''

for n in range (len(lista)):
    nomedoarquivo = 'NA' 
    classecc = 'NA' 
    numerocc = 'NA' 
    processo_juris = 'NA' 
    incidentecc = 'NA'
    requerente_cc = 'NA' 
    requerente_cctipo = 'NA' 
    requerido = 'NA' 
    partes = 'NA'
    andamentos = 'NA' 
    codigofonte = 'NA' 
    eletronico_fisico = 'NA' 
    sigilo = 'NA'
    nome_processo = 'NA' 
    numerounico = 'NA' 
    relatorcc = 'NA' 
    relator = 'NA' 
    redator_acordao = 'NA' 
    relator_juris = 'NA'
    data_acordao = 'NA' 
    orgao_julgador_acordao = 'NA' 
    publicacao_acordao = 'NA' 
    ementa = 'NA' 
    decisao_juris = 'NA' 
    legislacao = 'NA' 
    doutrina = 'NA' 
    lista_processos_citados = 'NA'
    lista_procesoss_citados_com_tema = 'NA'
    relator_ultimo_incidente = 'NA' 
    assuntos = 'NA' 
    procedencia = 'NA' 
    protocolo_data = 'NA' 
    entradacc = 'NA' 
    distribuicao = 'NA' 
    orgaodeorigem = 'NA' 
    numerodeorigem = 'NA' 
    origem = 'NA' 
    origemcc = 'NA' 
    procedencia = 'NA' 
    n_acordaos = 'NA'  
    liminar = 'NA' 
    dispositivoquestionado = 'NA' 
    resultadoliminar = 'NA' 
    resultadofinal = 'NA' 
    decisaomonofinal = 'NA' 
    fundamento = 'NA' 
    indexacao = 'NA'
    requerentes1 = 'NA'
    
    # extrai nome e conteúdo do último arquivo da lista
    nomedoarquivo, html = extrair_da_lista(lista, path)
    
    # carrega dados do arquivo (para poder ver um arquivo específico)
    # nomedoarquivo, html = carregar_arquivo ('ADI', '5000', 'ADItotal\\')
    print(nomedoarquivo)
    
    # extrai as informações totais das partes
    partes = extrair(html,'partes>>>>', '<div id="partes-resumidas">')

    
    # Módulo de extração das partes
    # inserir parâmetros para extração das partes
    inicio_e_fim_dos_elementos  =[
                                 ['tipo', '<div class="detalhe-parte">', '</div>'],
                                 ['nome', '<div class="nome-parte">','&nbsp']
                                 ]
    
    marcador_para_split         = '<div class="processo-partes lista-dados">'
    
    extrair_da_string           = partes
    
    # extrai partes a partir dos parâmetros definidos
    partes = extrair_campo_lista (
                                 extrair_da_string,
                                 marcador_para_split, 
                                 inicio_e_fim_dos_elementos
                                 )
    if partes != []:
        requerente1_ap = partes[0][2][1]
        requerente1_ap = remover_acentos(requerente1_ap)
        # print (requerente1_ap)
    else:
        requerente1 = 'NA'
    
    # extrai as informações totais das partes
    andamentos = extrair(html,'andamentos>>>>', 'pauta>>>>')
    
    # Módulo de extração dos andamentos
    (andamentos_totais,
            andamentos_processados,
            andamentos_a_processar,
            ritoart12, 
            conexo, 
            baixado_em, 
            transitoemjulgado_data,
            processofindo, 
            cancelado, 
            distribuido, 
            primeirorelator,
            relatores,
            prevencao,
            protocolado, 
            autuado, 
            decisoes, 
            liminarpleno, 
            liminarmono, 
            redistribui, 
            embargos, 
            agravos,
            pautas, 
            despachos, 
            atas, 
            rito_art_12_total, 
            interlocutorias, 
            virtual, 
            pedidos, 
            julgamento,
            lista_de_links,
            modula) = extrair_andamentos (andamentos)
    
    # extrai campos do código fonte
    
    codigofonte = extrair(html,'fonte>>>>', 'partes>>>>')
    
    incidente_ap = extrair(html,'incidente" value="', '">')
    # print (incidente_ap)
    
    eletronico_fisico = extrair(codigofonte,'bg-primary">','</span>')
    
    sigilo = extrair(codigofonte,'bg-success">','</span>')
    
    nome_processo = extrair(codigofonte,'-processo" value="','">')
    
    numerounico  = extrair(codigofonte,'-rotulo">','</div>')
    
    relator = extrair(codigofonte,'Relator: ','</div>')
    relator = relator.replace('MINISTRO ','')
    relator = relator.replace('MIN. ','')
    relator = relator.strip(' ')
    if relator == '':
        relator = 'NA'
    relator = remover_acentos(relator)
    # print(relator)
    
    redator_acordao = extrair(codigofonte,'>Redator do acórdão:','</div>')
    redator_acordao = redator_acordao.replace ('MIN. ','')
    redator_acordao = remover_acentos(redator_acordao)
    
    apensado_a = extrair(codigofonte, "Apenso Principal:",'</div>' )
    if apensado_a != "NA":
        apensado_a = extrair(apensado_a,'>','<')
        apensado_a = limpar2(apensado_a)
    
    # print (f'apensado a {apensado_a}')
    
    processos_apensados = []
    apensos = extrair(codigofonte, "Processo(s) Apensado(s):",'' )
    apensos = limpar2(apensos)
    apensos = apensos.replace('&nbsp;','')
    apensos = apensos.replace(' ','')
    if 'incidente' in apensos:
        apensos = apensos.split('incidente')[1:]
        for n_apensos in range(len(apensos)):
            processo_apensado = extrair(apensos[n_apensos], '>','<')
            processos_apensados.append(processo_apensado)
            
    
    relator_ultimo_incidente = extrair(codigofonte,
                                      'Relator do último incidente:'
                                      ,'</div>')
    relator_ultimo_incidente = relator_ultimo_incidente.lstrip(' ')
    relator_ultimo_incidente = relator_ultimo_incidente.replace('MIN. ','')
    relator_ultimo_incidente = remover_acentos(relator_ultimo_incidente)
    
    # extrai campos do código fonte
    informacoes = extrair(html,'informacoes>>>>', '>>>>')
    
    assuntos = extrair(informacoes, '<ul style="list-style:none;">', '</ul>')
    if '<li>' in assuntos:
        assuntos = assuntos.replace('\n\n                        \n\n                    ','')
        assuntos = assuntos.replace('</li>', '')
        assuntos = assuntos.split('<li>')[1:]
    
    procedencia = extrair(informacoes,'<div class="col-md-12 m-t-8 m-b-8">', '<div class="col-md-7 processo-detalhes-bold p-l-0">')
    procedencia = remover_acentos(procedencia)
    
    protocolo_data = extrair(informacoes, '<div class="col-md-5 processo-detalhes-bold m-l-0">', '</div>')
    
    orgaodeorigem = extrair(informacoes, '''Órgão de Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    
    numerodeorigem = extrair(informacoes, '''Número de Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    
    origem  = extrair(informacoes, '''Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    origem = remover_acentos(origem)
                
    procedencia = extrair(informacoes, '''<span id="descricao-procedencia">''', '</span>')
    procedencia = limpar2(procedencia)
    procedencia = remover_acentos(procedencia)
    
    
    # extrai campos CC
    if 'ADI' in nomedoarquivo or 'ADPF' in nomedoarquivo or 'ADC' in nomedoarquivo or 'ADO' in nomedoarquivo:
    
        html_cc = extrair(html, 'cc>>>','')
        
        # extrai campo incidente
        incidentecc = extrair(html_cc, 'verProcessoAndamento.asp?incidente=', '">')
        
        # extrai campos classe + liminar + numero
        cln = extrair(html_cc, '<div><h3><strong>','</strong>')
            
        # extrai campo numero
        numerocc = extrair(cln, ' - ', "")
        # tratamento do campo numero
        numerocc = numerocc.replace('<FONT COLOR=RED><B>1</B></FONT>','1')
        numerocc = "0"*(4-len(numerocc))+numerocc
     
        # extrai campo liminar
        if 'Liminar' in cln:
            liminar = 'sim'
        else:
            liminar = 'não'
        
        # extrai campo classe
        classecc = extrair(cln, '', ' - ')
        classecc = extrair(classecc, '', ' (') 
        
        ## tratamento do campo classe
        classecc = classecc.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
        classecc = classecc.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
        
    ## definição de campo: origem     
        origemcc = remover_acentos(extrair(html_cc,'Origem:</td><td><strong>','</strong>'))
                
               
        ## definição de campo: incidente
        entradacc = extrair(html_cc,'Entrada no STF:</td><td><strong>','</strong>')
        
        ## definição de campo: relator
        relatorcc = extrair(html_cc,'Relator:</td><td><strong>','</strong>')
        # print (html_cc)
        relatorcc = relatorcc.replace('MINISTRA','MINISTRO')
        relatorcc = relatorcc.replace('MINISTRO ','')
        relatorcc = relatorcc.replace('MIINISTRO ','')
        relatorcc = remover_acentos(relatorcc)
        # print (relatorcc)
        
        ## definição de campo: distribuição
        distribuicao = extrair(html_cc,'Distribuído:</td><td><strong>','</strong>')
        
        
        ## definição de campo: requerente_cc
        requerente_cc = extrair(html_cc,'requerente_cc: <strong>','</strong>')
        if '(CF 103, ' in requerente_cc:
            requerente_ccsplit = requerente_cc.split('(CF 103, ')
            requerente_cc = requerente_ccsplit[0]
            requerente_cc = requerente_cc.lstrip(' ')
            requerente_cctipo = requerente_ccsplit[1]
            requerente_cctipo = requerente_cctipo.replace(')','')
            requerente_cctipo = requerente_cctipo.replace('0','')
        else:
            requerente_cctipo = 'NA'
        
        ## definição de campo: requerido
        requerido = extrair(html_cc,
                            'Requerido :<strong>',
                            '</strong>')
        
        ## definição de campo: dispositivo questionado
        dispositivoquestionado = extrair(html_cc,
                                         'Dispositivo Legal Questionado</b></strong><br /><pre>',
                                         '</pre>')
        dispositivoquestionado = limpar(dispositivoquestionado)
        
        ## definição de campo: resultado da liminar
        resultadoliminar = extrair(html_cc,
                                   'Resultado da Liminar</b></strong><br /><br />',
                                   '<br />')
        
        ## definição de campo: resultado final
        resultadofinal = extrair(html_cc,
                                 'Resultado Final</b></strong><br /><br />',
                                 '<br />')
        
        ## definição de campo: decisão monocrática final
        if 'Decisão Monocrática Final</b></strong><br /><pre>' in html_cc:
            decisaomonofinal = extrair(html_cc,
                                       'Decisão Monocrática Final</b></strong><br /><pre>',
                                       '</pre>')
            decisaomonofinal = limpar(decisaomonofinal)
        else: 
            decisaomonofinal = 'NA'
             
        ## definição de campo: fundamento    
        if 'Fundamentação Constitucional</b></strong><br /><pre>' in html_cc:
            fundamento = extrair(html_cc,
                                 'Fundamentação Constitucional</b></strong><br /><pre>',
                                 '</pre>')
            fundamento = limpar2(fundamento)
        else:
            fundamento = 'NA'
        
        ## definição de campo: fundamento
        if 'Indexação</b></strong><br /><pre>' in html_cc:
            indexacao = extrair(html_cc,
                                'Indexação</b></strong><br /><pre>',
                                '</pre>')
            indexacao = limpar2(indexacao)
            indexacao = indexacao.replace('<br />','')
        else:
            indexacao = 'NA'
    
    # extrair dados da jusrisprudência
    # extrai número de acórdãos
    
    
    (nomedoarquivo, 
     adi_decisao, 
     acordaos_publicados, 
     acordaos_adi, 
     acordaos_agr, 
     acordaos_emb, 
     acordaos_qo, 
     acordaos_outros) = extrai_acordaos_da_string (nomedoarquivo, 'ADIjuris\\')
    
    adi_decisao = limpar_decisao(adi_decisao)
    if 'MODULA' in adi_decisao:
        modulacao = 'avalia modulacao'
    else:
        modulacao = 'NA'
    
# extrai decisoes monocraticas
    (processo_mono, 
     nomedoarquivo_mono, 
     adi_decisao_mono, 
     monocraticas_publicadas, 
     monocraticas_adi, 
     monocraticas_mc,
     monocraticas_agr, 
     monocraticas_emb, 
     monocraticas_qo, 
     monocraticas_amicus,
     monocraticas_outros) = extrai_mono_da_string (nomedoarquivo, 'ADImono\\')

    # tratamento adi_decisao
    adi_decisao_mono = limpar_decisao(adi_decisao)
            
    (processo_presid, 
     nomedoarquivo_presid, 
     adi_decisao_presid, 
     presidencia_publicadas, 
     presidencia_adi, 
     presidencia_mc,
     presidencia_agr, 
     presidencia_emb, 
     presidencia_qo, 
     presidencia_amicus,
     presidencia_outros) = extrai_mono_da_string (nomedoarquivo, 'ADIpresid\\')       
    
    
    # adi_decisao_presid = limpar_decisao(adi_decisao_presid)

    decisoes_lista = []
    data_ultima_dec = 'NA'
    # print (adi_decisao)
    if adi_decisao != 'NA':
        decisoes = adi_decisao.split('DECISAO:')
        for item in range(len(decisoes)):
            decisao = decisoes[item].split('PLENARIO,')
            if len(decisao) >1:
                data_dec = decisao[1]
                data_dec = limpar2(data_dec)
                data_dec = data_dec.rstrip(' ')
                data_dec = data_dec.rstrip(' ')            
                data_dec = data_dec.rstrip('.')
                data_dec = data_dec.replace('.','/')
                
                dec = decisao[0]
                dec = dec.rstrip(' ')
                dec = dec.rstrip(' ')            
                dec = dec.rstrip('.')          
                
            decisao = [data_dec,dec]
            decisoes_lista = [decisao] + decisoes_lista
            
            if item == len(decisoes):
                data_ultima_dec = data_dec
            
            # print (len(decisoes_lista))

    # print (decisoes_lista)
    # print (decisoes) ; print (len(decisoes))
    
    
    # criação da variável dados extraídos, com uma lista de dados
    dados = [nome_processo, 
            nomedoarquivo, 
            incidente_ap, 
            apensado_a, 
            len(processos_apensados), processos_apensados,
            modula,
            requerente1_ap, 
            requerido,
            len(partes),partes, 
            eletronico_fisico, 
            sigilo,
            numerounico, 
            andamentos_totais,
            andamentos_processados,
            andamentos_a_processar,
            ritoart12, 
            conexo, 
            baixado_em, 
            transitoemjulgado_data,
            processofindo, 
            cancelado, 
            protocolado, 
            autuado, 
            distribuido, 
            len(redistribui), redistribui, 
            primeirorelator,
            relatores,
            prevencao,
            len (decisoes), decisoes, 
            len (liminarpleno), liminarpleno,
            len (liminarmono), liminarmono, 
            len (embargos), embargos, 
            len (agravos), agravos,
            len (pautas), pautas, 
            len (despachos), despachos, 
            len (atas), atas, 
            len (rito_art_12_total), rito_art_12_total, 
            len (interlocutorias), interlocutorias, 
            len (pedidos), pedidos, 
            len (julgamento), julgamento,
            len (virtual), virtual, 
            relatorcc, 
            relator, 
            redator_acordao,
            relator_ultimo_incidente, 
            assuntos, 
            procedencia, origem, origemcc,
            protocolo_data, entradacc, distribuicao, 
            orgaodeorigem, numerodeorigem, 
            liminar, 
            dispositivoquestionado, 
            resultadoliminar, 
            resultadofinal, 
            decisaomonofinal, 
            fundamento, 
            indexacao, 
            adi_decisao, 
            data_ultima_dec,
            decisoes_lista,
            modulacao,
            len(acordaos_publicados), acordaos_publicados, 
            len(acordaos_adi), acordaos_adi, 
            len(acordaos_agr), acordaos_agr, 
            len(acordaos_emb), acordaos_emb,
            len (acordaos_qo), acordaos_qo,
            len(acordaos_outros), 
            acordaos_outros, processo_mono,  
            adi_decisao_mono, 
            len(monocraticas_publicadas), monocraticas_publicadas, 
            len(monocraticas_adi), monocraticas_adi, 
            len(monocraticas_mc), monocraticas_mc,
            len(monocraticas_agr), monocraticas_agr, 
            len(monocraticas_emb), monocraticas_emb, 
            len(monocraticas_qo), monocraticas_qo, 
            len(monocraticas_amicus), monocraticas_amicus, 
            len(monocraticas_outros), monocraticas_outros, 
            processo_presid, adi_decisao_presid, 
            len(presidencia_publicadas), presidencia_publicadas, 
            len(presidencia_adi), presidencia_adi, 
            len(presidencia_agr), presidencia_agr, 
            len (presidencia_emb), presidencia_emb, 
            len (presidencia_qo), presidencia_qo, 
            len (presidencia_amicus), presidencia_amicus, 
            len (presidencia_outros), presidencia_outros, 
            lista_de_links]
    
    # print (dados)
    
    campos = '''nome_processo, 
            nomedoarquivo, 
            incidente_ap, 
            apensado_a, 
            len(processos_apensados), processos_apensados,
            modula,
            requerente1_ap, 
            requerido,
            len(partes),partes, 
            eletronico_fisico, 
            sigilo,
            numerounico, 
            andamentos_totais,
            andamentos_processados,
            andamentos_a_processar,
            ritoart12, 
            conexo, 
            baixado_em, 
            transitoemjulgado_data,
            processofindo, 
            cancelado, 
            protocolado, 
            autuado, 
            distribuido, 
            len(redistribui), redistribui, 
            primeirorelator,
            relatores,
            prevencao,
            len (decisoes), decisoes, 
            len (liminarpleno), liminarpleno,
            len (liminarmono), liminarmono, 
            len (embargos), embargos, 
            len (agravos), agravos,
            len (pautas), pautas, 
            len (despachos), despachos, 
            len (atas), atas, 
            len (rito_art_12_total), rito_art_12_total, 
            len (interlocutorias), interlocutorias, 
            len (pedidos), pedidos, 
            len (julgamento), julgamento,
            len (virtual), virtual, 
            relatorcc, 
            relator, 
            redator_acordao,
            relator_ultimo_incidente, 
            assuntos, 
            procedencia, origem, origemcc,
            protocolo_data, entradacc, distribuicao, 
            orgaodeorigem, numerodeorigem, 
            liminar, 
            dispositivoquestionado, 
            resultadoliminar, 
            resultadofinal, 
            decisaomonofinal, 
            fundamento, 
            indexacao, 
            adi_decisao,
            data ultima dec,
            decisoes,
            modulacao,
            len(acordaos_publicados), acordaos_publicados, 
            len(acordaos_adi), acordaos_adi, 
            len(acordaos_agr), acordaos_agr, 
            len(acordaos_emb), acordaos_emb,
            len (acordaos_qo), acordaos_qo,
            len(acordaos_outros), 
            acordaos_outros, processo_mono,  
            adi_decisao_mono, 
            len(monocraticas_publicadas), monocraticas_publicadas, 
            len(monocraticas_adi), monocraticas_adi, 
            len(monocraticas_mc), monocraticas_mc,
            len(monocraticas_agr), monocraticas_agr, 
            len(monocraticas_emb), monocraticas_emb, 
            len(monocraticas_qo), monocraticas_qo, 
            len(monocraticas_amicus), monocraticas_amicus, 
            len(monocraticas_outros), monocraticas_outros, 
            processo_presid, adi_decisao_presid, 
            len(presidencia_publicadas), presidencia_publicadas, 
            len(presidencia_adi), presidencia_adi, 
            len(presidencia_agr), presidencia_agr, 
            len (presidencia_emb), presidencia_emb, 
            len (presidencia_qo), presidencia_qo, 
            len (presidencia_amicus), presidencia_amicus, 
            len (presidencia_outros), presidencia_outros, 
            lista_de_links'''
    
    
    write_csv_header('ADItotal6.csv',campos, n)
    if( requerente1_ap == '' or 
       nome_processo == 'NA' or 
       requerente1_ap == 'ADV' or
       partes == [] or
       relator == 'NA'):
       print ('Processo Inexistente')
       inexistentes_csv.append(dados)
    else:   
        dados_csv.append(dados)
        
    # print (dados_csv[-1])
    if (n+1)%(100) == 0:
        write_csv_lines('ADItotal6.csv',dados_csv)
        dados_csv = []

    
write_csv_lines('ADItotal6.csv',dados_csv)
write_csv_lines('Inexistentes.csv',inexistentes_csv)
    
print ('Gravado arquivo ADItotal6.csv')