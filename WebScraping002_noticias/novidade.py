import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import shutil

#cria pasta de download de imagens
PASTA_IMAGENS = "imagens"
#os.makedirs(PASTA_IMAGENS, exist_ok=True)

#if os.path.exists(PASTA_IMAGENS):
    #shutil.rmtree(PASTA_IMAGENS)  # apaga a pasta inteira
os.makedirs(PASTA_IMAGENS)

# --- Configuração Selenium ---
options = Options()
service = Service()

# Headless + tamanho de tela + user-agent
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://lupa.uol.com.br/jornalismo/categoria/verificação")

# --- Repetir scroll incremental + leve subida ---
for i in range(80):  # pode aumentar se quiser mais
    print(f"🔄 Passagem {i+1} de 80")

    # Scroll em blocos (em vez de ir direto pro fim)
   # driver.execute_script("window.scrollBy(0, 800);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(0.3)

    # Scroll levemente para cima
    driver.execute_script("window.scrollBy(0, -250);")
    time.sleep(0.5)

    # Tenta clicar no botão "Carregar mais"
    try:
        botao = WebDriverWait(driver, 0.4).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
        )
        if "Carregar mais" in botao.text:
            botao.click()
            print("✅ Botão 'Carregar mais' clicado")
            time.sleep(0.2)
    except: 
        pass

# --- Captura todas as notícias ao final ---
dados = []
time.sleep(0.2)  # espera 2s antes de capturar
noticias = driver.find_elements(By.CSS_SELECTOR, "div.sc-dkrFOg.cbDCWR")
print(f"📊 Total de notícias encontradas: {len(noticias)}")

for noticia in noticias:
    try:
        titulo = noticia.find_elements(By.CSS_SELECTOR, 'span')[1].text
    except:
        titulo = ""
    try:
        descricao = noticia.find_element(By.CSS_SELECTOR, "p").text
    except:
        descricao = ""
    try:
        dataHora = noticia.find_elements(By.CSS_SELECTOR, 'span')[0].text
    except:
        dataHora = ""
    try:
        autor = noticia.find_elements(By.CSS_SELECTOR, 'span')[3].text
    except:
        autor = ""
    try:
        link = noticia.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except:
        link = ""

    # entra na pagina da noticia para pegar outras informacoes
    if link:
        # abre nova aba
        driver.switch_to.new_window("tab")
        driver.get(link)
        time.sleep(0.5)

        # pega o texto do corpo da noticia ignorando os 10 primeiros (cabecalho, autor, data,etc)
        texto = ""
        try:
            spans = driver.find_elements(By.CSS_SELECTOR, "span")[10:51]
            texto = " ".join([s.text for s in spans if s.text.strip()])
        except:
            texto = ""

        # Tenta pegar as tags da noticia (politica, educacao,etc)
        tag = ""
        try:
            tags_label = driver.find_element(
                By.XPATH, "//span[contains(text(), 'Tags')]")

            # 2. Achar o próximo span que contém as tags
            tags_container = tags_label.find_element(
                By.XPATH, "./ancestor::div/following-sibling::div//span")

            # 3. Extrair todos os <a> dentro dele
            tags = tags_container.find_elements(By.TAG_NAME, "a")
            tags = [t.text.strip().replace(",", "")
                    for t in tags_container.find_elements(By.TAG_NAME, "a")]
            tag = ", ".join(tags)
        except:
            tag = ""

        # tenta pegar links dentro da noticia
        try:
            u_tags = driver.find_elements(By.CSS_SELECTOR, "u")
            list_links = []
            for u_tag in u_tags:
             # Encontrar a tag <a> pai da tag <u>
                # ".." para pegar o elemento pai (a tag <a>)
                a_tag = u_tag.find_element(By.XPATH, "..")

             # Verificar se existe o atributo href na tag <a>
                if a_tag and a_tag.get_attribute('href'):
                    linkH = a_tag.get_attribute('href')
                    list_links.append(linkH)

        except:
            pass

        #Tenta pegar imagens de dentro da noticia
        try:

            images = driver.find_elements(By.CSS_SELECTOR, "img")
            imagens_locais=[]
            for idx, img in enumerate(images):
                src = img.get_attribute("src")
                if src and "a.storyblok.com" in src:
                    try:
                        # Nome do arquivo da imagem
                        nome_arquivo = f"noticia_{int(time.time())}_{idx}.jpg"
                        caminho_local = os.path.join(PASTA_IMAGENS, nome_arquivo)

                        # Baixa e salva a imagem
                        r = requests.get(src, timeout=10)
                        r.raise_for_status()
                        with open(caminho_local, "wb") as img_file:
                            img_file.write(r.content)

                        imagens_locais.append(caminho_local)

                    except Exception as e:
                        print(f"⚠ Erro ao baixar imagem {src}: {e}")

        except:
            pass

        classificacao=[]
        class_text=""
        try:
            classificacao = driver.find_elements(By.XPATH, '//span[@size="32"]')
            class_text = classificacao[len(classificacao)-1].text
            # talves fazer o comprimento de classificação - 1 pra pegar o ultimo item da lista invés do nro fixo 1

        except:
            pass
        # fecha aba atual
        driver.close()

        # volta pra aba principal (primeira da lista)
        driver.switch_to.window(driver.window_handles[0])

    dados.append({
        "titulo": titulo,
        "descricao": descricao,
        "autor": autor,
        "data": dataHora,
        "texto": texto,
        "tag": tag,
        "link": link,
        #"imagens": ", ".join(filtered_images),
        "imagens": imagens_locais,
        "links_noticia": ", ".join(list_links),
        "classificacao": class_text
    })

# --- Salvar em JSON ---
with open("noticias_lupa.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(
    f"🎉 Capturadas {len(dados)} notícias. Arquivo salvo como noticias_lupa.json")

driver.quit()