import random as rd
import pandas as pd

path= "C:\\Users\\buddha\\Desktop\\calendar_proble_solving"
##classes

class timeset:
    ids = 0
    day =''
    time =0
    def __init__(self,ids,day,time):
        self.ids = ids
        self.day = day
        self.time = time

    def display(self):
        print(self.ids,self.day,self.time)

class room:
    ids = 0
    capacity = 0
    idType = 0
    types = ""
    def __init__(self,ids,cap,idtype,types):
        self.ids = ids
        self.capacity = cap
        self.idType = idtype
        self.types = types

    def display(self):
        print(self.ids,self.capacity,self.idType,self.types)


class lecturer:
    ids = 0 
    idmodule = []
    module = []
    name = ""
    def __init__(self,ids,name,idmodule,modules):
        self.ids = ids
        self.idmodule = idmodule
        self.module = modules
        self.name = name 

    def display(self):
        print(self.ids ,self.idmodule ,self.module ,self.name)

class fixe:
    def __init__(self,niveau,filiere,module,types,goupe,nb):
        self.niveau = niveau
        self.filiere = filiere 
        self.module = module
        self.type = types 
        self.goupe = goupe 
        self.nb = nb
    
    def display(self):
        print(self.niveau,self.filiere,self.module,self.type,self.goupe,self.nb)
#################### NFTG = [Niveau][Filiere][Module][Type][Groupe][Capacité]

d = pd.read_excel(path+"\GA.xlsx",) 

dic = {}
i=0
for item in zip(d["id_niveau"],d["id_filiere"],d["id_module"],d["id_types"],d["id_groupe"],d["nombre_etudiants"]):
    f = fixe(item[0],item[1],item[2],item[3],item[4],item[5])
    dic[i] =f
    i+=1

##################################### ROOM
d = pd.read_excel(path+"\\room.xlsx",) 

dicR = {}
for item in zip(d["id_room"],d["capacity"],d["id_types"],d["type"]):
    r = room(item[0],item[1],item[2],item[3])
    dicR[item[0]] = r

roomRange = len(dicR.keys())

############################## day
d = pd.read_excel(path+"\\day.xlsx",) 

dicD = {}
for item in zip(d["id_timeset"],d["day"],d["time"]):
    ts = timeset(item[0],item[1],item[2])
    dicD[item[0]] = ts

dayRange = len(dicD.keys())

############################## Lecturer
d = pd.read_excel(path+"\\lecturer.xlsx",) 

dicL = {}
for item in zip(d["id_lecturer"],d["name"],d["id_modules"],d["modules"]):
    l = lecturer(item[0], item[1], list(map(int,item[2].split(","))), item[3].split(",") )
    dicL[item[0]] = l

lecturerRange = len(dicL.keys())

#################################################################################
#################################################################################
#################################################################################
#################################################################################

from typing import List  , Tuple

Gen = Tuple[int,int,int,int]
Genome = [Gen]
Population = [Genome]

def generate_population(size: int, data : [int]) -> Population : 
    pop = []
    for _ in range(size):
        H = generate_genome(data)
        pop+=[H]
    return pop

def generate_genome(data : [int]) -> Genome  :
    genome = []
    for gen in data:
        genome.append( generate_gen(gen)  )
    return genome

def generate_gen(idF : int) -> Gen :  #  [idF,lecturer , room , timeset]  , [dicL ,dicR ,  dicD]

    idL = rd.randrange(lecturerRange)
    idR = rd.randrange(roomRange)
    idD = rd.randrange(dayRange)

    return [idF,idL,idR,idD]

pop_size = 2

h = generate_population(pop_size,list(dic.keys()))

#def fitness(genome : Genome):  # [dicL ,dicR ,  dicD]
#    weight = 0
#    size = len(genome)
#
#    for i in range(size):
#        gen1 = genome[i]
#        idL = gen1[1]
#        L = dicL[idL]
#
#        idR = gen1[2]
#
#
#
#
#        for j in range(i+1,len(genome)):
#
#            gen2 = genome[j]
#
#
#    return None


###############################
###############################
############################### Contraint de prof-module

def contraint_prof_module(individu):
    

    
    idProf = individu[1]
    prof = dicL[idProf]

    id_NTFG = dic[individu[0]]
    module = id_NTFG[2]
    verification = 1
    #### qui viole la contrainte
    if str(module) in prof[1]:
        verification = 0
    #return "le prof est : ",prof," le module est : ",module," le poids est : ",verification
    return verification
    
############################# Inserer dans une dataframe les genomes avec leurs evaluations
import pandas as pd

#contraint_prof_module_liste = pd.DataFrame()
contraint_prof_module_population = pd.DataFrame()

for i in range(0,len(h)):
    eval_population = 0
    for j in range(0,len(h[i])):
        #print(h[i][j],contraint_prof_module(h[i][j]))
        #contraint_prof_module_liste = contraint_prof_module_liste.append({'Genome':str(h[i][j]) ,'Evaluation':str(contraint_prof_module(h[i][j]))}, ignore_index=True)
        eval_population = eval_population + contraint_prof_module(h[i][j])
    contraint_prof_module_population = contraint_prof_module_population.append({'Population':h[i],'id_Population':i ,'Evaluation_Population':eval_population}, ignore_index=True)
#contraint_prof_module_liste.to_excel("Contraint_Prof_Module.xlsx")
contraint_prof_module_population.to_excel("Contraint_Prof_Module_ParPopulation.xlsx")

#############################
#############################
############################# Contraint de capacité-groupe
def contraint_capaciteRoom_typesRoom(individu):  
    id_room = individu[2]
    id_NTFG = dic[individu[0]]
    individu_room_capacite = id_NTFG[5] 
    room_capacite = dicR[id_room][1]  
    individu_room_types =  id_NTFG[3]
    room_types = dicR[id_room][2]               
    verification = 1    #### qui viole la contrainte
    if individu_room_capacite <= room_capacite and str(individu_room_types) == str(room_types):
        verification = 0
    #return "la capacite et le type de l'individu est : ",individu_room_capacite,individu_room_types," capacite du room et le type est : ",room_capacite,room_types," le poids est : ",verification   
    return verification

#################################
import pandas as pd

contraint_capaciteRoom_typesRoom_population = pd.DataFrame()
#c = pd.DataFrame()
for i in range(0,len(h)):
    eval_population = 0
    for j in range(0,len(h[i])):
        #print(h[i][j],contraint_prof_module(h[i][j]))
        #c = c.append({'Genome':str(h[i][j]) ,'Evaluation':str(contraint_capaciteRoom_typesRoom(h[i][j]))}, ignore_index=True)
        eval_population = eval_population + contraint_capaciteRoom_typesRoom(h[i][j])
    contraint_capaciteRoom_typesRoom_population = contraint_capaciteRoom_typesRoom_population.append({'Population':h[i],'id_Population':i ,'Evaluation_Population':eval_population}, ignore_index=True)
#c.to_excel("Contraint_capacite.xlsx")
contraint_capaciteRoom_typesRoom_population.to_excel("contraint_capaciteRoom_typesRoom_parPopulation.xlsx") 


##################################
##################################
################################## Contraint de prof-temps


def contraint_prof_temps(populations):
    contraint_prof_temps_population = pd.DataFrame()
    for i in range(0,len(populations)):
        eval_population = 0
        #print("generation",i)
        for j in range(0,len(populations[i])):
            
            for k in range(j+1,len(populations[i])):
                #print(populations[i][k][1],populations[i][j][1],"temps",populations[i][k][3],populations[i][j][3])
                verification = 0
                if str(populations[i][k][1])==str(populations[i][j][1]) and str(populations[i][k][3])==str(populations[i][j][3]) : 
                    verification = 1
                    
                eval_population = eval_population + verification
        #print("la valeur est : ",eval_population)
        contraint_prof_temps_population = contraint_prof_temps_population.append({'Population':h[i],'id_Population':i ,'Evaluation_Population':eval_population}, ignore_index=True)
    contraint_prof_temps_population.to_excel("contraint_prof_temps_population.xlsx") 



contraint_prof_temps(h)

##################################
##################################
################################## Contraint de room-temps


def contraint_room_temps(populations):
    contraint_room_temps_population = pd.DataFrame()
    for i in range(0,len(populations)):
        eval_population = 0
        #print("generation",i)
        for j in range(0,len(populations[i])):
            
            for k in range(j+1,len(populations[i])):
                #print(populations[i][k][2],populations[i][j][2],"temps",populations[i][k][3],populations[i][j][3])
                verification = 0
                if str(populations[i][k][2])==str(populations[i][j][2]) and str(populations[i][k][3])==str(populations[i][j][3]) : 
                    verification = 1
                    
                eval_population = eval_population + verification
        #print("la valeur est : ",eval_population)
        contraint_room_temps_population = contraint_room_temps_population.append({'Population':h[i],'id_Population':i ,'Evaluation_Population':eval_population}, ignore_index=True)
    contraint_room_temps_population.to_excel("contraint_room_temps_population.xlsx") 



contraint_room_temps(h)

##################################
##################################
################################## Contraint de prof-desponibilite

def contraint_prof_disponibilite(individu):  

    idProf = individu[1]
    prof = dicL[idProf]

    temps = individu[3]
    verification = 1
    #### qui viole la contrainte
    if str(temps) in prof[2]:
        verification = 0
    return verification
    
############################# Inserer dans une dataframe les genomes avec leurs evaluations
import pandas as pd

#contraint_prof_disponibilte_liste = pd.DataFrame()
contraint_prof_disponibilite_population = pd.DataFrame()

for i in range(0,len(h)):
    eval_population = 0
    for j in range(0,len(h[i])):
        #print(h[i][j],contraint_prof_disponibilite(h[i][j]))
        #contraint_prof_disponibilte_liste = contraint_prof_disponibilte_liste.append({'Genome':str(h[i][j]) ,'Evaluation':str(contraint_prof_disponibilite(h[i][j]))}, ignore_index=True)
        eval_population = eval_population + contraint_prof_disponibilite(h[i][j])
    contraint_prof_disponibilite_population = contraint_prof_disponibilite_population.append({'Population':h[i],'id_Population':i ,'Evaluation_Population':eval_population}, ignore_index=True)
#contraint_prof_disponibilte_liste.to_excel("Contraint_prof_disponibilite.xlsx")
contraint_prof_disponibilite_population.to_excel("Contraint_Prof_Disponibilite_ParPopulation.xlsx")