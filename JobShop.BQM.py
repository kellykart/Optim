import numpy as np
# Importer methodes pour definir entre autres un modèle ISING
import dimod
# On importe les librairies de DWAVE
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector as inspector
import pandas as pd
from dwave.system.samplers import DWaveSampler
from dimod.binary.binary_quadratic_model import BinaryQuadraticModel
from dimod.vartypes import Vartype

from utils import *




# ------------------------------------------------------------------------------------
#                                   CQM Code (Hybrid)
# ------------------------------------------------------------------------------------


######################### Remarks #########################
# Attention : ici les jobs et opérations commencent à zero
# les numéros des machines données en input commcent à un
 
######################### Mediam Instance Loading #########################

"""
# Constants for mini instance
# Machines, Operations and Jobs start at 0 (=> go to n-1)
nbOfPeriods = 4
nbOfJobs = 2
nbOfMachines = 2
# number of operations per job
nbOfOperationsPerJob = [2, 2]
######################### Lagrange Multipliers #######################
lambda_equalityConst = 20 
lambda_precedenceConst = 20
lambda_ressourceConst = 20
######################### Other Constants #######################
annealsNumber = 10
bigInteger = 999999
"""


# Constants for general instances
# Machines, Operations and Jobs start at 0 (=> go to n-1)
nbOfPeriods = 8
nbOfJobs = 4
nbOfMachines = 4
# number of operations per job
nbOfOperationsPerJob = [4, 4, 4, 4]
######################### Lagrange Multipliers #######################
lambda_equalityConst = 20 
lambda_precedenceConst = 20
lambda_ressourceConst = 20
######################### Other Constants #######################
annealsNumber = 2500
bigInteger = 999999



"""
# Instance n°0 mini instance
#######################################################################
# Precedence constraints - en ligne : le job, et n colonne : l operation
idMachinesPerOperationPerJob = [[1, 2 ], 
                                [2, 1]]
timeMachinesPerOperationPerJob = [[1, 2 ], 
                                  [3, 1 ]]
"""



 
# Instance n°1 Nature Paper
#######################################################################
# Precedence constraints - en ligne : le job, et n colonne : l operation
idMachinesPerOperationPerJob = [[2, 3, 4, 1], 
                                  [4, 3, 1, 2],
                                  [4, 1, 2, 3],
                                  [3, 2, 4, 1]]
timeMachinesPerOperationPerJob = [[1, 1, 1, 1], 
                                  [1, 1, 1, 2],
                                  [2, 1, 2, 1],
                                  [2, 1, 2, 2]]



"""
# Instance n°2 for ICCSA
#######################################################################
# Precedence constraints - en ligne : le job, et n colonne : l operation
idMachinesPerOperationPerJob = [[3,1,2,4], 
                                  [4,1,3,2],
                                  [1,3,4,2],
                                  [2,3,4,1]]
timeMachinesPerOperationPerJob = [[1,1,2,1], 
                                  [2,1,2,1],
                                  [1,1,2,1],
                                  [2,1,2,1]]
"""


 
"""
# Instance n°3 for ICCSA
#######################################################################
# Precedence constraints - en ligne : le job, et n colonne : l operation
idMachinesPerOperationPerJob = [[1,4,2,3], 
                                  [4,2,3,1],
                                  [2,4,3,1],
                                  [3,1,2,4]]
timeMachinesPerOperationPerJob = [[2,2,1,1], 
                                  [1,1,2,2],
                                  [1,1,1,1],
                                  [2,1,1,2]]
"""


"""
# Instance n°4 for ICCSA
#######################################################################
# Precedence constraints - en ligne : le job, et n colonne : l operation
idMachinesPerOperationPerJob = [[2,1,4,3], 
                                  [3,4,2,1],
                                  [1,2,3,4],
                                  [4,3,1,2]]
timeMachinesPerOperationPerJob = [[2,2,2,2], 
                                  [2,1,2,2],
                                  [2,2,2,2],
                                  [3,2,2,2]]


# Instance n°5  for ICCSA
#######################################################################
# Precedence constraints - en ligne : le job, et n colonne : l operation
idMachinesPerOperationPerJob = [[3,4,1,2], 
                                  [1,4,2,3],
                                  [2,4,1,3],
                                  [4,2,3,1]]
timeMachinesPerOperationPerJob = [[3,1,1,1], 
                                  [2,1,1,1],
                                  [1,1,1,1],
                                  [1,2,1,2]]
"""

 













 
###########################################################   
###########################################################
#########################  MODEL  #########################
###########################################################
###########################################################
bqm = BinaryQuadraticModel(Vartype.BINARY)
for i in range(nbOfJobs):
    for p in range(nbOfPeriods) :
        nameVar = "x_" + str(i) + "_" + str(nbOfOperationsPerJob[i]-1) + "_" + str(p)  
        endTimeLastOperation = p+timeMachinesPerOperationPerJob[i][nbOfOperationsPerJob[i]-1]         
        bqm.add_linear(nameVar,endTimeLastOperation)
#        
#
#
#           Satisfied Operation constraints for all jobs
for i in range(nbOfJobs):
    for j in range(nbOfOperationsPerJob[i]):    
        # We consider the constraint with the sum on the periods
        terms = []
        for p in range(nbOfPeriods):
            nameVar = "x_" + str(i) + "_" + str(j) + "_" + str(p)  
            terms.append((nameVar,1))
        bqm.add_linear_equality_constraint(terms,lambda_equalityConst,-1)
        terms.clear
 
#
#
#          Constraints to forbid more than one operation
#           on a machine in the same time
# Here we can directly insert it to the objective function
for i1 in range(nbOfJobs):
    for j1 in range(nbOfOperationsPerJob[i1]):  
        for p1 in range(nbOfPeriods):
            for i2 in range(nbOfJobs):
                for j2 in range(nbOfOperationsPerJob[i2]):  
                    for p2 in range(nbOfPeriods):
                        if (i1!=i2) and ((idMachinesPerOperationPerJob[i1][j1] == idMachinesPerOperationPerJob[i2][j2])) and (p2 - p1 < timeMachinesPerOperationPerJob[i1][j1]) and (p2 - p1 >= 0): 
                            nameVar1 = "x_" + str(i1) + "_" + str(j1) + "_" + str(p1)           
                            nameVar2 = "x_" + str(i2) + "_" + str(j2) + "_" + str(p2)           
                            bqm.add_quadratic(nameVar1,nameVar2,lambda_ressourceConst)
#
#
#          Constraints to forbid overlapping with consecutive
#          operation in a given job
# Here we can directly insert it to the objective function
for i1 in range(nbOfJobs):
    for j1 in range(nbOfOperationsPerJob[i1]-1):  
        for p1 in range(nbOfPeriods):
            for p2 in range(nbOfPeriods):
                if (p1 + timeMachinesPerOperationPerJob[i1][j1] > p2):
                    nameVar1 = "x_" + str(i1) + "_" + str(j1) + "_" + str(p1)           
                    nameVar2 = "x_" + str(i1) + "_" + str(j1+1) + "_" + str(p2)           
                    bqm.add_quadratic(nameVar1,nameVar2,lambda_precedenceConst)                    

print(dict(bqm.linear))

print("\n")

print(dict(bqm.quadratic))

print("\n")

print(bqm.offset)

print("\n")

# ------------------------------------------------------------------------------------
#                                 Quantum Annealing
# ------------------------------------------------------------------------------------
sampler = EmbeddingComposite(DWaveSampler(solver='Advantage_system6.2'))
sampler_name = sampler.properties['child_properties']['chip_id']
sampleset = sampler.sample(bqm, num_reads= annealsNumber)


 
# ------------------------------------------------------------------------------------
#                                 Results Analysis 
# ------------------------------------------------------------------------------------
print("(INITIALISATION) La solution obtenue par recuit quantique ",sampler_name,"est\n")
print(sampleset)
print("\n Une des meilleures solutions est :\n")
bestSolutionSample = sampleset.first.sample
print (bestSolutionSample)
samples =  sampleset.samples()
#Transform the solution in a panda dataframe
dataFrame = sampleset.to_pandas_dataframe(sample_column=True)
"""
dataFrame = dataFrame[['sample','energy','is_feasible']]
dataFrame = dataFrame.sort_values(by = 'energy')
"""
dataFrame.to_csv("./JobShopProblem/JobShopResultBQM.txt")



for i, sample in enumerate(sampleset):
    objective = 2
    feasability = checkSolutionFeasability(sample, nbOfJobs, nbOfPeriods, nbOfMachines, nbOfOperationsPerJob, timeMachinesPerOperationPerJob, idMachinesPerOperationPerJob)
    if feasability:
        print("Sol ", i, "with energy ", objective, " has a Feasability = ", feasability)




 