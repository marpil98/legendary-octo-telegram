import re

class TextAnalyzer:
    
    def __init__(self, file):
        
        self.file = file
    
    def _remove_index_ref(self, text):
        
        pattern = r'\[\s*(\d+\s*,\s*)*\d+\s*\]'
        text = re.sub(pattern=pattern, repl='', string=text)
        
        return text
        
    def split_by_heads(self):
        
        pattern = r'^\*\*(.+?)\*\*\s*$'
        matches = list(re.finditer(pattern, self.file, re.MULTILINE))
        
        sections = {}
        
        for i, match in enumerate(matches):
            
            start = match.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(self.file)
            title = match.group(1).strip('# ').strip()

            body = self.file[start:end].strip()
            sections[title] = body
        
        self._part_dict = {}
        
        self._fid_part(sections, "abstract")
        self.abstract = sections[self._part_dict['abstract']]
        sections.pop(self._part_dict['abstract'])
        
        self._fid_part(sections, "keywords")
        self.keywords = sections[self._part_dict['keywords']]
        sections.pop(self._part_dict['keywords'])
        
        self._fid_part(sections, "references")
        self.ref = sections[self._part_dict['references']]
        sections.pop(self._part_dict['references'])
        
        del self._part_dict
        
        self._find_appendixes(sections=sections)
        
        self.appendixes = {i:sections[i] for i in self._app_headers}
        del self._app_headers
        
        for i in sections:
            
            sections[i] = self._remove_index_ref(sections[i])
            
        self.sections = sections
        
    def _fid_part(self, sections, name):
        
        for i in sections.keys():
            
            if name in i.lower():
                
                self._part_dict[name] = i
                break
        
        try:
            
            self._part_dict[name]
            
        except:
            
            print(f"Nie odnaleziono w tekście częśći: {name}")
        
    def _find_appendixes(self, sections):
        
        app_occ = 0
        app_heads = []
        
        for i in sections.keys():
            
            if "appendix" in i.lower():
                
                app_occ = 1
                
            if app_occ:
                
                app_heads.append(i)
                
        self._app_headers = app_heads
