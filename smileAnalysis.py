from re import search
import pathManage
import parsePDB
import writePDBfile



def searchP (smile):
    
    if search ("P", smile) : 
        return 1
    else : 
        return 0
    
def searchMetal (smile):
    l_metal = ["B", "F", "I", "K", "V", "W", "Y","AG", "AL", "AR" ,"AU", "BA", "BE", "BR", "CA","CD","CE","CF","CL","CO","CR","CS","CU","EU","FE","GA","GD","HE","HF","HG","IN","IR","KR","LA","LI","LU" ,"MG","MN" ,"MO" ,"NA","ND","NE","NI","OS","PB","PD","PR","PT","RB","RE","RU","SB","SE","SI","SM","SR","TA","TB","TE","TL","XE","YB","ZN","ZR"]
    
    smile = smile.upper ()
    smile = smile.replace ("+","")
    smile = smile.replace ("-","")
    smile = smile.replace ("[", "")
    smile = smile.replace ("]", "")
    
    for metal in l_metal : 
        if search("\." + metal + "\.", smile) : 
            return metal
        elif search ("\." + metal + "$", smile) : 
            return metal
        elif search ("^" + metal , smile) : 
            return metal
    return 0

def searchRing (smile):
    
    smile = smile.replace ("[", "")
    smile = smile.replace ("]", "")
    if search ("c1", smile) or search ("C1", smile) : 
        return countlenRing (smile)
    else : 
        return 0
    
    

def countlenRing (smile):
    
    c = 0
    size = len (smile)
    i = 0
    ring_open = 0
    
    while i < size : 
        if ring_open == 0 : 
            if smile[i] == "1" and smile[i-1].upper () == "C":
                c = c + 1
                ring_open = 1
        elif ring_open == 1 : 
            if smile[i] == "(" : 
                ring_open = 2
            elif smile[i].upper () == "C" : 
                c = c + 1
            elif smile[i] == "1": 
                return c
            elif smile[i] != "=" and smile[i] != "[" and smile[i] != "]" and smile[i] != "#" and smile[i] != "@" and smile[i] != "H": 
                return 99
        elif ring_open == 2 : 
            if smile[i] == ")" : 
                ring_open = 1
        
        i = i + 1
    
    return 1       


def searchSulfonyl (smile): 
    
    smile = smile.replace ("[", "")
    smile = smile.replace ("]", "")
    if search("O=S\(=O\)", smile) or search ("S\(=O\)\(=O\)", smile) or  search("S\(=O\)O", smile ) or search("O=S=O", smile) or search ("\(=O\)S\(=O\)", smile) or search ("S\(O\)O", smile): 
        return 1
    else : 
        return 0    
             
def searchCON (smile):
    
    if search ("NC\(=O\)", smile) or search ("C\(=O\)N", smile) : 
        return 1
    else : 
        return 0

def searchCarboxy (smile) :
    if search ("O=C\(O\)", smile) or search ("C\(=O\)O", smile) : 
        return 1
    else : 
        return 0

def searchCandOandN (smile) : 
    
    for at in smile : 
        if search("[a-z,A-Z]", at) : 
            if at.upper() != "C" and at.upper() != "O" and at.upper() != "N" : 
                return 0
    return 1


def searchCandO (smile) : 
    
    for at in smile : 
        if search("[a-z,A-Z]", at) : 
            if at.upper() != "C" and at.upper() != "O" : 
                return 0
    return 1

def searchCandN (smile) : 
    
    for at in smile : 
        if search("[a-z,A-Z]", at) : 
            if at.upper() != "C" and at.upper() != "N" : 
                return 0
    return 1

 
 
def searchConly (smile) : 
    
    for at in smile : 
        if search("[a-z,A-Z]", at) : 
            if at.upper() != "C" : 
                return 0
    return 1
 

def searchReplacement (smile, PDB_query, PDB_ref, name_ligand) : 
    
    metal_find  = searchMetal (smile)
    if metal_find != 0 : 
        p_dir_dataset = pathManage.dataset(name_ligand + "/" + PDB_ref)
        l_PDB_query = pathManage.findPDBQueryDataset(p_dir_dataset)
        for p_query in l_PDB_query : 
            if search (PDB_query, p_query): 
                p_PDB_query = p_query
                break
        if "p_PDB_query" in locals() : 
            l_atom_parsed = parsePDB.loadCoordSectionPDB(p_query)
            l_ions_PDB = parsePDB.retrieveListIon(l_atom_parsed)
            
            if metal_find in l_ions_PDB : 
                l_atom_ion = parsePDB.retrieveLigand(l_atom_parsed, metal_find)
                filout = open (p_dir_dataset + str(metal_find) + "_" + p_query.split("/")[-1], "w")
                for atom_ion in l_atom_ion : 
                    writePDBfile.coordinateSection(filout, atom_ion, recorder = "HETATM", header = str(metal_find), connect_matrix = 0)
                filout.close ()
                return "metal", metal_find
            
    if searchP(smile) == 1 : 
        return "phosphate", ""
    elif searchRing(smile) == 99 : 
        return "cycle",""
    elif searchRing(smile) > 0 : 
        return "cycle",""
    elif searchSulfonyl(smile) : 
        return "SO2",""
    elif searchCON (smile) : 
        return "CON",""
    elif searchCarboxy (smile) : 
        return "COO",""
    elif searchConly(smile) :
        return "onlyC", ""
    elif searchCandO (smile) : 
        return "C+O", ""
    elif searchCandN (smile) : 
        return "C+N", "" 
    elif searchCandOandN (smile) :
        return "C+O+N", ""
    else : 
        return "other"  ,""

 
