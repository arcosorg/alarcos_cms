from datamining import extrair, limpar, limpar2, remover_acentos

def convertedata (string):
    if len(string)==10:
        string = string[6:]+string[3:5]+string[0:2]
        string = int(string)
        return string
    else:
        return string
    

def extrair_andamentos (string):
    # define o número de elementos a serem extraídos
    n_elementos= string.count('<div class="andamento-item">') 
    
    # cria uma lista (dados) com os dados da string, segmentada no split
    
    string = remover_acentos(string)
    string = string.split('<div class="andamento-item">')
    andamentos_string = string[1:]
    
    # imprime o número de elementos a serem extraídos
    # print (str(n_elementos) + ' elementos')
    
    #define a lista que será retornada como resultado
    andamentos_processados = []
    andamentos_totais = []
    andamentos_a_processar = []
    lista_de_links = []
    decisoes = []
    modula = []
    liminarpleno = []
    liminarmono = []
    redistribui = []
    embargos = []
    agravos = []
    pautas = []
    despachos = []
    atas = []
    rito_art_12_total = []
    interlocutorias = []
    virtual = []
    pedidos = []
    julgamento = []
    relatores = []
    baixado_em = 'NA'
    transitoemjulgado_data = 'NA'
    processofindo = 'NA'
    cancelado = 'NA'
    distribuido = 'NA'
    primeirorelator = 'NA'
    prevencao = 'NA'
    protocolado = 'NA'
    autuado = 'NA'
    conexo = 'NA'
    ritoart12 = 'NA'

    
    # iteração sobre cada um dos n elementos
    for item in range(n_elementos):
        
    

        docs = 'NA'
        
        filtrar = False
        
        andamento_string = andamentos_string[item]
        
        # carrega na variável campo um elemento de cada vez
        ordem = str(n_elementos - item)
     
        
            # lista_inicio_fim=   [
            #             ['data','<div class="andamento-data ">','</div>'],
            #             ['nome','<h5 class="andamento-nome ">','</h5>'],
            #             ['complemento','<div class="col-md-9 p-0','</div>'],
            #             ['julgador','julgador badge bg-info ">','</span>']
            #             ['docs','"col-md-4 andamento-docs">','</div>'],
            #             ,                          
            #             ]
        
        # define campo data
        data = extrair(andamento_string,'<div class="andamento-data ">','</div>').upper()
        data = limpar2(data)
        
        # define campo nome
        nome = extrair(andamento_string,'<h5 class="andamento-nome ">','</h5>').upper()
        nome = limpar2(nome)
        nome = nome.replace('JULG. ','JULGAMENTO ')
        nome = nome.replace('  ', ' ')
        nome = nome.replace('JULGAMENTO NO PLENO', 'JULGAMENTO DO PLENO')
        nome = nome.replace('JULG. POR DESPACHO - ', 'JULGAMENTO POR DESPACHO')
        nome = nome.replace('DECISAO DA RELATORA', 'JULGAMENTO POR DESPACHO')
        nome = nome.replace('DECISAO DO RELATOR', 'JULGAMENTO POR DESPACHO')
        nome = nome.replace('DECISAO DO(A) RELATOR(A) - ', 'JULGAMENTO POR DESPACHO')
        nome = nome.replace('DECISAO DO(A) RELATOR(A) - ', 'JULGAMENTO POR DESPACHO')
        nome = nome.replace('JULGAMENTO POR DESPACHO - ', 'JULGAMENTO POR DESPACHO')
        nome = nome.replace('JULGAMENTO DO PLENO - ', 'JULGAMENTO DO PLENO')
        nome = nome.replace('JULGAMENTO DO PLENO ', 'JULGAMENTO DO PLENO')
        nome = nome.replace('DECISAO DA PRESIDENCIA - ', 'DECISAO DA PRESIDENCIA')
        nome = nome.replace('DO RELATOR NO PL','')
        nome = nome.replace('CONEXAO COM O PROCESSO Nº', 'CONEXAO')
        nome = nome.replace('CONEXAO PROC. N.', 'CONEXAO')
        nome = nome.replace('DECISAO LIMINAR - ', 'LIMINAR')
        nome = nome.replace('LIMINAR POR DESPACHO','LIMINAR JULGADA POR DESPACHO')
        nome = nome.replace('LIMINAR JULGAMENTO POR DESPACHO','LIMINAR JULGADA POR DESPACHO')
    
        # define campo complemento
        complemento = extrair(andamento_string,'<div class="col-md-9 p-0','</div>').upper()
        complemento = limpar(complemento)
        
        # define campo julgador
        julgador = extrair(andamento_string,'julgador badge bg-info ">','</span>').upper()
        julgador = limpar(julgador)
        
        # define campo decisao_tipo        
        if 'MIN.' in julgador:
            decisao_tipo = 'MONOCRATICA'
            julgador = julgador.replace('MIN. ','')
        else:
            decisao_tipo = 'VER'
            
        #define campo docs
        docs = extrair(andamento_string,'col-md-4 andamento-docs">','</div>')
        docs = docs.replace('\n','')
        docs = docs.replace('\t','')
        docs = docs.replace(' ','')
        
        if 'href' in docs:
            link = extrair(docs,'href="','"target=')
            link = 'http://portal.stf.jus.br/processos/'+link
            docs = extrair(docs,'</i>','</a>')
            lista_de_links.append([ordem, docs, link])
        else:
            link = 'NA'
            docs = 'NA'
     
        # composicao do andamento
        andamento = [ordem, data, nome, complemento, julgador, decisao_tipo, docs, link]
        
        # processa andamentos
        if 'JULGAMENTO DO PLENO' in nome:
            nome = nome.replace('JULGAMENTO DO PLENO','')
            decisao_tipo = 'PLENO'
            
        if 'JULGAMENTO POR DESPACHO' in nome and julgador == '':
            nome=nome.replace('JULGAMENTO POR DESPACHO','')
            decisao_tipo = 'MONOCRATICA'

        if 'LIMINAR JULGADA PELO PLENO - ' in nome:
              nome = nome.replace('LIMINAR JULGADA PELO PLENO - ','')
              decisao_tipo = 'PLENO'
              
        if 'LIMINAR JULGADA POR DESPACHO - ' in nome:
              nome = nome.replace('LIMINAR JULGADA POR DESPACHO - ','')
              decisao_tipo = 'MONOCRATICA'
              
        if 'DECISAO DA PRESIDENCIA' in nome:
              decisao_tipo = 'PRESIDENCIA'

        if nome == 'DEFERIDA':
            nome = nome.replace('DEFERIDA','LIMINAR DEFERIDA')       
        
        if nome == 'DEF. EM PARTE':
            nome = nome.replace('DEF. EM PARTE','LIMINAR DEFERIDA EM PARTE')

        if 'NAO VERIFICO NA ESPECIE A PRESENÇA DE PERICULUM IN MORA' in complemento and nome == '':
            nome = 'LIMINAR INDEFERIDA'
            
        if 'COLHAM-SE, PRIMEIRAMENTE, AS MANIFESTAÇOES' in complemento and nome == '':
            nome = 'VISTA AO AGU'
            
        if 'NEGO SEGUIMENTO À INICIAL' in complemento:
            nome = 'NEGADO SEGUIMENTO'
            
        if 'ANTE O EXPOSTO, NEGO SEGUIMENTO A PRESENTE ACA0' in complemento:
            nome = 'NEGADO SEGUIMENTO'
            
        if 'INDEFIRO LIMINARMENTE O PEDIDO' in complemento:
            nome = 'INDEFERIDA A INICIAL'        
   
        # rito art. 12
        if ('RITO' in complemento and
            '12' in complemento and 
            'ART' in complemento):
            ritoart12 = data
            nome = 'LIMINAR INDEFERIMENTO IMPLICITO (RITO ART. 12)'
            rito_art_12_total.append(andamento)
        elif ('ADOTADO RITO DO ART. 12, DA LEI 9.868/99' in nome):
                ritoart12 = data
                nome = 'LIMINAR INDEFERIMENTO IMPLICITO (RITO ART. 12)'
                rito_art_12_total.append(andamento)   
                
# acrescenta o elemento extraído na lista que compõe o campo
        andamentos_totais.append(andamento)
        
#     filtrar andamentos sem interesse para a pesquisa
        
        if ('RETIFICAÇAO DE AUTUAÇAO' in nome or 
                'LANÇAMENTO INDEVIDO' in nome or 
                'AMENTO INDEVIDO' in nome or 
                'CONVERTIDO EM ELET' in nome or 
                'APENSADO' in nome or 
                'APENSACAO' in nome or
                'DETERMINADA A REDISTRIB' in nome or
                'DETERMINADA CITACAO' in nome or
                'DETERMINADA INTIMACAO' in nome or
                nome[:7] == 'CONCLUS' or 
                'CONCLUSOS' in nome or 
                nome == 'CONCLUSAO' or 
                nome[:5] == "AUTOS" or 
                'REMESSA DOS autos' in nome or 
                'COBRADA A DEVOLU' in nome or
                nome == 'CERTIDAO' or 
                nome == 'PETICAO' or 
                'ARQUIVADA A PET' in nome or 
                nome == 'CIENCIA' or 
                nome == 'CIENTE' or
                nome[:9] == 'COMUNICAD' or 
                nome[:6] == 'INTIMA' or 
                'COMUNICACAO ASSINAD' in nome or
                'INFORMACOES PRESTADAS' in nome or
                'JUNTADA' in nome or 
                'DEVOLUÇAO DE' in nome or
                'VISTA A PGR' in nome or 
                'RECEBIMENTO DOS' in nome or 
                'MANIFESTACAO DA' in nome or
                nome == 'PETICAO AVULSA' or 
                nome == 'PETICAO' or 
                'DESENTRANHAMENTO' in nome or 
                'RECEBIMENTO EXTERNO DOS AUTOS' in nome or
                nome == 'VISTA AO AGU' or
                'PUBLICADA, DJ' in nome or 
                'JULGAMENTO PUBLICADA' in nome 
                or 'DECISAO PUBLICADA' in nome or 
                'DECISAO PUBLICADA' in nome or 
                nome == 'DECISAO PUBLICADA, DJ:' or 
                'PUBLICADA NO D' in complemento or 
                'PUBLICADA NO D' in nome or 
                'REPUBLICAD' in nome or
                nome == 'REMESSA DOS AUTOS' or
                nome == 'REMESSA' or
                'AUTOS DEVOLVIDOS' in nome or
                nome[:7] == 'INFORMA' or
                nome[:7] == 'PUBLICA' or
                nome == 'VIDE' or
                nome == 'ACORDAO N.:'or
                nome == 'REMESSA:' or
                nome == 'REMESSA' or
                nome == 'AUTOS COM:' or
                'EXPEDIDO' in nome or
                nome[:7] == 'PUBLICA' or
                'COMUNICADA D' in nome or
                nome[:8] == 'COMUNICA' or
                'INFORMACOES RECEBIDAS' in nome or
                nome == 'EXPEDIDO OFICIO nº' or
                nome[:6] == 'EXPEDI' or
                andamento_string.find('class="andamento-nome andamento-invalido"') > 0
                # or (nome == 'PUBLICADO ACORDAO, DJ:' and link == "")
            ):
                filtrar = True
 
    
        # Incorporando a outros campos informações de andamentos
        # e depois excluindo das decisões
        if nome[:7]=='CONEXAO':
            conexo = complemento
            filtrar = True

        if nome[:5] == "BAIXA":
            baixado_em = data
            filtrar = True

        if (nome == 'DECORRIDO O PRAZO' or
            nome == 'TRANSITADO EM JULGADO' or
            nome == "TRANSITADO(A) EM JULGADO"):
            transitoemjulgado_data = data 
            filtrar = True

        
        if ('REAUTUADO' in nome or 
            'CANCELAMENTO DE AUTUA' in nome or 
            'IMPOSSIBILIDADE DE PROCESSAMENTO' in nome):
            cancelado = 'Sim'
            filtrar = True

        if (nome == 'DISTRIBUIDO' or 
            nome == 'REGISTRADO'):
            distribuido = data
            primeirorelator = complemento
            primeirorelator = primeirorelator.replace('MIN. ','')
            relatores.append([ordem, data, primeirorelator])
            filtrar = True
            
        if (nome == 'REGISTRADO A PRESIDENCIA' or 
            nome == 'REGISTRADO'):
            distribuido = data
            primeirorelator = 'PRESIDENTE'
            filtrar = True
            
        if (nome == 'DISTRIBUIDO POR PREVENCAO'):
            distribuido = data
            primeirorelator = complemento
            prevencao = "PREVENÇÃO"
            relatores.append([ordem, data, primeirorelator])
            filtrar = True
            
        if (nome == 'DISTRIBUIDO/EXCLUSAO DE MINISTRO' or 
            'DISTRIBUIDO POR EXCLUS' in nome):
            distribuido = data
            ministroexcluido = complemento
            ministroexcluido = ministroexcluido.replace("MIN. ",'')
            prevencao = "PREVENÇÃO"
            filtrar = True            
            
        if nome == 'PROTOCOLADO':
            protocolado = data 
            filtrar = True
            
        if nome == 'AUTUADO':
            autuado = data 
            filtrar = True
            
        if nome == 'PROCESSO FINDO':
            processofindo = data
            filtrar = True
            
    #identifica decisoes secundárias
        # questoes de ordem
        if (nome == 'QUESTAO DE ORDEM' or 
            'DECISAO INTERLOCUTORIA' in nome or 
            nome[:8] == 'DETERMINAD'):
            interlocutorias.append(andamento)
            filtrar = True
            
        if 'ATA DE JULGAMENTO' in nome:
            atas.append(andamento)
            filtrar = True
            
        if 'JULGAMENTO VIRTUAL' in nome:
            virtual.append(andamento)
            filtrar = True    
            
        if ('REDISTRIBUIDO' in nome or 
            'SUBSTITUICAO DO RELATOR' in nome):
            if complemento[0:3] == 'MIN':
                redistribui.append(andamento)
                complemento = complemento.replace('MIN. ','')
                relatores.append([ordem,data,complemento])
                filtrar = True
            
        if ('EMBARGOS' in nome or 
            'INTERPOSTOS' in nome):
            embargos.append(andamento)
            filtrar = True
            
        if  ('DETERMINADA DILI' in nome or 
            'DESPACHO ORDINATORIO' in nome or 
            nome == 'DESPACHO' or 
            nome[:8] == 'DESPACHO'):
            despachos.append(andamento)
            filtrar = True
            
        if ('AGRAVO ' in nome or 
            'INTERPOSTO ' in nome or 
            'HOMOLOGADA A DESISTENCIA' in nome or 
            nome == 'REJEITADO'):
            agravos.append(andamento)
            filtrar = True
            
        if  ('RETIRADO DA MESA' in nome or 
                nome == 'ADIADO O JULGAMENTO' or 
                'NA LISTA DE JULGAMENTO' in nome or 
                'PROCESSO A JULGAMENTO' in nome or 
                'PAUTA' in nome or 
                'CALENDARIO' in nome or 
                'DIA PARA JULGAMENTO' in nome or 
                'EM MESA PARA' in nome or 
                'PAUTA' in nome or 
                'EM MESA' in nome or 
                'DE MESA' in nome or 
                'COM DIA PARA JULGAMENTO' in nome):
            pautas.append(andamento)
            filtrar = True
            
        if ('PEDIDO DE LIMINAR' in nome or 
                'REQUERIDA TUTELA PROVISORIA' in nome):
            pedidos.append(andamento)
            filtrar = True
            
        if ('MODULA' in nome or 'MODULA' in complemento):
            modula.append(andamento)
            
            
        #cria listas sem filtrar
        # rito art. 12
        if ('RITO' in complemento and
            '12' in complemento and 
            'ART' in complemento):
            ritoart12 = data
            nome = 'LIMINAR INDEFERIMENTO IMPLICITO (RITO ART. 12)'
            rito_art_12_total.append(andamento)
        elif ('ADOTADO RITO DO ART. 12, DA LEI 9.868/99' in nome):
                ritoart12 = data
                nome = 'LIMINAR INDEFERIMENTO IMPLICITO (RITO ART. 12)'
                rito_art_12_total.append(andamento)   
                
        # identifica decisoes liminares
        if nome == 'LIMINAR JULGADA PELO PRESIDENTE - ':
            nome = nome.replace('LIMINAR JULGADA PELO PRESIDENTE - ','')
            julgador = "PRESIDENTE"
            decisao_tipo= "PRESIDENCIA"
            liminarmono.append(andamento)
            filtrar = True
            
        # identifica andamentos sobre o julgamento que nao constituem decisao
        if ('VISTA - DEVOLU' in nome or 
                'SUSPENSO O JULGAMENTO' in nome or 
                'VISTA RENOVADA' in nome or 
                'VISTA A MINISTRA' in nome or 
                'VISTA AO MINISTRO' in nome):
            julgamento.append(andamento)
            filtrar = True

        # identifica e organiza as decisões liminares
        if filtrar == False:   
            if (nome[:7] == 'LIMINAR' or
                    "AD REFERENDUM" in nome or 
                    'AD REFERENDUM' in complemento):
                if 'PLENO' in julgador:
                    nome = nome.replace('LIMINAR ','')
                    nome = nome.replace('DE LIMINAR','')
                    nome = nome.replace('LIMINAR','')
                    nome = nome.replace('JULGAMENTO PELO PLENO - ','')
                    nome = nome.replace('JULGAMENTO PLENO - ','')
                    nome = nome.replace('PELO PLENO','')
                    decisao_tipo = 'PLENO'
                    liminarpleno.append(andamento)
                    filtrar = True
                else:
                    nome = nome.replace('LIMINAR ','')
                    nome = nome.replace('DE LIMINAR','')
                    nome = nome.replace('LIMINAR','')
                    nome = nome.replace('AD REFERENDUM','')
                    decisao_tipo = 'MONOCATICA'
                    if ' JULGADA PELO PRESIDENTE - ' in nome:
                        nome = nome.replace('JULGADA PELO PRESIDENTE - ','')
                        julgador = "PRESIDENTE"
                        decisao_tipo= "PRESIDENCIA"
                    liminarmono.append(andamento)
                    filtrar = True
                    
        if julgador != "" and filtrar == False:
            if 'EMBARGOS' in nome:
                    embargos.append(andamento)
                    filtrar = True
            else:
                    if 'AGRAVO ' in nome:
                        agravos.append(andamento)
                        filtrar = True
                    else: 
                        if 'QUESTAO DE ORDEM' in nome:
                            interlocutorias.append(andamento)
                            filtrar = True
                        else:
                            decisoes.append(andamento)
                            filtrar = True
                        

        if filtrar == False:
            if  ('NEGADO SEGUIMENTO' in nome or
                    'FIXADA A  TESE' in nome or
                    'DECLARADA A INCONSTITUCIONALIDADE ' in nome or
                    nome == 'ARQUIVADO' or
                    nome == 'ADITAMENTO A DECISAO'or
                    decisao_tipo == 'MONOCRATICA' or
                    nome =='PREJUDICADO' or
                    'SUSPENSO O JULGAMENTO' in nome or
                    'RECONSIDERACAO' in nome or
                    'EXTINTO O PROCESSO' in nome or
                    'DECISAO DA PRESI' in nome or
                    'DECISAO DA REL' in nome or
                    'RETIFICACAO NO PLENO' in nome or
                    'INICIADO JULGAMENTO VIRTUAL' in nome or
                    'FINALIZADO JULGAMENTO VIRTUAL' in nome or
                    nome[:4] == 'JULG' or
                    'ADIADO O JULGAMENTO' in nome or
                    nome[:10] == 'DECISAO DO'):
                nome = nome.replace('DECISÃO DA PRESIDÊNCIA - ','')
                decisoes.append(andamento)
                filtrar = True

 

        
        # print (andamentos_a_processar)
        # print (lista_de_links)
        if filtrar == True:
            andamentos_processados.append(andamento)
        else:
            andamentos_a_processar.append(andamento)    
    
    # retorna a lista de elementos como resultado função
    return (andamentos_totais,
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
            modula)
