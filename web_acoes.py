import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from io import StringIO
import sys

# URL da página de proventos
url = 'https://statusinvest.com.br/acoes/proventos'

print(f"Iniciando a extração com Selenium para: {url}...")

driver = None

try:
    #  Configuração e Inicialização do Selenium
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #  LINHA ABAIXO COMENTADA PARA RODAR NO MODO VISÍVEL
    # options.add_argument('--headless') 
    options.add_argument('--no-sandbox')     
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=service, options=options)
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

        # remover  'R$' e  manter como string
        if 'VALOR' in df_proventos.columns:
            print("Limpando a coluna 'VALOR' (Removendo R$ e mantendo formato de string)...")
            
            # Remove R$ e qualquer espaço extra
            df_proventos['VALOR'] = (
                df_proventos['VALOR']
                .astype(str)
                .str.replace(r'R\$', '', regex=False) 
                .str.strip() 
            )

        # Remove colunas indesejadas 
        df_final = df_proventos.drop(columns=['DY']) if 'DY' in df_proventos.columns else df_proventos
            
        # 9. Salva o df no arquivo Excel 
        nome_arquivo = 'proventos_statusinvest_texto_limpo.xlsx'
        df_final.to_excel(nome_arquivo, index=False, engine='openpyxl')

        print(f"\n✅ Dados extraídos e salvos com sucesso no novo arquivo Excel: **{nome_arquivo}**")
        
    else:
        print("❌ Nenhuma tabela encontrada na página após o carregamento dinâmico.")

except Exception as e:
    # Garante que o driver feche mesmo em caso de erro
    if driver:
        driver.quit() 
    print(f"❌ Ocorreu um erro: {e}")
    sys.exit(1)