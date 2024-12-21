# Descrição do projeto e objetivo.
O objetivo do projeto é disponibilizar uma ferramente com dados dos principais campeonatos de futebol, com dados da liga, temporada, partida e statisticas de cada jogador. 
Tambem uma integração com LLM para ser capaz não apenas de trazer os dados da partida mas também dizer o que aconteceu naquela partida, o comparativo entre os jogadores escolhido.
url: https://dadosabertos.camara.leg.br/swagger/api.html


📂 projeto 
├── 📂 data # Contém os conjuntos de dados utilizados no projeto 
├── 📂 docs # Documentação do projeto 
├── 📂 src # Código-fonte principal do projeto 
│ ├── dashboard.py  # Arquivo de visualização
│ ├── dataprev.py   # Funções execultadas
│ ├── ex_01.ipunb   # Exercicio 01
│ ├── summarizer.py # Aplicação de sumarização de textos
│ └── tools.py      # Aplicação LLMs
├── .env # Configurações de ambiente (ex.: credenciais, variáveis) 
├── venv # Ambiente virtual
├── .gitignore # Arquivo para ignorar arquivos no controle de versão 
├── README.md # Documentação principal do projeto
└── requirements.txt # Dependências necessárias para executar o projeto
 

# Instruções para configurar o ambiente e executar o código.
1. Execultar o download da aplicação no github https://github.com/diegopoliveira80/Prompt-AT
2. Salvar a aplcação em um diretorio separado
3. Abrir pasta AT em um notebook
4. Criar ambiente virtual para receber as instalações das bibliotecas necessarias
```bash
python -m venv venv
```

5. Ativar o ambiente
```bash
venv/scripts/activate
```

6. Instalar dependências requirements.txt
```bash
pip install -r requirements.txt
```

7. Criar arquivo .env e inserir API_KEY GEMINI para funcionamento do LLM conforme estrutura mencionada acima
comando para ios ou windows
```bash
GEMINI_API_KEY_PRO=your-api-key-here
```

8. Desative o ambiente virtual quando terminar
```bash
venv/scripts/deactivate
```

9. Iniciar streamlit run src/dashboard.py no terminal para visualizar o front-end
```bash
streamlit run src/dashboard.py
```

Após o passo a passo acima a aplicação estará funcionando em seu localhost

# Exemplos de entrada e saída das funcionalidades.



# Conclusão
A aplicação foi desenvolvida com o objetivo de trazer experiencias com LLMs, utilizando alguns prompts instruindo a LLM a abrir dados de uma API e realizar diversas analises que a propria LLM indicar.
