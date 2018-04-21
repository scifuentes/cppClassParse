import re

#re_scope=re.compile('(}|(namespace|class|struct)\s+(.+?){|{)')
re_scope=re.compile('(}|(namespace|class|struct)\s+(.+?){|{)')
class ScopeNode:
    def __init__(self,key,name,parent):
        self.key=key
        self.name=name
        self.parent=parent
        if parent:
            parent.childs.append(self)
        self.childs=[]
def textToScopes(text):
    text=text.replace('\n',' ')
    currentScope=None
    scopes=[]
    for match in re_scope.findall(text):
        if match[0]!='}':
            newScope=ScopeNode(match[1],match[2].strip(),currentScope)
            scopes.append(newScope)
            currentScope=newScope
        else:
            currentScope = currentScope.parent
    return scopes
            

            

    
    


    