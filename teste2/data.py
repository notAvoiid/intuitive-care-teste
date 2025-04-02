#pip install tabula-py

import zipfile
import tabula
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ZIP_DIR = 'teste2'
os.makedirs(ZIP_DIR, exist_ok=True)

try:
    with zipfile.ZipFile("teste1/anexos.zip", 'r') as zip_ref:
        logging.info("Iniciando extração do arquivo PDF...")
        zip_ref.extract("Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf", '.')
        logging.info("Arquivo PDF extraído com sucesso")

    logging.info("Iniciando conversão do PDF para CSV...")
    tabula.convert_into(
        "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
        "converted.csv",
        output_format="csv",
        lattice=True,
        stream=False,
        pages="all"
    )
    logging.info("Conversão para CSV concluída")

    logging.info("Iniciando processamento do arquivo CSV...")
    with open("converted.csv", 'r', encoding='utf-8') as file:
        conteudo = file.read()

    logging.info("Realizando substituições de texto...")
    conteudo = conteudo.replace('OD', 'Seg. Odontológica ')
    conteudo = conteudo.replace('AMB', 'Seg. Ambulatorial ')

    with open("converted.csv", 'w', encoding='utf-8') as file:
        file.write(conteudo)
    logging.info("Substituições concluídas com sucesso")

    logging.info("Criando arquivo ZIP final...")
    final_zip_path = os.path.join(ZIP_DIR, "Teste_Igor.zip")
    with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("converted.csv")
    logging.info("Arquivo ZIP criado com sucesso em teste2/")

    logging.info("Limpando arquivos temporários...")
    os.remove("Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
    os.remove("converted.csv")
    logging.info("Limpeza concluída")

    print("\nProcesso finalizado com sucesso!")
    print(f"Arquivo resultante disponível em: {final_zip_path}")

except FileNotFoundError as e:
    logging.error(f"Arquivo não encontrado: {str(e)}")
    raise
except Exception as e:
    logging.error(f"Ocorreu um erro durante o processamento: {str(e)}")
    raise
