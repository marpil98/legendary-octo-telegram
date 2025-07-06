from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    """Translator based on facebook/nllb-200-distilled-600M model.
    """
    def __init__(self, 
                src_lang="eng_Latn", 
                tgt_lang="pol_Latn", 
                model="translation/nllb-200-distilled-600M"
                ):
        """

        Parameters
        ----------
        src_lang : str, optional
            Primary language of text, by default "eng_Latn"
        tgt_lang : str, optional
            Target language, by default "pol_Latn"
        model : str, optional
            Path to model, by default "facebook/nllb-200-distilled-600M"
        """
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self._model_link = model
        
    def _model_init(self):
        
        self.tokenizer = AutoTokenizer.from_pretrained(self._model_link)
        self.translator = AutoModelForSeq2SeqLM.from_pretrained(self._model_link)
        self.tokenizer.src_lang = self.src_lang
        
    def translate(self, text):
        
        """Method which genrate translattion
        
        Prarmeters:
        -----------
        text : str
            Oryginall text whitch will be translated
        """
        self._model_init()
        inputs = self.tokenizer(text, return_tensors="pt")
        forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(
            self.tgt_lang
        )
        generated_tokens = self.translator.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id
        )
        self.translated = self.tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True)[0]
                
