

from array import array


class Json:



    def __init__(self, filename:str = None, dict_obj:dict = None, array:list = None, simple:(int|str|float) = None) -> None:
        
        self.file = filename
        self.dict_obj = dict_obj
        self.array = array
        self.simple = simple
        

    def print_json(self):
       
        
        print(self.simple)
        print(self.array)
        print(self.dict_obj)



    def parse_dict(self,file):
        diz = {}
        chunk = '{'
        key  = ""   
             
        while True: 
            chunk = file.read(1)
            if chunk == '{':
                diz[key] = self.parse_dict(file)
            elif chunk == '"' and len(key) == 0:
                value = self.parse_simple(file,chunk)
                key = value[0]
            elif chunk == ',':
                key = ""
            elif chunk.isspace():
                pass
            elif chunk == '}':
                return diz
            elif chunk == ':':
                pass
            elif chunk == "[":
                diz[key] = self.parse_array(file)
            else:
                value = self.parse_simple(file, chunk)                
                if value[1] == '}':
                    diz[key] = (value[0])
                    return diz
                
                diz[key] = (value[0])
                

    def parse_array(self,file):
        arr = []
        chunk = '['
        while True: 
            chunk = file.read(1)
            if chunk == '[':
                arr.append(self.parse_array(file))
            elif chunk == ',' or chunk.isspace():
                pass
            elif chunk == ']':
                return arr
            elif chunk == '{':
                arr.append(self.parse_dict(file))
            else:
                value = self.parse_simple(file, chunk)
                if value[1] == ']':
                    arr.append(value[0])
                    return arr
                arr.append(value[0])
    
    def parse_simple(self,file,ch:str):
        token = ch
        chunk = ch
        while True :  
            if(chunk.isspace()):
                pass
            elif(chunk.isdigit()):
                dot = False
                chunk = file.read(1)
                while chunk.isdigit():
                    token +=chunk 
                    chunk = file.read(1)
                    if chunk == '.':
                        dot = True
                        token +=chunk 
                        chunk = file.read(1)
                        continue
                if dot == True:
                    return float(token),chunk
                else :
                    return int(token),chunk
            elif chunk == 't' or chunk == 'f': 

                while chunk != 'e' :
                    token +=chunk 
                    chunk = file.read(1)
                
                if token[1:] + 'e' == "true":
                    return True,chunk
                else:
                    return False,chunk

            elif chunk == '"':
                chunk = file.read(1)
                
                while chunk != '"' :
                    token += chunk 
                    chunk = file.read(1)
                return token[1:],chunk

            chunk = file.read(1)



    def parse(self):
        
        with open(self.file) as file:
            chunk = file.read(1) 
            if(chunk.isspace()):
                pass
            elif chunk == '{':
                self.dict_obj = self.parse_dict(file)
            elif chunk == '[':
                self.array = self.parse_array(file)
            else:
                value = self.parse_simple(file,chunk)
                self.simple = value[0]





js = Json("prova.json")

s = js.parse()

js.print_json()