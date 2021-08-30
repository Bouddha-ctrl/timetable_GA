import random as rd
import pandas as pd
rd.seed(11)
path= "C:\\Users\\buddha\\Desktop\\calendar_proble_solving\\"
##classes

class timeset:
    ids = 0
    day =''
    time = ''
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
    disponibilite = []
    name = ""
    def __init__(self,ids,name,idmodule,modules,disponibilite):
        self.ids = ids
        self.idmodule = idmodule
        self.module = modules
        self.name = name 
        self.disponibilite = disponibilite

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
for item in zip(d["id_lecturer"],d["name"],d["id_modules"],d["modules"],d["disponibilite"]):
    l = lecturer(item[0], item[1], list(map(int,item[2].split(","))), item[3].split(","),list(map(int,item[4].split(","))) )
    dicL[item[0]] = l

lecturerRange = len(dicL.keys())

#################################################################################
#################################################################################
#################################################################################
#################################################################################

from typing import List, Tuple

Gen = Tuple[int,int,int,int]
Genome = [Gen]
Population = [Genome]


### initialisaion
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

## contraint

prof_module_weight = 15
prof_dispo_weight  = 10
room_cap_weight    = 25
room_type_weight   = 20
room_time_weight   = 30
prof_time_weight   = 30
 
###############################
############################### Contraint de prof-module

def contraint_prof_module(individu): # [idF,lecturer , room , timeset], [dicL ,dicR ,  dicD]
    
    idProf = individu[1]
    prof = dicL[idProf]

    fixe = dic[individu[0]]
    module = fixe.module

    verification = 1
    if module in prof.idmodule:
        verification = 0

    return verification
    
#############################
############################# Contraint de capacité-groupe
def contraint_capaciteRoom(individu):  # [idF,lecturer , room , timeset], [dicL ,dicR ,  dicD]
    id_room = individu[2]
    room_capacite = dicR[id_room].capacity

    fixe = dic[individu[0]]
    student_nb = fixe.nb

    verification = 0
    if room_capacite < student_nb :
        verification += 1 

    return verification

def contraint_typesRoom(individu): # [idF,lecturer , room , timeset], [dicL ,dicR ,  dicD]
    verification = 0

    id_room = individu[2]
    room_types = dicR[id_room].idType  
    
    fixe = dic[individu[0]]
    types_required =  fixe.type

    if room_types != types_required :
        verification = 1
    return verification

#################################
################################## Contraint de disponibilite prof
def contraint_prof_dispo(individu):  # [idF,lecturer ,room ,timeset], [dicL ,dicR ,dicD]
    verification = 0

    individu_time = individu[3]
    prof = dicL[individu[1]]
    
    if individu_time not in prof.disponibilite:
        verification = 1

    return verification 
##################################
################################## Contraint de prof-temps

def contraint_prof_temps(indv1, indv2): # [idF,lecturer , room , timeset], [dicL ,dicR ,  dicD]
    verification = 0

    time1 = indv1[3]
    time2 = indv2[3]

    if time1 == time2:
        idprof1 = indv1[1]
        idprof2 = indv2[1]
        if idprof1 == idprof2:
            verification = 1

    return verification


##################################
################################## Contraint de room-temps

def contraint_room_temps(indv1, indv2): # [idF,lecturer , room , timeset], [dicL ,dicR ,  dicD]
    verification = 0

    time1 = indv1[3]
    time2 = indv2[3]

    if time1 == time2:
        idroom1 = indv1[2]
        idroom2 = indv2[2]
        if idroom1 == idroom2:
            verification = 1

    return verification

##################################


## functions

def fitness(genome : Genome):   # [idF,lecturer , room , timeset], [dicL ,dicR ,  dicD]
    #print(genome)
    Tweight = 0
    size = len(genome)

    for i in range(size):
        weight = 0
        weight += contraint_prof_module(genome[i]) * prof_module_weight
        weight += contraint_prof_dispo(genome[i])  * prof_dispo_weight
        weight += contraint_capaciteRoom(genome[i])* room_cap_weight    
        weight += contraint_typesRoom(genome[i])   * room_type_weight    
        for j in range(i+1,size):
            weight += contraint_room_temps(genome[i],genome[j]) * room_time_weight   
            weight += contraint_prof_temps(genome[i],genome[j]) * prof_time_weight   
        Tweight += weight
    return Tweight

def selection_roulette(popEval, num_parent=2) : #roulette
    maxFitness = max( list(zip(*popEval))[1] )
    return rd.sample(population=popEval,counts=[maxFitness*2 - genome[1] for genome in popEval],k=num_parent)

def selection_random(popEval, num_parent=2):

    return rd.sample(population=popEval,k=num_parent)

def single_point_crossover(genome1 :Genome,genome2 :Genome) -> [Genome,Genome]:
    if len(genome1) != len(genome2) :
        raise ValueError("G1 and G2 not the same lenght")

    if len(genome1) < 2: 
        return genome2 ,genome1

    p = rd.randrange(1,len(genome1))
    
    return genome1[0:p] + genome2[p:] , genome2[0:p] + genome1[p:] 

def all_mutation(genome : Genome,number_of_mutation :int=1, prob : float=0.5) -> Genome:
    for _ in range(number_of_mutation):
        index = rd.randrange(len(genome))
        if rd.random() > prob:
            idL = rd.randrange(lecturerRange)
            idR = rd.randrange(roomRange)
            idD = rd.randrange(dayRange)
            genome[index] = [index,idL,idR,idD] 
    return genome

def one_mutation(genome : Genome,number_of_mutation :int=1, prob : float=0.7) -> Genome:
    for _ in range(number_of_mutation):
        index = rd.randrange(len(genome))

        if rd.random() <= prob:
            columnIndex = rd.randrange(1,4)
            if columnIndex == 1:
                idL = rd.randrange(lecturerRange)
                genome[index] = [index,idL,genome[index][2],genome[index][3]] 

            elif columnIndex==2:
                idR = rd.randrange(roomRange)
                genome[index] = [index,genome[index][1],idR,genome[index][3]] 
            elif columnIndex==3:
                idD = rd.randrange(dayRange)
                genome[index] = [index,genome[index][1],genome[index][2],idD] 
            else : print("error switch")

    return genome

def evolution(fitness_funct, selection_pair, crossover, mutation, generation_limit :int ,pop_size :int ):
    pop = generate_population(pop_size,list(dic.keys()))

    for i in range(generation_limit):

        popEval = []
        for k in range(pop_size):
            popEval.append( [pop[k],fitness_funct(pop[k])] )
        popEval = sorted(popEval,key=lambda genome:genome[1])

        print("gen :",i," liste:",list(zip(*popEval))[1][:10])

        next_generation = [popEval[0][0],popEval[1][0]]
       
       
        for j in range(pop_size//2-1):

            genomeEval1, genomeEval2 = selection_pair(popEval)
            genome1, genome2 = crossover(genomeEval1[0], genomeEval2[0])
        
            genome1 = mutation(genome1)
            genome2 = mutation(genome2)
            next_generation += [genome1,genome2]  
        
        pop = next_generation
        
evolution(fitness_funct= fitness,
            selection_pair = selection_roulette,
            crossover= single_point_crossover,
            mutation= all_mutation,
            generation_limit = 500,
            pop_size=100)

