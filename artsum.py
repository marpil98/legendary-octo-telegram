from translator import Translator
from summarizer import Summarizer
from analyzer import TextAnalyzer
from reader import ArticleReader
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
            
    def summarize(self):
        
        self._sum_parts()
        summaries = '. '.join(list(self.summs.values()))
        summarizer = Summarizer(summaries)
        self.summary = summarizer.summarize()
        
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
    
    