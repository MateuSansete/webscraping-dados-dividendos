## Web Scraping de Proventos de Ações

Um mini projeto de Web Scraping para extrair dados de proventos de ações e fundos imobiliários do site **Status Invest** e salvar o resultado em um arquivo Excel limpo.

O projeto utiliza **Selenium** para lidar com o carregamento dinâmico da página web e **Pandas** para processar e estruturar os dados.

---

## Funcionalidades

* **Extração Dinâmica:** Utiliza **Selenium** com `webdriver-manager` para automatizar a abertura do navegador (Chrome) e capturar o conteúdo dinâmico da página.
* **Processamento de Dados:** Emprega **Pandas** para ler a tabela HTML, limpar a coluna de valores (removendo 'R$') e renomear as colunas.
* **Exportação:** Salva o conjunto de dados final em um arquivo **`.xlsx` (Excel)** para fácil análise e manipulação.

---

##  Tecnologias Utilizadas

* **Python 3.x**
* **Selenium:** Para automação e extração de conteúdo dinâmico.
* **Pandas:** Para manipulação e exportação de dados.
* **WebDriver Manager:** Para gerenciar o driver do Chrome automaticamente.
* **URL de Origem:** `https://statusinvest.com.br/acoes/proventos`

---

##  Como Executar o Projeto

### 1. Pré-requisitos

Certifique-se de ter o Python instalado.

### 2. Instalação das Dependências

Instale as bibliotecas necessárias usando `pip`:

```bash
pip install pandas selenium webdriver-manager openpyxl html5lib
