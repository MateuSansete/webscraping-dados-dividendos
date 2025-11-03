import pandas as pd
from selenium import webdriver
#  MUDANÇA PARA EDGE 
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

from time import sleep
from io import StringIO
import sys

# URL da página de proventos
url = 'https://statusinvest.com.br/acoes/proventos'

print(f"Iniciando a extração com Selenium para: {url} usando o Microsoft Edge...")

driver = None

try:
    # 1. Configura o serviço do Edge
    service = EdgeService(EdgeDriverManager().install())
    
    # 2. Configura as opções do navegador Edge
    options = EdgeOptions()
    # Para rodar no modo headless (sem interface gráfica), ative a linha abaixo
    # options.add_argument('--headless') 
    options.add_argument('--no-sandbox')     
    options.add_argument('--disable-dev-shm-usage')
    
    # 3. Inicializa o navegador Edge
    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)
    
    print("Aguardando o carregamento dinâmico da tabela (10 segundos)...")
    sleep(10) 
    
    html_content = driver.page_source
    driver.quit() 

    tabelas = pd.read_html(StringIO(html_content), flavor='html5lib')
    
    print(f"Total de tabelas encontradas no HTML completo: {len(tabelas)}")

    #  Processamento da Tabela
    if tabelas:
        df_proventos = tabelas[0]
        
        # Tentativa de definir o cabeçalho
        if len(df_proventos.columns) >= 6:
            df_proventos.columns = ['ATIVO', 'VALOR', 'DATA COM', 'DATA PAGAMENTO', 'TIPO', 'DY']
        
        # Limpeza simples: remove a primeira linha se for um cabeçalho repetido
        if 'ATIVO' in df_proventos.columns and df_proventos.iloc[0]['ATIVO'] == 'ATIVO':
            df_proventos = df_proventos.iloc[1:]

        # remover 'R$' e manter como string
        if 'VALOR' in df_proventos.columns:
            print("Limpando a coluna 'VALOR' (Removendo R$ e mantendo formato de string)...")
            
            # Remove R$ e qualquer espaço extra
            df_proventos['VALOR'] = (
                df_proventos['VALOR']
                .astype(str)
                .str.replace('R\$', '', regex=False) 
                .str.strip() 
            )

        # Remove colunas indesejadas (DY é a que estava sendo removida no script original)
        df_final = df_proventos.drop(columns=['DY']) if 'DY' in df_proventos.columns else df_proventos
            
        # 9. Salva o df no arquivo Excel 
        nome_arquivo = 'proventos_statusinvest_edge.xlsx'
        df_final.to_excel(nome_arquivo, index=False, engine='openpyxl')

        print(f"\n✅ Dados extraídos e salvos com sucesso no novo arquivo Excel: **{nome_arquivo}**")
        
    else:
        print("❌ Nenhuma tabela encontrada na página após o carregamento dinâmico.")

except Exception as e:
    # Garante que o driver feche mesmo em caso de erro
    if driver:
        driver.quit() 
    print(f"❌ Ocorreu um erro: {e}")
    print("\nAVISO: O MsedgeDriver requer que o Microsoft Edge esteja instalado. Verifique também a dependência 'msedge-selenium-tools'.")
    sys.exit(1)t