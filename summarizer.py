from transformers import pipeline
class Summarizer:
    """Class generating summarizations
    """
    def __init__(self, text, max_chars=1500):
        
        self.text = text 
        self.max_chars = max_chars
        self._chunk(max_chars)
        
    def _chunk(self, max_chars):
        
        chunks = []
        current = ''
        splitted = self.text.split('.')
        
        for sentence in splitted:
            
            if len(current) + len(sentence) <= max_chars:
                
                current += sentence + ". "
                
            else:
                
                chunks.append(current.strip())
                current = sentence + ". "
                
        
        self.chunks = chunks
        
    def summarize(self, max_length=500, min_length=200, model="summarize/text_summarization"):        
        
        summaries = []
        
        for chunk in self.chunks:
            
            l = len(chunk.split(' '))
            min_l = int(.4 * l)
            max_l = int(.8 * l)
            summaries.append(self.summ_pipe(chunk, max_length=max_l, min_length=min_l, model=model)[0]['summary_text'])
            
        self._sub_summ = summaries
        all_texts = ' '.join(summaries)
        self.summary = self.summ_pipe(all_texts, max_length=max_length, min_length=min_length, model=model)
        
        return self.summary[0]['summary_text']
    
    def summ_pipe(self, chunk, model, max_length=1000, min_length=300):
        
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