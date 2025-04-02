import unittest
from unittest.mock import patch, MagicMock
import requests
from io import BytesIO
import zipfile
from bs4 import BeautifulSoup
from script import download_pdf, extract_pdf_links, fetch_page

class TestPDFDownload(unittest.TestCase):
    
    @patch('script.requests.Session.get')
    def test_download_pdf_success(self, mock_get):
        """Testa o download bem-sucedido de um PDF."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Fake PDF content"
        mock_get.return_value = mock_response
        
        file_name, content = download_pdf(requests.Session(), "https://example.com/test.pdf")
        self.assertEqual(file_name, "test.pdf")
        self.assertEqual(content, b"Fake PDF content")
    
    @patch('script.requests.Session.get')
    def test_download_pdf_failure(self, mock_get):
        """Testa falha no download de um PDF."""
        mock_get.side_effect = requests.RequestException("Erro de conexão")
        
        file_name, content = download_pdf(requests.Session(), "https://example.com/test.pdf")
        self.assertEqual(file_name, "test.pdf")  # Nome ainda é retornado
        self.assertIsNone(content)

class TestPDFExtraction(unittest.TestCase):
    
    def test_extract_pdf_links(self):
        """Testa extração de links de PDFs da página HTML."""
        html_content = '''
        <html>
            <body>
                <a href="https://example.com/Anexo_I.pdf">Anexo I</a>
                <a href="https://example.com/Anexo_II.pdf">Anexo II</a>
                <a href="https://example.com/documento.docx">Outro</a>
            </body>
        </html>
        '''
        extracted_links = extract_pdf_links(html_content)
        self.assertEqual(len(extracted_links), 2)
        self.assertIn("https://example.com/Anexo_I.pdf", extracted_links)
        self.assertIn("https://example.com/Anexo_II.pdf", extracted_links)
    
    def test_extract_pdf_links_empty(self):
        """Testa comportamento quando nenhum PDF é encontrado na página."""
        html_content = """<html><body><p>Nenhum PDF aqui!</p></body></html>"""
        extracted_links = extract_pdf_links(html_content)
        self.assertEqual(len(extracted_links), 0)
    
class TestZipCreation(unittest.TestCase):
    
    def test_zip_creation(self):
        """Testa se os arquivos são corretamente adicionados a um ZIP."""
        pdf_files = {"file1.pdf": b"content1", "file2.pdf": b"content2"}
        
        with BytesIO() as zip_buffer:
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for file_name, content in pdf_files.items():
                    zip_file.writestr(file_name, content)
            
            zip_buffer.seek(0)
            with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                self.assertEqual(set(zip_file.namelist()), set(pdf_files.keys()))
                for file_name in pdf_files.keys():
                    with zip_file.open(file_name) as f:
                        self.assertEqual(f.read(), pdf_files[file_name])

if __name__ == "__main__":
    unittest.main()
