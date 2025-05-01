import requests
from bs4 import BeautifulSoup
import random
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

def raspar_cuponomia():
    url = "https://www.cuponomia.com.br/descontos"
    
    try:
        # Simula comportamento humano
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()  # Verifica erros HTTP

        soup = BeautifulSoup(response.text, 'html.parser')
        cupons = []
        
        for item in soup.select('.offer-box:has(.offer-store)'):  # Filtra itens válidos
            try:
                loja = item.select_one('.offer-store').text.strip().lower()
                titulo = item.select_one('.offer-title').text.strip() if item.select_one('.offer-title') else loja
                desconto = item.select_one('.offer-discount').text.strip() if item.select_one('.offer-discount') else "N/A"
                link = "https://www.cuponomia.com.br" + item.select_one('a')['href']
                
                # Aplica link de afiliado (exemplo para Amazon)
                if 'amazon' in loja:
                    link_afiliado = f"{link}?ref=dicasdoph-20"
                else:
                    link_afiliado = link
                
                cupons.append({
                    "loja": loja,
                    "titulo": titulo,
                    "desconto": desconto,
                    "link": link_afiliado
                })
            except Exception as e:
                print(f"Erro ao processar item: {e}")
                continue

        return cupons if cupons else None

    except Exception as e:
        print(f"Erro ao acessar Cuponomia: {e}")
        return None