#pip install requests beautifulsoup4
#Os testes devem ser feitos em ordem pois um depende do outro.

import requests
from bs4 import BeautifulSoup
import zipfile
import concurrent.futures
import logging
import os
from typing import List, Tuple

BASE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
TARGET_EXTENSION = '.pdf'
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
ZIP_DIR = 'teste1'
ZIP_FILENAME = os.path.join(ZIP_DIR, 'anexos.zip')
TIMEOUT = 10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_page(session: requests.Session, url: str) -> str:
    """Obtém o conteúdo HTML de uma página."""
    logging.info(f"Acessando página: {url}")
    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Falha ao acessar {url}: {e}")
        raise

def extract_pdf_links(html: str) -> List[str]:
    """Extrai links de PDFs dos Anexos I e II."""
    logging.info("Processando HTML para encontrar links de PDF")
    soup = BeautifulSoup(html, 'html.parser')
    return [
        link.get('href') for link in soup.find_all('a')
        if link.get('href') and
        link.get('href').endswith(TARGET_EXTENSION) and
        ('Anexo_I' in link.get('href') or 'Anexo_II' in link.get('href'))
    ]

def download_pdf(session: requests.Session, url: str) -> Tuple[str, bytes]:
    """Baixa um arquivo PDF e retorna seu nome e conteúdo."""
    filename = url.split('/')[-1]
    logging.info(f"Iniciando download: {filename}")
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return filename, response.content
    except requests.RequestException as e:
        logging.error(f"Erro ao baixar {filename}: {e}")
        return filename, None

def main():
    """Execução principal do script."""
    os.makedirs(ZIP_DIR, exist_ok=True)
    
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    try:
        html = fetch_page(session, BASE_URL)
    except requests.RequestException:
        return

    pdf_links = extract_pdf_links(html)
    if not pdf_links:
        logging.warning("Nenhum PDF encontrado!")
        return

    logging.info(f"Encontrados {len(pdf_links)} arquivos para download")

    with zipfile.ZipFile(ZIP_FILENAME, 'w') as zipf:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_pdf, session, link) for link in pdf_links]
            for future in concurrent.futures.as_completed(futures):
                filename, content = future.result()
                if content:
                    zipf.writestr(filename, content)
                    logging.info(f"{filename} adicionado ao ZIP")

    logging.info(f"Processo concluído. Arquivos salvos em {ZIP_FILENAME}")

if __name__ == "__main__":
    main()
