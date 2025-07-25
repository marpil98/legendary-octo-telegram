from transformers import pipeline, logging
logging.set_verbosity_warning()
class Summarizer:
    """Class generating summarizations
    """
    def __init__(self, text, max_words=450):
        
        self.text = text 
        self.max_tokens = max_words
        self._chunk(max_words)
        
    def _chunk(self, max_words):
        
        chunks = []
        current = ''
        splitted = self.text.split('.')
        
        for sentence in splitted:
            
            added = 0
            if len((current + ' ' + sentence).split(' ')) <= max_words:
                
                current += sentence + ". "
                
            else:
                
                chunks.append(current.strip())
                current = sentence + ". "
                added = 1
        
        if not added:
            
            chunks.append(current)
            
        self.chunks = chunks
        
    def summarize(self, max_length=70, min_length=20, model="summarize/text_summarization"):        
        
        summaries = []
        
        for chunk in self.chunks:
            l = len(chunk.split(' '))
            
            min_l = max(int(.4 * l), min_length)
            max_l = max(int(.8 * l), max_length)
            summaries.append(self._sum_if_len(chunk, min_l, max_l, model))
        
        if len(summaries) > 1:    
            
            self._sub_summ = summaries
            all_texts = ' '.join(summaries)

            self.summary = self._sum_if_len(
                all_texts, 
                min(int(.8 * len(all_texts)), max_length), 
                max(min_length, int(.4 * l)), 
                model)
        
        else:
            
            self.summary = summaries[0]
            
        return self.summary
    
    def _sum_if_len(self, text, min ,max, model):
        
        if len(text.split(' ')) > 30:
        
            return self.summ_pipe(
                text, 
                max_length=max, 
                min_length=min, 
                model=model)[0]['summary_text']
        
        else:
            
            return text
        
    def summ_pipe(self, chunk, model, max_length=512, min_length=300):
        
        # tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        # model = AutoModelForSeq2SeqLM.from_pretrained(model)
        
        # inputs = tokenizer(
        #         chunk,
        #         return_tensors="pt",
        #         max_length=1024,
        #         truncation=True
        #     )
        # print(inputs["input_ids"])
        # summary_ids = model.generate(
        #     inputs["input_ids"],
        #     max_length=max_length,
        #     min_length=min_length,
        #     do_sample=False
        # )
        summarizer = pipeline("summarization", model=model,)
        
        return summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=True)