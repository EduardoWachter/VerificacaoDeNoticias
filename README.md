Verificação de Notícias – Descrição dos Arquivos
📂 WebScraping002_noticias/

Pasta contendo o código de web scraping utilizado para coletar notícias do site da Agência Lupa.
Inclui o script em Python com Selenium responsável por acessar as páginas, extrair título, descrição, conteúdo, data, autor e classificação da notícia, gerando o dataset bruto.

📄 ZeroShot_vFINAL2.ipynb

Notebook responsável pela etapa de filtragem e classificação das notícias.
Neste arquivo são realizados:

carregamento do dataset coletado,

limpeza e remoção de notícias fora do escopo,

preparação dos textos,

aplicação de modelos de linguagem (zero-shot) para classificar os rótulos.

📄 noticias_lupa.json

Arquivo gerado pelo web scraping contendo todas as notícias extraídas da Agência Lupa, no formato JSON estruturado.
