import requests, sys, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlunparse, urljoin

def buscar_parametros_links(url):
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        # Cria o objeto BeautifulSoup para analisar o conteúdo HTML da página
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Extrai os parâmetros da URL atual
        parsed_url = urlparse(url)
        parametros = parse_qs(parsed_url.query)
        
        # Extrai as URLs encontradas na página
        urls = []

        #parametros = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                url_absoluta = urljoin(url, href)
                urls.append(url_absoluta)
        return urls, parametros
            # Retorna os parâmetros encontrados como uma lista
            
    else:
        print('Falha ao fazer a requisição HTTP.')
        return {}, ()

def checkssti(links_parametros):
    payloads = ["${7*7}","<%=7*7%>","#{7*7}","*{7*7}","3*3"]
    urls_personalizadas = ()
    links = links_parametros
    #print(type(links))

    for link in links:
        for link2 in link:
            for payload in payloads:
                nova_url = urljoin(link2, payload)    
                #Adiciona a nova URL à lista de URLs personalizadas
                #urls_personalizadas.append(nova_url)
                urls_personalizadas = tuple(list(urls_personalizadas) + [nova_url])
                
    
    return urls_personalizadas


url_ativa = sys.argv[1]

# Chama a função para extrair os parâmetros da página
parametros_links_encontrados = buscar_parametros_links(url_ativa)
#print(parametros_links_encontrados)

nova = checkssti(parametros_links_encontrados)
for urls in nova:
    print(urls)
