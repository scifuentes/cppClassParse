#!/usr/bin/env python

import sys, os
import re
sys.path.append('/home/scifuent/Projects/cParser/vg/')
import graphWriter as gw 


def CollectFiles(paths, fileExtensions=None, skipDirs=None, skipPatterns=None) :
    def MatchExtensions(filename):
        if not fileExtensions:
            return True
        else:
            return any(filename.endswith(ending) for ending in fileExtensions)
    def MatchExclusions(filename):
        if not skipPatterns:
            return False
        else:
            return any(skipPattern in filename for skipPattern in skipPatterns)
    def CollectFiles_R(path): 
        pfiles=[]
        for dirObject in os.listdir(path) :
            if dirObject not in skipDirs:
                dirObjectWithPath= path+os.sep+dirObject
                if os.path.isdir(dirObjectWithPath):
                    pfiles+=CollectFiles_R(dirObjectWithPath)
                else:
                    #links are also taken in
                    if MatchExtensions(dirObject) and not MatchExclusions(dirObject):
                        pfiles.append(dirObjectWithPath)
        return pfiles
    
    files = []
    for path in paths:
        files += CollectFiles_R(path)
    return files


def findFilesWithClasses(paths):
    relevantFiles = CollectFiles(paths,['.cpp','.hpp','.c','.h'],['bld','xifs','tst','Eigen'],['asd', '_data_gen_'])

    filesWithClass = []
    for file in relevantFiles:
        with open(file) as f:
            for line in f.readlines():
                if 'class' in line:
                    filesWithClass.append(file)
    return filesWithClass


def getClassesFromFiles(files):
    class ClassData:
        def __init__(self, name, file, parents):
            self.name = name
            self.file = file
            self.parents = parents
    classes = []

    for file in files:
        with open(file) as f:
            classDefinitions = getClassDefinitions(f.read())
            for classDefinition in classDefinitions:
                classes.append(ClassData(classDefinition.name, 
                                         file, 
                                         extractParents(classDefinition.parents)))
    return classes

re_class=re.compile(r'class\s+(\w+)\s*(:([\w\s:<>,]+))?{',re.MULTILINE)
def getClassDefinitions(fileText):
    class ClassDefinitionData:
        def __init__(self, name, parents=None):
            self.name = name
            self.parents = parents
    matches = re_class.findall(fileText)
    return [ClassDefinitionData(match[0].strip(),match[2].replace('\n','').strip()) for match in matches]

re_parentDef= re.compile(r'((public|protected|private)\s+)?(([\w:]+(<.*>)?)+)')
def extractParents(parentsMatch):
    class ParentData:
        def __init__(self, simpleType, privacy, qualifiedType):
            self.simpleType = simpleType
            self.privacy = privacy
            self.qualifiedType = qualifiedType    
    parents = []
    parentMatch= re_parentDef.findall(parentsMatch)
    for parent in parentMatch:
        privacy = parent[1].strip() if parent[1] != '' else 'private'
        simpleType = re.search('((\w+(<.*>)?)::)*((\w+)(<.*>)?)',parent[2]).group(5)
        qualifiedType = parent[2]
        parents.append(ParentData(simpleType, privacy, qualifiedType))
    return parents


def createClassDiagram(classes, file):
    def createNodeFromClass(clas):
        node = gw.Node(clas.name)
        node.label = clas.name+'\n@'+clas.file
        node.info = clas.file
        node.clas = clas
        return node
    def connectNodes(node,nodes):
        if hasattr(node, 'clas'):
            for parent in node.clas.parents:
                if parent.simpleType in nodes:
                    parentNode = nodes[parent.simpleType]
                else:
                    parentNode = gw.Node(parent.simpleType)
                    if parent.simpleType != parent.qualifiedType:
                        parentNode.label = parent.simpleType +'\n' + parent.qualifiedType
                    nodes[parent.simpleType] = parentNode
                edge = gw.Edge(parentNode)
                edge.label = parent.privacy
                node.edgeL.append(edge)
        
    nodes = {clas.name:createNodeFromClass(clas) for clas in classes}
    for node in nodes.values():
        connectNodes(node, nodes)
    gw.NodeL2File(nodes.values(), file)
    
    
    
    



if __name__ == '__main__':
    filesWithClass = findFilesWithClasses('.')
    classes = getClassesFromFiles(filesWithClass)
    createClassDiagram(classes, '/home/scifuent/public/classes.gml')
    
    
    for clas in classes:
            #if clas.parents and any(['<' in pn for pp,pn in clas.parents]):
            #if len(clas.parents)>1:
            #if not clas.parents:
            #if clas.parents:
            print clas.file, ' => ', clas.name, [parent.privacy+' '+parent.qualifiedType for parent in clas.parents]
    
    