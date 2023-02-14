from os import listdir
from os.path import isfile, join
import os
import networkx as nx


def getInformation(line):
    subs = line.split()
    subs = list(filter(None, subs))
    return subs
def createNodes(lines, defineuselist, nodes, cfnodelist,path):
    counter = 0
    for l in lines:
        if l[0] != "}" and l[1] != None:
            if l[1] != "->":
                node = Node(l[0],counter)
                nodes.append(node)
                
                counter = counter +1
            elif "DDG" in l[6]:
                index = next((i for i, item in enumerate(nodes) if item.Name == l[0]), -1)
                
                defi = (nodes[index])
                index2 = next((i for i, item in enumerate(nodes) if item.Name == l[2]), -1)
                
                use = nodes[index2]
                dunode = DUNode(defi,use)
                defineuselist.append(dunode)
            elif "CDG" in l[6]:
                
                index = next((i for i, item in enumerate(nodes) if item.Name == l[0]), -1)
                 
                init = (nodes[index])
                index2 = next((i for i, item in enumerate(nodes) if item.Name == l[2]), -1)
                
                dom = nodes[index2]
                cfnode = CFNode(init,dom)
                cfnodelist.append(cfnode)
            else:
                print("made it to else")    
           


class Node:
    def __init__(self, Name, Line):
        self.Name = Name
        self.Line = Line
       
    def __str__(self):
     return f"  Name: {self.Name}"   

class DUNode(Node):
    def __init__(self, defi, use):
        self.defi = defi
        self.use = use

class CFNode(Node):
  def __init__(self, initial, dominator):
        self.initial = initial
        self.dominator = dominator
        
def main():
    mypath1 = "./pdgs/Vul"
    mypath2 = "./pdgs/No-Vul"
    onlyfiles1 = [f for f in listdir(mypath1) if isfile(join(mypath1, f))]
    
    for file in onlyfiles1:
        
        go(file,"Vul/")

    onlyfiles2 = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
    
    for file in onlyfiles2:
        
        go(file,"No-Vul/")
    #go("CVE_raw_000087785_CWE195_Signed_to_Unsigned_Conversion_Error__fgets_strncpy_12_bad.dot")
def go(path,folder):
    lines = []
    defineuselist = []
    cfnodelist = []
    nodes = []
    
    f = open("./pdgs/"+folder +path, "r")
    line = f.readline()
    line = f.readline()
        
    while(line != None):
        #print(line)
        if not line:
            break
        lines.append(getInformation(line))
        line = f.readline()
    if(f != None):
        f.close()
            
    
    
    createNodes(lines, defineuselist, nodes,cfnodelist,path)

    dicts = {}
    keys = range(len(nodes))
    l = []
    for i in keys:
        l.append(chr(nodes[i].Line))
        dicts[i] = l
        l.clear()
    #print(dicts)
    #g = graph(dicts) #might not need the variables
    #print(g.returndic())
    G = nx.DiGraph()
    G.add_nodes_from(keys)

    
    for nd in defineuselist:
        #print(nd.defi.Line , nd.use.Line)
        G.add_edge(nd.defi.Line, nd.use.Line)
    
    #print(g.returndic())    
    
    for cf in cfnodelist:
        #print(cf.initial.Line, cf.dominator.Line)
        G.add_edge(cf.initial.Line, cf.dominator.Line)

    #print("EDGES")

    #print(g.edges()) 
    #print("vertices")
    #print(g.getVertices())
    #print(g) 
    newfile = open("sliced.txt", "w+")
    forwardslicematrix = []
    values = range(len(nodes))
    
    visited = [] # List for visited nodes.
    queue = []     #Initialize a queue 

    for a in values:
        newfile.write("LINE: " +str(a))
        newfile.write("NODE:"+ nodes[a].Name)
        #print(g.returndic())
        edges = nx.bfs_edges(G, a)
        slice = [a] + [v for u, v in edges]
        #print(len(slice))
        #print(len(nodes))
        
       
        forwardslicematrix.append(((float(len(slice)-1))/(float(len(nodes)))))
        for node in nodes:
            if node.Line in slice:
                newfile.writelines(str(node.Line) + "\n")
    
    newfile.close()
    
    
    substring = path[0:int(len(path)-4)]
    
    outputpath = "./dictionaries/" + folder
    isExist = os.path.exists(outputpath)
    if not isExist:
   # Create a new directory because it does not exist
        os.makedirs(outputpath)
    fp = open(outputpath+substring+".txt","w+")
    b = 0
    for node in nodes:
        name = node.Name[1:]
        name = name[:-1]
        fp.write(name + " " + str(forwardslicematrix[b])+ "\n")
        b = b+1
    fp.close()

main()
