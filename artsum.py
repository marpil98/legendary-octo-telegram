from tqdm import tqdm

from translator import Translator
from summarizer import Summarizer
from analyzer import TextAnalyzer
from reader import ArticleReader

import pymupdf as pm
model_path = "/home/marcinpielwski/LLMs/HFCert/translation/nllb-200-distilled-600M"
class ArticleSummarizer:
    
    def __init__(self, article_link):
        
        self.link = article_link
        self.article = ArticleReader(self.link).read_pdf()
        self.analyzer = TextAnalyzer(self.article)
        
        self._splitting()
        
    def _splitting(self):
        
        self.analyzer.split_by_heads()
        
    def _sum_parts(self):
        
        self.summs = {}
        
        for i in self.analyzer.sections:
            
            summarizer = Summarizer(self.analyzer.sections[i])
            self.summs[i] = summarizer.summarize()
            
    def summarize(self, max_length=250, min_length=150):
        
        self._sum_parts()
        summaries = '. '.join(list(self.summs.values()))
        summarizer = Summarizer(summaries)
        self.summary = summarizer.summarize(min_length=min_length, max_length=max_length)
        
    def _translate(self, text, src_lang="eng_Latn", tgt_lang="pol_Latn", model=model_path):
        
        self.translator = Translator(src_lang=src_lang, tgt_lang=tgt_lang, model=model)
        self.translator.translate(text=text)
        
        return self.translator.translated
        
    def translate_long(self):
        
        self.translation_all = self._translate(self.summary)
    
    def _translate_part(self, part_name):
        
        return self._translate(self.summs[part_name])
    
    def _translate_parts(self):
        
        self.translations = {}

        for i in self.summs:
        
            self.translations[self._translate(i)] = self._translate_part(i)
            
    def display(self):
        
        print("Artykuł: ", self.analyzer.title)
        print("Tłumaczenie podsumowania: \n", self.translation_all)
        
        for i in self.summs:

            print(f"Tłumaczenie sekcji {i}: \n", self._translate_part(i))
    
class ArticleTranslator:
    
    def __init__(self, article_link):
        
        self.link = article_link
        self.article = ArticleReader(self.link).read_pdf()
        self.analyzer = TextAnalyzer(self.article)
        
        self._splitting()
        
    def _splitting(self):
        
        self.analyzer.split_by_heads()
        
    def translate_all(self):
        
        set_trans = {}
        
        def tlumaczenie(text):
            
            t = Translator()
            t.translate(text=text)
            return t.translated
        
        set_trans["Tytuł"] = tlumaczenie([self.analyzer.title])
        set_trans["Abstrakt"] = tlumaczenie([self.analyzer.abstract])
        
        for i in tqdm(self.analyzer.sections):
            
            print(f"Tłumaczę sekcję {i}")
            t = tlumaczenie(self.analyzer.sections[i])
            if len(t) > 1:
                
                t = '. '.join(t)
                
            else:
                
                t = t[0]
                
            set_trans[i] = tlumaczenie(self.analyzer.sections[i])
        
        self.translations = set_trans
        

    def display(self):
        
        print("Artykuł: ", self.translations['Tytuł'])
    
        for i in self.translations:
            
            if i != 'Tytuł':
            
                print(f"Tłumaczenie sekcji {i}: \n", self.translations[i])
                
class PDFGenerator():
    
    def __init__(self):
        
        self.doc = pm.open() 
    
    def _insert_text(self, text):
        
        p = pm.Point(75, 80)
        page = self.doc[-1]
        rect = pm.Rect(50, 200, 500, 800)
        page.insert_htmlbox(
            rect,
            text,
            css="*{font-family: sans-serif; font-size:14px}"
        )
        # page.insert_text(p,  # bottom-left of 1st char
        #     text,  # the text (honors '\n')
        #     fontname = "helv",  # the default font
        #     fontsize = 11,  # the default font size
        #     rotate = 0,  # also available: 90, 180, 270
        #     )

    def _insert_header(self, header):
        
        page = self.doc.new_page()
        rect = pm.Rect(50, 60, 400, 200)
        header = header.replace("**", "")
        page.insert_htmlbox(
            rect,
            header,
            css="*{font_family: sans-serif; font-size:20px}"
        )
        # page.insert_text(p,
        #     header,
        #     fontname='hebo',
        #     fontsize=20,
        #     rotate=0
        # )
    
    def _generate_page(self, header, text):
        
        self._insert_header(header)
        self._insert_text(text)
        
    def generate_pdf(self, translator):
        
        sections = translator.translations
        
        for i in sections:
            
            self._generate_page(i, sections[i])
            
    def save(self, name="Untitled_pdf.pdf"):    
        
        self.doc.save(name)