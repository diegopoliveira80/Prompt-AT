import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
import tools
import dashboard
from summarizer import ChunkSummary
from dotenv import load_dotenv
load_dotenv()

################################
# EXECUÇÃO DAS FUNÇÕES
REQUEST_DEPUTADOS = False
REQUEST_DESPESAS = False
REQUEST_PROPOSICOES = False


################################
# EX_03 GRAFICO DE PIZZA
EX_03 = True
EX_04 = True
EX_05 = True
EX_06 = True
EX_07 = True

################################ 
# REQUEST DOS DADOS
# SALVAMENTO DOS DADOS DIRETORIO DATA

if REQUEST_DEPUTADOS:
    def api_request(deputados,inicio,fim):
        url = f'{deputados}?dataInicio={inicio}&dataFim={fim}&ordem=ASC&ordenarPor=nome'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

    df=api_request(deputados='https://dadosabertos.camara.leg.br/api/v2/deputados',
                  inicio='2024-08-01',
                  fim='2024-08-30')
    
    df = pd.json_normalize(df['dados'])
    df.to_parquet('./data/deputados.parquet', engine="pyarrow", index=False)
    

################################ 
# REQUEST DOS DADOS DE DESPESAS
# SALVAMENTO DOS DADOS DIRETORIO DATA

if REQUEST_DESPESAS:
    def deputados(dbfile):
        #dbfile = './data/deputados.parquet'
        data = pd.read_parquet(dbfile)
        id = data['id'].tolist()
        return id        
        
        
    def api_request_despesas(deputados,cod,ano,mes):
        lista = []
        for num in cod:
            url = f'{deputados}{str(num)}/despesas?ano={ano}&mes={mes}&ordem=ASC&ordenarPor=ano'
            response = requests.get(url)
            if response.status_code == 200:
                response = response.json()['dados']
                deputado = [{**i, 'id': num} for i in response]
                lista.append(deputado)
            else:
                raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")
        return lista

    df2=api_request_despesas(deputados='https://dadosabertos.camara.leg.br/api/v2/deputados/',
                    cod=deputados(dbfile = './data/deputados.parquet'),
                    ano='2024',
                    mes='8')
    
    flat_list = [item for sublist in df2 for item in sublist]
    df2 = pd.DataFrame(flat_list)
    df2.to_parquet('./data/serie_despesas_diárias_deputados.parquet', engine="pyarrow", index=False)
    
    

################################ 
# REQUEST DOS DADOS PROPOSICOES
# SALVAMENTO DOS DADOS DIRETORIO DATA

if REQUEST_PROPOSICOES:
    def api_request_proposicoes(deputados,inicio,fim,cod_temas):
        lista = []
        for num in cod_temas:
            url = f'{deputados}?dataInicio={inicio}&dataFim={fim}&codTema={num}&ordem=ASC&ordenarPor=id'
            response = requests.get(url)
            if response.status_code == 200:
                response = response.json()['dados']
                proposicoes = [{**i,    'id': num,
                                        'tema': ('Economia' if num == 40 else 
                                                'Educação e Ciência' if num == 46 else 
                                                'Tecnologia e Inovação' if num == 62 else 'Outro')} for i in response]
                lista.append(proposicoes)
            else:
                raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")
        return lista

    df3=api_request_proposicoes(deputados='https://dadosabertos.camara.leg.br/api/v2/proposicoes',
                                inicio='2024-08-01',
                                fim='2024-08-31',
                                cod_temas = [40,46,62])
    
    flat_list = [item for sublist in df3 for item in sublist]
    df3 = pd.DataFrame(flat_list)
    df3.to_parquet('./data/proposicoes_deputados.parquet', engine="pyarrow", index=False)
    
    
    
################################ EX_03
if EX_03:
    def ex_03(deputados):
        partidos_count = deputados['siglaPartido'].value_counts()
        
        system_prompt = f"""
            Preciso que crie um codigo em pyhton que leia os dados de um dataframe de partidos e o total de
            candidatos por partido e gere um grafico de pizza com o total e o percentual de deuputados por partido.

            - Apenas o codigo, sem instruções
            - O codigo precisa ser no formato para streamlit
            - o grafico de pizza precisa ter percentual e total de deputados por partido

            {partidos_count}
            """
        generation_config = {
                'temperature': 0.6,
                'max_output_tokens': 1000
            }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=system_prompt,
                generation_config = generation_config
            )

        return model.llm_ex_03(system_prompt)
    
    
    def ex_03_insights(insights):
        system_prompt = f"""
            Você é um analista de dados que precisa analisar e extrair insights dos dados sobre a distribuição de 
            partidos {insights} e como isso influencia a câmara dos deputados.
            
            - não utrapassar a 200 tokens
            - trazer no maximo 3 topicos de insights
            - insights importantes
            
            exemplo de resposta:
            1°
            2°
            3°
            """
            
        generation_config = {
                'temperature': 0.6,
                'max_output_tokens': 500
            }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=system_prompt,
                generation_config = generation_config
            )
        
        
        return model.llm_ex_03(system_prompt)


################################ EX_04
if EX_04:
    def ex_04(prompt_chaning):
        prompt_chaning = f"""
        Você é um cientista de dados especializado em analisar conteúdos de despesas. Os dados são destinados a gastos gerados pelos deputados.
        Todos os dados estão no arquivo DataFrame:

        - dataDocumento: data da despesa
        - nome: nome do deputado
        - tipoDespesa: descrição da despesa
        - valorDocumento: valor realizado na despesa

        Gere uma lista de 3 análises que podem ser implementadas com base nos dados disponíveis, em um arquivo JSON:
        {[
            {'Nome':'nome da análise',
            'Objetivo': 'o que precisamos analisar',
            'Método': 'como vamos analisar isso'
            }
        ]
        }
        """
        
        generation_config = {
                'temperature': 0.6,
                'max_output_tokens': 500
            }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=prompt_chaning,
                generation_config = generation_config
            )
        
        return model.llm_ex_04(prompt_chaning)
        

        
    def ex_04_graficos(resultado4_prompt,deputados_despesas):
        system_prompt = f"""
        Você é um cientista de dados especializado em analisar conteúdos de despesas. Os dados são destinados a gastos gerados pelos deputados.
        Todos os dados estão no caminho {deputados_despesas}, abra o diretorio e crie os visuais no formato "STREAMLIT"
        com as seguintes colunas:
        
        - dataDocumento: data da despesa
        - nome: nome do deputado
        - tipoDespesa: descrição da despesa
        - valorDocumento: valor realizado na despesa
        
        Implemente a análise descrita abaixo em Python.
        Saída somente o código, sem explicações.
        ## ANÁLISE
        {resultado4_prompt}
        - Apenas 1 grafico por objetivo
        """
            
        generation_config = {
                'temperature': 0.6,
                'max_output_tokens': 1000
            }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=system_prompt,
                generation_config = generation_config
            )
            
        return model.llm_ex_04(system_prompt) 

    
    def ex_04_insights(insights):
        system_prompt = f"""
        Você é um analista de dados que precisa analisar e extrair insights dos dados sobre as despesas de 
        gastos dos deputados, conforme os dados apresentados: {insights} gere alguns insights.
        
        - não utrapassar a 200 tokens
        - trazer no maximo 3 topicos de insights
        - insights importantes
        
        exemplo de resposta:
        1°
        2°
        3°
        """
        generation_config = {
                'temperature': 0.6,
                'max_output_tokens': 1000
            }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=system_prompt,
                generation_config = generation_config
            )
        return model.llm_ex_04(system_prompt)
    
    
    
################################ EX_05

if EX_05:
    def ex_05(proposicoes):
        df = proposicoes
        df['prompt'] = 'Tema :' + df['tema'] + '- Assunto: ' + df['ementa']
        
        system_prompt = f"""
        Você é um assistente editor da camera focado em projetos de lei, resoluções, medidas provisórias, 
        emendas, pareceres e todos os outros tipos de proposições na Câmara.
        Você receberá dados reais no seguinte formato:
        <tema: assunto>
        """
        user_prompt = f"""
        Você deve criar um resumo das ementa, destacando os pontos principais.
        Certifique-se de descrever os seguintes aspectos:
        1. Tema: Principais informações.
        2. 3 topicos sendo ('Economia', 'Educação' e 'Ciência, Tecnologia e Inovação')
        """
        
        ementa_summarizer = ChunkSummary(
        model_name = "gemini-1.5-pro",
        apikey = os.getenv("GEMINI_API_KEY_PRO"),
        text = df['prompt'].tolist(),
        window_size = 15,
        overlap_size = 10,
        system_prompt=system_prompt,
    )

        proposicoes_summary = ementa_summarizer.summarize(user_prompt)
        return proposicoes_summary


################################ EX_06
if EX_06:
    def ex_06(prompt1):
        prompt1 = f"""
        criar um codigo com streamlit. 
        Escrever o código criando as abas Overview, Despesas e Proposições
        Não é necessario import streamlit
        Na aba overview descrever:
        - Titulo: Streamlit via PLN
        - Objetivo: Criar aplicação streamlit utilizando PLN, sera capaz de ler diretorio de dados e apresentar
        os dados nas abas  Despesas e Proposições
        Escrever somente o codigo, sem explicação.
        """
        
        generation_config = {
        'temperature': 0.6,
        'max_output_tokens': 1000
    }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=prompt1,
                generation_config = generation_config
            )
        return model.llm_ex_06(prompt1)
    
    def ex_06_prompt2(prompt1):
        sumarizacao = './data/config.yaml'
        prompt2 = f"""
        Com o primeiro prompt: <{prompt1}>. adicione na aba Overview o conteudo do diretorio: {sumarizacao} 
        que está no formato yaml e utf-8.
        - Escrever somente o codigo, sem explicação.
        """
        
        generation_config = {
        'temperature': 0.6,
        'max_output_tokens': 1000
    }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=prompt2,
                generation_config = generation_config
            )
        return model.llm_ex_06(prompt2)
    
    def ex_06_prompt3(prompt2):
        img = './docs/distribuicao_deputados.png'
        deputados = './data/insights_distribuicao_deputados.json'
        prompt3 = f"""
        Com prompt: <{prompt2}>. Adicione na aba Overview o conteudo do diretorio: {img} 
        que está no formato png<imagem>.
        Adicione na aba Overview o conteudo do diretorio: {deputados} 
        que está no formato JSON.
        - Escrever somente o codigo, sem explicação.
        """
        
        generation_config = {
        'temperature': 0.6,
        'max_output_tokens': 1000
    }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=prompt3,
                generation_config = generation_config
            )
        return model.llm_ex_06(prompt3)
    
    
    
################################ EX_07
if EX_07:
    def ex_07(prompt1):
        deputados = './data/insights_distribuicao_deputados.json'
        dbfile = './data/serie_despesas_diárias_deputados1.parquet'
        df_proposicoes = './data/proposicoes_deputados.parquet'
        summary_proposicoes = 'data/sumarizacao_proposicoes.json'
        prompt1 = f"""
        Com a tecnica Batch-prompting preciso que você realize todas as etapas aseguir:
        Com prompt: <{prompt1}>.
        1. Adicione na Aba Despesas o conteudo di duretorio: {deputados}
        2. A aba despesas deve conter um st.selectbox da coluna nome que esta no diretorio: {dbfile}
        3. Agora adicione na Aba Despesas o gráfico de barras com a série temporal na coluna "dataDocumento" e  
        o valor da coluna "valorDocumento" conforme deputado selecionado no st.selectbox
        4. Na aba proposicoes abra o diretorio {df_proposicoes} no formato DataFrame 
        5. Na ana proposicoes abra o diretorio {summary_proposicoes}
        - Trate os dados codificado como UTF-8
        - Não use set_page_config()
        - Escrever somente o codigo, sem explicação.
        """
        
        generation_config = {
        'temperature': 0.6,
        'max_output_tokens': 1000
    }
        model = tools.Gemini(
                model_name = "gemini-1.5-pro",
                apikey = os.getenv("GEMINI_API_KEY_PRO"),
                system_prompt=prompt1,
                generation_config = generation_config
            )
        return model.llm_ex_07(prompt1)
    