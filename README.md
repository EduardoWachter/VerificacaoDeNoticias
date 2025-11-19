Verificação de Notícias – Descrição dos Arquivos
📂 WebScraping002_noticias/

Contém o script em Python (Selenium) responsável por coletar automaticamente as notícias do site da Agência Lupa, extraindo título, descrição, conteúdo, autor, data e classificação. Gera o dataset bruto para processamento.

📄 ZeroShot_vFINAL2.ipynb

Notebook que realiza a filtragem e a classificação das notícias.
Inclui:

limpeza e padronização do dataset,

remoção de notícias fora dos rótulos definidos,

testes com modelos zero-shot,

classificação com ou sem busca na web.

📄 noticias_lupa.json

Arquivo original do web scraping contendo as 2160 notícias coletadas da Lupa.

📄 palavrasChavePModelo.json

Lista com palavras-chave geradas para cada notícia, utilizadas para buscas externas na web durante a classificação.

📄 noticiasClassificadasPM.json

Lista de notícias que foram classificadas apenas a partir da descrição, sem uso de informações externas.

📄 noticiasClass_buscaLivre.json

Lista de notícias classificadas pelo modelo utilizando descrição + informações recuperadas da web.

📄 noticiasFIL_lupa.json

Conjunto filtrado contendo:

apenas notícias com classificações dentro do conjunto oficial de rótulos,

descrições limpas de palavras pertencentes ao rótulo ou sinônimos.

O conjunto inicial possuía 408 notícias, retornando 400 após o processamento.
