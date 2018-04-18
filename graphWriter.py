import os

#==============================================================================

class Node:
    def __init__(self,name):
        self.name=name
        self.label=name
        self.info=""
        self.edgeL=[]               # a collection of Edge items
        self.color=None
        self.colorOutline=None
        self.group=None
        
    @classmethod
    def Copy(cls,node):
        self=cls(node.name)
        self.label=node.label
        self.info=node.info
        self.color=node.color
        self.colorOutline=node.colorOutline
        self.group=node.group
        return self

class Edge:
    def __init__(self,target=None):
        self.target=target          # a Node item
        self.info=""
        self.label=''
        self.color=None
        self.style=None
    
    @classmethod
    def Copy(cls,edge):
        self=cls()
        self.info=edge.info
        self.label=edge.label
        self.color=edge.color
        self.style=edge.style
        return self
        
class NodeGroup:
    def __init__(self,name):
        self.name=name
        self.label=name
        self.group=None
        self.color=None
        self.edgeL=[]

#==============================================================================
def GetTopNodes(nodeL) :
    topNodeL=nodeL[:]
    for node in nodeL:
        for edge in node.edgeL :
            try:
                topNodeL.remove(edge.target)
            except ValueError :
                pass
    return topNodeL

def GetEndNodes(nodeL) :
    endNodeL=[]
    for node in nodeL:
        if len(node.edgeL)==0 :
            endNodeL.append(node)
    return endNodeL
        

#==============================================================================

def NodeL2File(nodeL,filename=None, format=None):
    if not filename : filename='output.gml'
    fileName=os.path.splitext(filename)[0]
    ext=os.path.splitext(filename)[1]
    if ext=='': ext ='.gml'
    
    format2ext={'gml':'.gml','graph':'.graphml','graphml':'.graphml','dot':'.dot','txt':'.txt'}
    if format :
        ext=format2ext[format]

    if ext=='.gml' :
        lines=NodeL2GML(nodeL)
    elif ext=='.graphml' :
        lines=NodeL2GraphML(nodeL)
    elif ext=='.dot' :
        lines=NodeL2DOT(nodeL)
    elif ext=='.txt' :
        lines=NodeL2txt(nodeL) 
    else :
        lines=NodeL2GML(nodeL)
        
    WriteLines(lines,fileName+ext)  
    
def WriteLines(lines,fileName) :

    if len(fileName)>255:
        ext=os.path.splitext(fileName)[1]
        name=os.path.splitext(fileName)[0]
        fileName=fileName[:254-len(ext)]+'~'+ext
        
    f=open(fileName,'w')
    f.write('\n'.join(lines))
    f.close()
    
def HighlightNode(nodeL, MatchFunc, color):
    for node in filter(MatchFunc, nodeL) :
        node.color=color
        
#==============================================================================

def GetGroups(nodeL):
    groupL=[node.group for node in nodeL if node.group]
    groupL=list(set(groupL))
    return groupL

#==============================================================================

def NodeL2GML(nodeL):
    def FormatString(string):
        out=string
        out=out.replace('&','&amp;')
        out=out.replace('"','&quot;')
        return out
        
    colorD={'light_gray':'#B0B0B0','gray':'#808080', "blue0": '#6666ff' , 'blue1':'#ccccff','orange':'#ff7700','dgreen':'#008000','red':'#ff0000'}
    
    lines=[]
    lines.append('graph [')
    group=True
    
    nodeL_i=dict(zip(nodeL,range(len(nodeL))))
    
    groupL=GetGroups(nodeL)
    groupL_i=dict(zip(groupL,range(len(nodeL),len(nodeL)+len(groupL))))
    
    for node in nodeL:
        lines.append('\t'*1+'node [')
        lines.append('\t'*2+'id '+str(nodeL_i[node]) )
        lines.append('\t'*2+'label "'+ FormatString(node.label) +'"')
        lines.append('\t'*2+'graphics [')
        lines.append('\t'*3+'w '+str(15+7*(len(FormatString(node.label))+2)))
        if node.color :
            if node.color in colorD.keys():
                lines.append('\t'*3+'fill "'+colorD[node.color]+'"')
            else:
                lines.append('\t'*3+'fill "'+node.color+'"')
        if node.colorOutline :
            if node.colorOutline in colorD.keys():
                lines.append('\t'*3+'outline "'+colorD[node.colorOutline]+'"')
            else:
                lines.append('\t'*3+'outline "'+node.colorOutline+'"')

        lines.append('\t'*2+']')
        if node.group:
            lines.append('\t'*2+'gid '+str(groupL_i[node.group]))    
        lines.append('\t'*1+']')        

    for group in groupL:
        lines.append('\t'*1+'node [')
        lines.append('\t'*2+'id '+str(groupL_i[group]) )
        lines.append('\t'*2+'label "'+ FormatString(group.label) +'"')
        if group.group:
            lines.append('\t'*1+'gid '+str(groupL_i[group.group]))        
        lines.append('\t'*1+'isGroup 1')        
        lines.append('\t'*1+']')        
        
    for node in nodeL:
        for edge in node.edgeL :
            lines.append('\t'*1+'edge [')
            lines.append('\t'*2+'source '+ str(nodeL_i[node]) )
            lines.append('\t'*2+'target '+ str(nodeL_i[edge.target]))
            if edge.label!='' :
                lines.append('\t'*2+'label "'+ FormatString(edge.label)+'"')
            
            lines.append('\t'*2+'graphics [')
            lines.append('\t'*3+'arrow "last"')                
            if edge.color:
                if edge.color in colorD.keys():
                    lines.append('\t'*3+'fill "'+colorD[edge.color]+'"')    
                else :
                    lines.append('\t'*3+'fill "'+edge.color+'"')    
            if edge.style :
                lines.append('\t'*3+'style "'+edge.style+'"')    
            lines.append('\t'*2+']')
            lines.append('\t'*1+']')
    
    lines.append(']')
    
    return lines
   

def NodeL2GraphML(nodeL):
    colorD={'light_gray':'#B0B0B0','gray':'#808080', "blue0": '#6666ff' , 'blue1':'#ccccff','orange':'#ff7700','dgreen':'#008000'}
    
    lines=[]
    lines.append('<graphml>')
    lines.append('<key id="color" for="node" attr.name="color" attr.type="string"/>')
    lines.append('<key id="label" for="node" attr.name="label" attr.type="string"/>')
    lines.append('<key id="info" for="node" attr.name="info" attr.type="string"/>')
    lines.append('<key id="ecolor" for="edge" attr.name="color" attr.type="string"/>')
    lines.append('<key id="einfo" for="edge" attr.name="info" attr.type="string"/>')
    lines.append('\t'*1+'<graph>')   
    
    nodeL_i=dict(zip(nodeL,range(len(nodeL))))
    for node in nodeL:
        lines.append('\t'*2+'<node id="n'+str(nodeL_i[node])+'" >')
        lines.append('\t'*3+'<data key="label">'+ node.label+'</data>')
        if node.color:
            lines.append('\t'*3+'<data key="color">'+colorD[node.color]+'</data>')
        if node.info!=''  :
            lines.append('\t'*3+'<data key="info">'+node.info+'</data>')
        lines.append('\t'*2+'</node>')
    
    for node in nodeL:
        for edge in node.edgeL :
            lines.append('\t'*2+'<edge source="n'+str(nodeL_i[node])+'" target="n'+str(nodeL_i[edge.target])+'">')
            if edge.color:
                lines.append('\t'*3+'<data key="ecolor">'+colorD[edge.color]+'</data>')
            if edge.info!=""  :
                lines.append('\t'*3+'<data key="einfo">'+edge.info+'</data>')
            lines.append('\t'*2+'</edge>')
    
    lines.append('\t'*1+'</graph>')
    lines.append('</graphml>')
    
    return lines

def NodeL2DOT(nodeL):
 
    lines=[]
    lines.append('digraph dotgraph {')
    
    for node in nodeL:
        for edge in node.edgeL :
            
            style=[]
            style_str=''
            if edge.label != '':
                style.append='label="'+edge.label+'" '
            if edge.color != '':
                style.append='color='+edge.color+' '
            if len(style)>0:
                style_str=' ['+','.join(style)+']'
            
            lines.append('\t'+node.label +' -> '+edge.target.label+ style_str+ ';')
    
    for node in nodeL:
        style=[]
        if node.color != '':
            style+='color="'+node.color
        
        if len(style)>0:
            lines.append('\t'+node.label+' ['+','.join(style)+']')
            
    lines.append('}')
    
    return lines

def NodeL2txt(nodeL):
    def FollowDown(node,lvl=0):
        lines=[]
        lines.append('\t'*lvl+node.name)
        for edge in node.edgeL:
            lines+=FollowDown(edge.target,lvl+1)
        return lines
        
    lines=[]
    
    topNodeL=GetTopNodes(nodeL)
    for topNode in topNodeL:
        lines+=FollowDown(topNode)
        
    return lines    
    
