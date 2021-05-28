# Thiago Costa Amaral
#

import random
import turtle
import time

class Genetic_obj:
    num_of_obj = 0
    def __init__(self,generation,ID,genotype,fenotype,fit=None):
        self.ID=ID             
        self.genotype = genotype
        self.fenotype = fenotype
        self.generation = generation
        if fit == None:
            self.fit=0
        else:
            self.fit=fit
        Genetic_obj.num_of_obj +=1

    def info(self):
        print("--- \nObj_Generation = %d ; Obj_ID = %d; Obj_fit = %.3f" %(self.generation,self.ID,self.fit))
        print("Obj_genotype = ",end="")
        print(self.genotype, end="\n---\n")

        
class Traveler(Genetic_obj):
    num_of_travelers=0
    def __init__(self,generation,ID,genotype,fenotype,fit):
        super().__init__(generation,ID,genotype,fenotype,fit)                    
        Traveler.num_of_travelers +=1

    def mutation(self,probability):
        ''' The mutation process
            is based in the idea of permutacion
            between the elements of the list
        '''
        p=probability
        #Variable to change without modifing original
        genotype=[]                                                     
        for i in range(len(self.genotype)):
            genotype.append(self.genotype[i])
        #
        for i in range(len(self.genotype)-1):                           #The first city will not change
            if p > random.randint(0,100)/100:                           #The permutacion will occur to element i?
                elem_change = random.randint(1,len(self.genotype)-1)    #Definicion of which element with permute with element i
                #---Process of permutancion -------------
                control=genotype[i+1]                                #Variable to control permutacion
                genotype[i+1]=genotype[elem_change]
                genotype[elem_change]= control
                #---------------------------------------

        self.genotype=genotype

    def mutation2(self,probability):
        '''
            Moves a element to another position of the list, maintaining the mains "routes"
            [1,2,3,4,5] ---> [1,2,5,3,4]
        '''
        p = probability
        genotype=[]
        control=[]
        for i in range(len(self.genotype)):
            genotype.append(self.genotype[i])
            control.append(self.genotype[i])
        #
        for i in range(len(self.genotype)-1):                           #The first city will not change
            m=i+1
            if p > random.randint(0,100)/100:                           #The permutacion will occur to element i?
                elem_pos = random.randint(1,len(self.genotype)-1)       #Definicion of which element with permute with element i
                #---Process of movement -------------
                if i+1<elem_pos:
                    control=genotype[0:m]+genotype[m+1:elem_pos+1]+[genotype[m]]+genotype[elem_pos+1:]
                    genotype=control
                elif i+1>elem_pos:
                    control=genotype[0:elem_pos]+[genotype[m]]+genotype[elem_pos:m]+genotype[m+1:]
                    genotype=control
        self.genotype=genotype
                
def best_index(lista):
    'Returns the best ID in form of a list --> [better ...... worse]'
    'Remember that lista have already all the fenotypes in order with the ID'
    elements=len(lista)
    max_valor=max(lista)+1
    best_ID=[]
    for i in range(elements):
        better_val=max_valor
        better_ID=0
        for j in range(elements):
            if lista[j]<better_val:
                better_val=lista[j]
                better_ID=j
        lista[better_ID]=max_valor
        best_ID.append(better_ID)
    return best_ID
        


def distance2(Obj,cities_d):
    dist=0
    n_cities=len(cities_d)
    for i in range(n_cities):
        if i < (n_cities-1):
            before = Obj.genotype[i]
            after = Obj.genotype[i+1]
        else:                       #The traveler needs to go back to the firs city
            before = Obj.genotype[i]
            after  = Obj.genotype[0]
        dist = dist + cities_d[before][after]
    Obj.fenotype = dist
    return dist

def optimization_1(Obj,cities_d):
    n_cities=len(Obj.genotype)
    dist_min=Obj.fenotype
    Worked = False
    for j in range (n_cities-1):
        for i in range(n_cities):
            control=Obj.genotype[i]
            Obj.genotype[i]=Obj.genotype[j]
            Obj.genotype[j]=control
            if distance2(Obj,cities_d)>=dist_min:
                Obj.genotype[j]=Obj.genotype[i]
                Obj.genotype[i] = control
            else:
                Worked =True
    dist_min=distance2(Obj,cities_d)
    return Worked

def optimization_2(Obj,cities_d,n):
    'Takes a block and mirror it --> try to remove connections'
    n_cities=len(Obj.genotype)
    dist_min=Obj.fenotype
    Worked = False
    copy=[]
    for i in range(n_cities):
        copy.append(Obj.genotype[i])
    for j in range(n_cities):
        block=[]
        #####Constructions of blocks that will "sofer" mirror ############3
        for b in range(n):                  
            control=j+b
            if control>n_cities-1:
                control=control-n_cities
            block.append(Obj.genotype[control])
        block.reverse()       #Mirror de list
        ################################################
        #print(Obj.genotype)
        ####Process to mirror the genotype
        for i in range(n):
            control= j+i
            if control>n_cities-1:
                control=control-n_cities
            Obj.genotype[control]=block[i]
        #print(Obj.genotype)
        #Verifing new obj
        
        #print(distance(Obj,cities))
        if distance2(Obj,cities_d)>=dist_min:     #Obj did not improve
            block.reverse()
            for i in range(n):
                control= j+i
                if control>n_cities-1:
                    control=control-n_cities
                Obj.genotype[control]=block[i]
            #print(Obj.genotype)
            distance2(Obj,cities_d)
            #print(distance2(Obj,cities_d))
        else:                                  #Obj improve
            Worked = True
            print("funcionou",end="")
            print(Obj.fenotype)
            dist_min=Obj.fenotype
    return Worked


def selection(list_of_Obj):
    n_obj = len(list_of_Obj)
    #probability of living based of "relative position"
    probability=[1/2]
    for i in range(n_obj-2):
        probability.append(1/2**(i+2) + probability[i])
    probability.append(1)
    #Seach for the best individuals
    fenotypes=[]            #list of fenotypes
    for i in range(n_obj):
        fenotypes.append(list_of_Obj[i].fenotype)
    #Definicion of best IDs
    best_ID=best_index(fenotypes)
    #Construction of new generation
    new_generation=[]
    for j in range(n_obj):
        prob_numb =random.randint(0,1000)/1000          #Number that will determine which obj will be selected
        for i in range(n_obj):
            if prob_numb <= probability[i]:
                new_generation.append(list_of_Obj[best_ID[i]])
                break
        new_generation[j].ID=j
    #print(len(new_generation))
    list_of_Obj=new_generation


            
def main():
    print("\n ------------------\nPROBLEM OF THE TRAVELER TRYING TO FIND THE SMALLER ROAD \n------------------\n")
    #-----Definitions-----
    n_cities=50
    n_generations=1
    num_of_obj = 50000
    Mutation_prob=0.1
    #Cities where the traveler needs to go
    cities=[]
    for i in range(n_cities):
        cities.append([random.randint(-250,250),random.randint(-250,250)])
    n_cities=len(cities)

    cities_d=[]
    #Matrix of distances 
    for i in range(n_cities):
        line=[]
        for j in range(n_cities):
            d= ((cities[i][0] - cities[j][0])**2 +   (cities[i][1] - cities[j][1]  )**2 )**0.5
            line.append(d)
        cities_d.append(line)
    #Ploting of the cities in the "Map"
    Travel=turtle.Pen()
    Travel.speed(0)
    Travel.penup()
    for i in range (n_cities):
        Travel.goto(cities[i][0],cities[i][1])
        Travel.dot()   
    Travel.goto(cities[0][0],cities[0][1])
    #Definicon of Genetic objects
    Gen_Objs=[]
    genotype_base =[]
    for i in range(n_cities):
        genotype_base.append(i)
    
    for i in range(num_of_obj):
        Gen_Objs.append(Traveler(0,i,genotype_base,0,0))
        Gen_Objs[i].mutation(Mutation_prob)
        #print(Gen_Objs[i].genotype)

    better_ID=0
    #-------------------Genetations--------------------------
    for j in range(n_generations):
        better_fen = distance2(Gen_Objs[0],cities_d)
        
        #Mutation process
        for i in range(num_of_obj):
            if i != better_ID and j<n_generations/2:
                Gen_Objs[i].mutation(Mutation_prob)             #---> At least one genect obj will not change --->(The better one)
            elif i != better_ID and j>=n_generations/2:
                Gen_Objs[i].mutation2(Mutation_prob)
            #print(Gen_Objs[i].genotype)
            Gen_Objs[i].generation +=1
        #fenotype verification and definicion of better fenotype (already seen the ID)
        for i in range(num_of_obj):
            dist = distance2(Gen_Objs[i],cities_d) #------> !!!!!!Funcion already change fenotype of object!!!!!!  <-----------
            if dist<better_fen:
                better_fen=dist
                better_ID=i
        #Presentation of better results
        print("BETTER RESULT OF GENERATION %d" %(Gen_Objs[i].generation))
        print("Obj_ID = %d Distance = %3f"%(better_ID,better_fen))
        print("Obj_genotype = ",end="")
        print(Gen_Objs[better_ID].genotype, end="\n---\n")
        #Defining new population of objects
        if j<n_generations-1:
            selection(Gen_Objs)
        else:
            Op_Obj=Traveler(j+1,0,Gen_Objs[better_ID].genotype,better_fen,0)
            Worked=True
            while(Worked):
                Worked = optimization_1(Op_Obj,cities_d)
                print(Op_Obj.fenotype)
            print("BETTER RESULT OF OPTIMIZATION %d" %(0))
            print("Obj_ID = %d Distance = %3f"%(better_ID,Op_Obj.fenotype))
            print("Obj_genotype = ",end="")
            print(Op_Obj.genotype, end="\n---\n")
            print(Gen_Objs[better_ID].genotype)
            ############# destroying all the nodes ---->max elements in node are n_cities/2
            j=n_cities//2+1
            for i in range(n_cities//2+1):
                Worked=True
                while(Worked):
                    print(j)
                    Worked=optimization_2(Op_Obj,cities_d,j)
                    #print("boooom")
                    #print(Op_Obj.fenotype)
                j=j-1
                print("BETTER RESULT OF OPTIMIZATION %d" %(i+1))
                print("Obj_ID = %d Distance = %3f"%(better_ID,Op_Obj.fenotype))
                #print("Obj_genotype = ",end="")
                #print(Op_Obj.genotype, end="\n---\n")
                #print(Gen_Objs[better_ID].genotype)
    #Printing result on screen
    print(cities)
    Travel.goto(cities[Gen_Objs[better_ID].genotype[0]][0],cities[Gen_Objs[better_ID].genotype[0]][1]) 
    Travel.pendown()
    for i in range (n_cities):
        Travel.goto(cities[Gen_Objs[better_ID].genotype[i]][0],cities[Gen_Objs[better_ID].genotype[i]][1])    
    Travel.goto(cities[Gen_Objs[better_ID].genotype[0]][0],cities[Gen_Objs[better_ID].genotype[0]][1])                  #Volta para o ponto de partida
    time.sleep(30)
main()
