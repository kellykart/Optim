import numpy as np
import random
from copy import deepcopy
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from    sklearn import manifold



def checkSolutionFeasability(sample, nbOfJobs, nbOfPeriods, nbOfMachines, nbOfOperationsPerJob,  timeMachinesPerOperationPerJob, idMachinesPerOperationPerJob):
    # We take all variables equal to 1
    solution = [k for k, v in sample.items() if v == 1]
    # We split according to i, j,
    solution = [(int(x.split('_')[1]),int(x.split('_')[2]),int(x.split('_')[3])    ) for x in solution]
    #
    #
    #
    # Check the feasability of the resource constraint
    for i1 in range(nbOfJobs):
        for j1 in range(nbOfOperationsPerJob[i1]):  
            for p1 in range(nbOfPeriods):
                for i2 in range(nbOfJobs):
                    for j2 in range(nbOfOperationsPerJob[i2]):  
                        for p2 in range(nbOfPeriods):
                            if (i1!=i2) and ((idMachinesPerOperationPerJob[i1][j1] == idMachinesPerOperationPerJob[i2][j2])) and (p2 - p1 < timeMachinesPerOperationPerJob[i1][j1]) and (p2 - p1 >= 0): 
                                # for the var 1:  nameVar1 = "x_" + str(i1) + "_" + str(j1) + "_" + str(p1)           
                                # for the var 2:  nameVar2 = "x_" + str(i2) + "_" + str(j2) + "_" + str(p2)  

                                foundVar1 = False
                                foundVar2 = False 
                                for sol in range(len(solution)):
                                    var_i = solution[sol][0]
                                    var_j = solution[sol][1]
                                    var_p = solution[sol][2]
                                    if var_i == i1 and var_j == j1 and var_p == p1:
                                        foundVar1 = True
                                    elif var_i == i2 and var_j == j2 and var_p == p2:
                                        foundVar2 = True
                                    # If we found both
                                    if foundVar1 and foundVar2:
                                        # The constraint is not satisfied
                                        return False
    #
    #
    #
    # Check the feasability of the resource constraint
    for i1 in range(nbOfJobs):
        for j1 in range(nbOfOperationsPerJob[i1]-1):  
            for p1 in range(nbOfPeriods):
                for p2 in range(nbOfPeriods):
                    if (p1 + timeMachinesPerOperationPerJob[i1][j1] > p2):
                        # for the var 1:  nameVar1 = "x_" + str(i1) + "_" + str(j1) + "_" + str(p1)           
                        # for the var 2:  nameVar2 = "x_" + str(i1) + "_" + str(j1+1) + "_" + str(p2)    

                        foundVar1 = False
                        foundVar2 = False      
                        for sol in range(len(solution)):
                            var_i = solution[sol][0]
                            var_j = solution[sol][1]
                            var_p = solution[sol][2]
                            if var_i == i1 and var_j == j1 and var_p == p1:
                                foundVar1 = True   
                            elif var_i == i1 and var_j == j1+1 and var_p == p2:
                                foundVar2 = True       
                            if foundVar1 and foundVar2:
                                # The constraint is not satisfied
                                return False
    #
    #
    #  Check the Satisfied Operation constraints for all jobs
    for i in range(nbOfJobs):
        for j in range(nbOfOperationsPerJob[i]):    
            counter = 0
            for t in range(nbOfPeriods):
                for sol in range(len(solution)):
                    var_i = solution[sol][0]
                    var_j = solution[sol][1]
                    var_p = solution[sol][2]       
                    if i == var_i and j == var_j and t == var_p:
                        counter = counter + 1
            if counter != 1:
                return False

    print(solution)

    # No constraints had been violated.
    return True
 