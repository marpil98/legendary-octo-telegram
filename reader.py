import requests
from requests.exceptions import MissingSchema

from bs4 import BeautifulSoup as bs
import pymupdf
import pymupdf4llm

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, logging
logging.set_verbosity_error()
logging.set_verbosity_warning()

class ArticleReader:
    """Class to reading articles from arxive or from drive
    """
    def __init__(self, link):
        """

        Parameters
        ----------
        link : str or path-like
            Link to the article. It can be url to article hosted on arxive
            or path to file in local drive
        """
        self.link=link
        self._page = None
        
        try:
            
            try:
                
                self._request()
                
            except MissingSchema:
                
                print("Ładowanie pliku z dokumentu")
                self.document = pymupdf.open(self.link)
        
        except Exception as e:
            
            print(e)            
            print("Nie można odczytać dokumentu. Upewnij się, że przekazany link jest poprawny!")
            
    def _request(self):
        
        self._page = requests.get(self.link)
    
    def read_pdf(self):
        """Method reads pdf an transform it into markdown 
        """
        if self._page is not None:
            
            data = self._page.content 
            self.document = pymupdf.Document(stream=data)
    
        else:
            
            pass
        
        try:
            
            self.text = pymupdf4llm.to_markdown(self.document)
            with open('temp/art.txt', 'w', encoding='utf-8') as file:
                
                file.write(self.text)
                
            print("Załadowano plik do markdown")
            self._markdown = 1
            
        except:
                
            self._connect_text()
            print("Załadowano zwykły tekst")
            self._markdown = 0
        
        return self.text
    
    def _connect_text(self):
        
        text = ''
        
        for page in self.document:
            
            print(page.get_text())
            text += page.get_text()
            
        self.text = text
        

