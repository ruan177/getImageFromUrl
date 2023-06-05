import requests
from bs4 import BeautifulSoup
import re
import os

def run():
    # URL da página que você deseja extrair as URLs das imagens
    url = "https://url de sua preferencia"

    # Enviar uma solicitação HTTP para obter o conteúdo da página
    response = requests.get(url)

    # Criar um objeto BeautifulSoup para analisar o conteúdo HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar todas as tags <img> que contêm as imagens
    # pode ser alterado par outras tags html
    images = soup.find_all("img")

    # Extrair as URLs das imagens que terminam com ".png"
    image_urls = [img["src"] for img in images if "src" in img.attrs]
    image_hiperlinks = []


    #for para armazenar as urls que iniciem com http
    for i in range(len(image_urls)):
        element = image_urls[i]
        if element.startswith("http"):
           image_hiperlinks.append(element)

    # Expressão regular para selecionar apenas as urls que contenham png
    pattern = r".*.*\.png"

    #armazenando as urls na variavel matching strings
    matching_strings = [string for string in image_hiperlinks if re.search(pattern, string, re.IGNORECASE)]


    #removendo a parte inutil da url
    for i in range(len(matching_strings)):
        element = matching_strings[i]
        element_without_extension = element.split("/revision/")[0]
        matching_strings[i] = element_without_extension

    #imprimindo as urls para ver se o codigo esta ok
    for matching_string in matching_strings:
        print(matching_string)

    directory = r"C:\Users\nome do diretorio da sua escolha"  # Diretório onde as imagens serão salvas

    if not os.path.exists(directory):
        os.makedirs(directory)

    for url in matching_strings:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = url.split("/")[-1]
            file_path = os.path.join(directory, file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Imagem '{file_name}' salva com sucesso.")
        else:
            print(f"Falha ao baixar a imagem de URL: {url}")


if __name__ == '__main__':
    run()
