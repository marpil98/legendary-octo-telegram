import re
from collections import OrderedDict
from pprint import pprint

def rename_key_ordereddict(odict, old_key, new_key):
    """Zamienia klucz w OrderedDict, zachowując kolejność."""
    items = list(odict.items())
    for idx, (k, v) in enumerate(items):
        if k == old_key:
            items[idx] = (new_key, v)
            break
    return OrderedDict(items)

class TextAnalyzer:
    
    def __init__(self, file, max_length=512):
        
        self.file = file
        self.max_length = max_length
    
    def _remove_index_ref(self, text):
        
        pattern = r'\[\s*(\d+\s*,\s*)*\d+\s*\]'
        text = re.sub(pattern=pattern, repl='', string=text)
        
        return text
    
    def _split_fraze(self, fraze):
        
        d = (len(fraze) // 1024)
        subfrazes = []
        
        if d > 0:
            
            l = len(fraze) // d            
            
            for i in range(l):
            
                subfrazes.append(fraze[i * l : (i + 1) * l])
                
            subfrazes.append(fraze[(i + 1) * d:])
        
        else:
            
            subfrazes.append(fraze)
            
        return subfrazes
    
    def _split_by_length(self, text):
            
        text = text.replace('\n', ' ').replace('\t', ' ')
        splitted = text.split('. ')
        parts = []
        
        for i in splitted:
            
            parts += self._split_fraze(i)
        
        
        return parts
    def _clean_sections_keys(self, sections):
        
        new = OrderedDict()
        chars = r'[^a-zA-Z]'
        
        for i in sections.keys():
            
            new[re.sub(chars, '', i)] = sections[i]
            
        return new
            
    def split_by_heads(self):
        
        pattern = r'^\*\*(.+?)\*\*\s'
        matches = list(re.finditer(pattern, self.file, re.MULTILINE))
        
        title_pattern = r'^\#\#(.+?)\*\*\s*$'
        self.title = list(re.finditer(title_pattern, self.file, re.MULTILINE))[0].group(1).strip()
        sections = OrderedDict()
        
        for i, match in enumerate(matches):
            
            start = match.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(self.file)
            title = match.group(1).strip('# ').strip()

            body = self.file[start:end].strip()
            body.replace('\n', ' ').replace('\t', ' ')
            sections[title] = body
        
        sections = self._clean_sections_keys(sections)
        
        pprint(sections.keys())
        self._part_dict = {}
        
        self._fid_part(sections, "abstract")
        pprint(self._part_dict)
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
            
            sections[i] = self._split_by_length(self._remove_index_ref(sections[i]))
            
        self.sections = sections
        self._clear_sections()
        
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

    def _clear_sections(self):
        
        header = ''
            
        for i in self.sections.copy():
            
            if header == '':
                
                if self.sections[i] == '':
                    
                    header = i
                    self.sections.pop(i)
            else:
                
                new_header = header + '\n' + i
                self.sections = rename_key_ordereddict(self.sections, i, new_header)
                header = ''
        