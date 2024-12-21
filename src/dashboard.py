import streamlit as st
import pandas as pd
import numpy as np
import json
import dataprev

# Cache data loading
@st.cache_data
def load_data(file_path):
    data = pd.read_parquet(file_path)
    return data
############################################################# CARGA DOS DADOS DEPUTADOS
#DEPUTADOS
dbfile = './data/deputados.parquet'
if not dbfile:
    st.error("DBFILE environment variable is not set.")
if st.session_state.get('data',None) is None:
    try:
        data = load_data(dbfile)
        st.session_state['data'] = data
    except Exception as e:
        st.error(f"Error loading data: {e}")
data_deputados = st.session_state['data']



@st.cache_data
def load_data1(file_path):
    data = pd.read_parquet(file_path)
    return data
#DESPESAS
dbfile1 = './data/serie_despesas_diárias_deputados.parquet'
if not dbfile1:
    st.error("DBFILE environment variable is not set.")
if st.session_state.get('data1',None) is None:
    try:
        data = load_data1(dbfile1)
        st.session_state['data1'] = data
    except Exception as e:
        st.error(f"Error loading data: {e}")
data_deputados_despesas = st.session_state['data1']

#df2=pd.merge(data_deputados, data_deputados_despesas, on='id', how='inner')
#df2.to_parquet('./data/serie_despesas_diárias_deputados1.parquet', engine="pyarrow", index=False)



@st.cache_data
def load_data(file_path):
    data = pd.read_parquet(file_path)
    return data
############################################################# CARGA DOS DADOS PROPOSIÇOES
#DEPUTADOS
dbfile = './data/proposicoes_deputados.parquet'
if not dbfile:
    st.error("DBFILE environment variable is not set.")
if st.session_state.get('data2',None) is None:
    try:
        data = load_data(dbfile)
        st.session_state['data2'] = data
    except Exception as e:
        st.error(f"Error loading data: {e}")
data_proposicoes = st.session_state['data2']


############################################################# VISUALIZAÇÃO

@st.cache_data
def process_ex_03():
    # 1° primeira analise
    resultado3 = dataprev.ex_03(data_deputados).text
    codigo3 = resultado3
    response_ex3 = resultado3.replace('```python',"").replace('```',"")
    
    # 2° segunda analise
    insights = dataprev.ex_03_insights(codigo3).text
    return codigo3, response_ex3, insights


def process_ex_04():
    dbfile2 = './data/serie_despesas_diárias_deputados1.parquet'
    df=pd.merge(data_deputados, data_deputados_despesas, on='id', how='inner')
    resultado4_prompt = dataprev.ex_04('prompt_chaning').text
    
    # 2° Segunda analise dos dados
    resultado4 = dataprev.ex_04_graficos(resultado4_prompt,dbfile2).text
    codigo4 = resultado4
    response_ex4 = resultado4.replace('```python',"").replace('```',"")

    #3° Insights
    insights = dataprev.ex_04_insights(codigo4).text


    return codigo4, response_ex4, resultado4_prompt, insights
    

    
def process_ex_05():
    df3=data_proposicoes[['tema','ementa']]
    resultado5 = dataprev.ex_05(df3)
    response_ex5 = resultado5.replace('```json',"").replace('```',"")
    return resultado5, response_ex5

    
def process_ex_06e07():
    #1 prompt
    resultado6=dataprev.ex_06('prompt').text
    
    #2 prompt
    resultado6_prompt = dataprev.ex_06_prompt2(resultado6).text
    response_ex06 = resultado6_prompt.replace('```python',"").replace('```',"")
    
    #3 prompt
    resultado_final = dataprev.ex_06_prompt3(response_ex06).text
    response_final = resultado_final.replace('```python',"").replace('```',"")
    
    #Exercicio 07
    resultado_final_exer07 = dataprev.ex_07(response_final).text
    response_final_exer07 = resultado_final_exer07.replace('```python',"").replace('```',"")
    
    
    return  response_final_exer07, resultado_final_exer07, resultado_final



    
def process_ex_08():
    if 'response_ex8' not in st.session_state:
        st.session_state['response_ex8'] = st.write('vazio')
    codigo = st.session_state['response_ex8']
    response_ex5 = st.session_state['response_ex8']#.replace('```python',"").replace('```',"")
    st.markdown(codigo)
    
def process_ex_09():
    if 'response_ex9' not in st.session_state:
        st.session_state['response_ex9'] = st.write('vazio')
    codigo = st.session_state['response_ex9']
    response_ex5 = st.session_state['response_ex9']#.replace('```python',"").replace('```',"")
    st.markdown(codigo)
    





############################################################# CRIANDO ABAS

with st.container():
    st.title('AT Engenharia de Prompts para Ciência de Dados')
    
    (EX_03_TAB,
    EX_04_TAB,
    EX_05_TAB,
    EX_06_TAB,
    EX_08_TAB,
    EX_09_TAB) = st.tabs(("EX_03", "EX_04", "EX_05", "EX_06 e 07", "EX_08", "EX_09"))

    with EX_03_TAB:
        if 'response_ex3' in st.session_state:
            exec(st.session_state['response_ex3'][1])
            st.markdown(st.session_state['response_ex3'][0])
            st.markdown(st.session_state['response_ex3'][2])
        elif st.button("Executar EX_03",key='ex_03_'):
            st.session_state['response_ex3'] = process_ex_03()
            exec(st.session_state['response_ex3'][1])
            st.markdown(st.session_state['response_ex3'][0])
            st.markdown(st.session_state['response_ex3'][2])

        if st.button("salvar JSON" , key="Ex_03_json"):
            with open('./data/insights_distribuicao_deputados.json', 'w', encoding='utf-8') as file:
                json.dump(st.session_state['response_ex3'][2],file, indent=4, ensure_ascii=False)
        
        
                

    with EX_04_TAB:
        if 'response_ex4' in st.session_state:
            st.markdown(st.session_state['response_ex4'][3]) # Insights
            st.markdown(st.session_state['response_ex4'][2]) # prompt com as metricas das analises
            st.markdown(st.session_state['response_ex4'][0]) # Codigo gerado LLM
            exec(st.session_state['response_ex4'][1]) # graficos
        elif st.button("Executar EX_04",key='ex_04'):
            #st.session_state['response_ex4'] = process_ex_04()
            #st.markdown(st.session_state['response_ex4'][3]) # Insights
            #st.markdown(st.session_state['response_ex4'][2]) # prompt com as metricas das analises
            #st.markdown(st.session_state['response_ex4'][0]) # Codigo gerado LLM
            #exec(st.session_state['response_ex4'][1]) # graficos
            success = False
            retries = 0

            while retries <=5 and success == False:
                try:
                    # Processa os dados novamente e armazena na sessão
                    st.session_state['response_ex4'] = process_ex_04()

                    # Exibe os dados processados
                    st.markdown(st.session_state['response_ex4'][3])  # Insights
                    st.markdown(st.session_state['response_ex4'][2])  # Prompt com as métricas das análises
                    st.markdown(st.session_state['response_ex4'][0])  # Código gerado pelo LLM
                    
                    # Tenta executar os gráficos
                    exec(st.session_state['response_ex4'][1])  # Gráficos
                    
                    # Se tudo foi executado sem erros, marca como sucesso
                    success = True
                except Exception as e:
                    retries += 1
                    st.warning(f"Tentativa {retries} falhou. Erro: {e}")
                    
                    if retries >= 5:
                        st.error("Máximo de tentativas atingido. Não foi possível concluir a execução.")
            
        if st.button("salvar JSON", key="Ex_04_json"):
            with open('./data/insights_despesas_deputados.json', 'w', encoding='utf-8') as file:
                json.dump(st.session_state['response_ex4'][3],file, indent=4, ensure_ascii=False)




    with EX_05_TAB:
        if 'response_ex5' in st.session_state:
            data = json.loads(st.session_state['response_ex5'][1])
            st.write(data['assistente']['resumo'])
        elif st.button("Executar EX_05",key='ex_05'):
            st.session_state['response_ex5']  = process_ex_05()
            data = json.loads(st.session_state['response_ex5'][1])
            st.write(data['assistente']['resumo'])
            
        if st.button("salvar JSON", key="Ex_05_json"):
            arquivo = st.session_state['response_ex5'][1]
            data = json.loads(arquivo)
            with open('./data/sumarizacao_proposicoes.json', 'w', encoding='utf-8') as file:
                json.dump(data,file, indent=4, ensure_ascii=False)
            
            

    with EX_06_TAB:
        if 'response_ex6' in st.session_state:
            exec(st.session_state['response_ex6'][0])
            
            st.write('Codigo Chain-of-thoughts')
            st.write(st.session_state['response_ex6'][1])
            
            st.write('Codigo Batch-prompting')
            st.write(st.session_state['response_ex6'][2])
        elif st.button("Executar EX_06",key='ex_06'):
            success = False
            retries = 0
            
            while retries <=5 and success == False:
                try:
                    # Processa os dados novamente e armazena na sessão
                    st.session_state['response_ex6'] = process_ex_06e07()
                    
                    # Exibe os dados processados
                    exec(st.session_state['response_ex6'][0])
                    
                    st.write('Codigo Chain-of-thoughts')
                    st.write(st.session_state['response_ex6'][1])
                    
                    st.write('Codigo Batch-prompting')
                    st.write(st.session_state['response_ex6'][2])
                    
                    success = True
                except Exception as e:
                    retries += 1
                    st.warning(f"Tentativa {retries} falhou. Erro: {e}")
                    
                    if retries >= 5:
                        st.error("Máximo de tentativas atingido. Não foi possível concluir a execução.")


######################################## Exercicio 07


    with EX_08_TAB:
        if st.button("Executar EX_08"):
            process_ex_08('prompt')


    with EX_09_TAB:
        if st.button("Executar EX_09"):
            process_ex_09('prompt')
