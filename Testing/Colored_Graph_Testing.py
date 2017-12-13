# coding=utf-8

'''
Created on 13 lug 2017

@author: Andrea Montanari

This class is a testing about Colored Graphs, 3-colorability.
The Graphs colored have 10 and many more variables. 
The aim is to analyze the average of the rmessages differences
which tends to 0, and that the number of conflicts tends to 0.
The results are: report about the average of the rmessages differences, 
factor graph of Dcop, the charts about the average of the rmessages differences
and the conflicts during the iterations.
The results are saved as chart (.png) and as log file (.txt)
'''

import sys, os
from collections import defaultdict
import random
import matplotlib.pyplot as pl
import argparse

sys.path.append(os.path.abspath('../maxsum/'))
sys.path.append(os.path.abspath('../solver/'))
sys.path.append(os.path.abspath('../system/'))
sys.path.append(os.path.abspath('../Graph/'))
sys.path.append(os.path.abspath('../misc/'))
sys.path.append(os.path.abspath('../function/'))

from Agent import Agent
from NodeVariable import NodeVariable
from NodeFunction import NodeFunction
from TabularFunction import TabularFunction
from NodeArgument import NodeArgument
from COP_Instance import COP_Instance
from MaxSum import MaxSum


def main():    
    '''
        invoke the parser that takes parameters from the command line
    '''
    args = getParser()
    '''
        How many iterations?
    '''
    nIterations = args.iterations
    '''
        How many instances? 
    '''    
    nIstances = args.instances
    '''
        number of variables in Dcop
    '''
    nVariables = args.variables
    '''
        max/min
    '''
    op = args.op
    '''
        location of MaxSum report
    '''
    reportMaxSum = args.reportMaxSum 
    '''
        create a directory for reports if it isn't exist
    '''
    directory = os.path.dirname(reportMaxSum + "/TestingColoring/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    '''
        location of FactorGraph report
    '''
    infoGraphPathFile = args.reportFactorGraph
    '''
        create a directory for reports if it isn't exist
    '''
    directory = os.path.dirname(reportMaxSum + "/FactorGraph/")
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    '''
        location of Charts
    '''
    chartsFile = args.reportCharts    
    '''
        create a directory for charts if it isn't exist
    '''
    directory = os.path.dirname(reportMaxSum + "/Charts/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    '''
        Constraint Optimization Problem
    '''
    cop = None
    '''
        average of rmessages difference for each link
    '''        
    rMessagesAverageDifference = defaultdict(dict)
    '''
        average of rmessages difference for each link and for each iteration
    '''
    rMessagesAverageDifferenceIteration = list()
    
    for i in range(nIterations):
        rMessagesAverageDifferenceIteration.append(0)       
    
    for run in range(nIstances): 
            '''
                fileName of log (Iteration Conflicts AverageDifferenceLink)
                save on file Iteration Conflicts AverageDifferenceLink
            '''                        
            fileOutputReport = reportMaxSum + "TestingColoring/TestingColoring_Report_RUN_" + str(run) + ".txt"
            '''
                values of MaxSum for each iteration
            '''
            values = list()
        
            for j in range(nIterations):
                rMessagesAverageDifferenceIteration[j] = 0       
          
            '''
                create a new COP with a colored Graph and 
                save the factorgraph on file
            '''
            cop = create_DCop(infoGraphPathFile, nVariables, run)                              
            '''
                create new MaxSum instance (max/min)
            '''            
            core = MaxSum(cop, op) 
            '''
                update only at end?
            '''
            core.setUpdateOnlyAtEnd(False)    

            core.setIterationsNumber(nIterations)
                                                            
            '''
                invoke the method that executes the MaxSum algorithm
            '''
            core.solve_complete()
            '''
                values of MaxSum for each iteration in this instance
            '''
            values = core.getValues()
            '''
                average of rmessages difference in the instance
            '''
            rMessagesAverageDifference = core.getRmessagesAverageDifferenceIteration()
            
            '''
                number of link in factor graph
            '''
            links = 0
                          
            for key in rMessagesAverageDifference.keys():
                for value in rMessagesAverageDifference[key]:
                    '''
                       count how many links there are
                    '''
                    links = links + 1
                    
                    '''
                        add all the averages of the differences of each link for each iteration
                    '''
                    for k in range(len(rMessagesAverageDifference[key][value])):
                        rMessagesAverageDifferenceIteration[k] = rMessagesAverageDifferenceIteration[k] + (rMessagesAverageDifference[key][value])[k]     
                        
            '''
                calculates the average of the differences
            '''
            for k in range(len(values)):
                rMessagesAverageDifferenceIteration[k] = rMessagesAverageDifferenceIteration[k] / links
                 
            
            final = "\tITERATION\tCONFLICTS\tAVERAGE_DIFFERENCE_LINK\n"              
            
            for i in range(len(values)):
                final = final + "\t" + str(i) + "\t\t" + str(values[i]) + "\t\t" + str(rMessagesAverageDifferenceIteration[i]) + "\n"

            '''
                save on file the log file
            '''
            core.stringToFile(final, fileOutputReport)
                
            
            # draw the chart 
            # x axis: number of iterations
            # y axis: average of the differences in the R messages
            x = list()
            
            '''
                x axis: iterations
            '''
            for i in range(nIterations):
                x.append(i)
        
            pl.xticks([20 * k for k in range(0, 16)])
            
            y = rMessagesAverageDifferenceIteration
            pl.title('Iteration / MediaDiffLink chart')
            pl.xlabel('Iterations')
            pl.ylabel('Average_Difference_Link')
            pl.plot(x, y)
            # pl.show()
            pl.savefig(chartsFile + "Charts/ChartMediaDiffLink_RUN_" + str(run) + ".png")
            pl.close()
            
            
            
            # draw the chart 
            # x axis: number of iterations
            # y axis: values of MaxSum (value < 0 = conflict)
            x = list()
            
            '''
                x axis: iterations
            '''
            for i in range(nIterations):
                x.append(i)
            
            y = values
                                      
            pl.xticks([20 * k for k in range(0, 16)])
        
            pl.title('Iteration / Conflict chart')
            pl.xlabel('Iterations')
            pl.ylabel('Values')
            pl.plot(x, y)
            # pl.show()
            pl.savefig(chartsFile + "Charts/ConflictsChart_RUN_" + str(run) + ".png")
            pl.close()
            
                                                        
def create_DCop(infoGraphPathFile, nVariables, run):
    '''
        infoGraphPathFile: location where saving the factor graph
        This function creates a colored graph with one agent that controls
        variables and functions. Each variable has 3 values in its domain (0,1,2).
        For each variable there is a a fictitious function useful for 
        breaking the symmetry of colorability.
        nVariables: how many variables are there in Dcop instance?
        run: number of Dcop instance 
    '''
    
    '''
        configurations of variables's values in a function:
        0 0, 0 1, 0 2, 1 0 ....
    '''
    arguments = [0, 0, 0, 1, 0, 2, 1, 0, 1, 1, 1, 2, 2, 0, 2, 1, 2, 2]
    
    '''
        list of variable in Dcop
    '''
    nodeVariables = list()
    '''
        list of function in Dcop
    '''
    nodeFunctions = list()
    '''
        list of agents in Dcop
        In this case there is only one agent
    '''
    agents = list()
    
    '''
        agent identifier
    '''    
    agent_id = 0
    '''
        variable identifier
    '''
    variable_id = 0
    '''
        function identifier
    '''
    function_id = 0
    '''
        variable identifier as parameter in the function
    '''
    variable_to_function = 0
    
    '''
        list of arguments in the function
    '''
    argumentsOfFunction = list()
    
    '''
       each variable has 3 values in its domain (0..2) 
    '''
    number_of_values = 3    
    
    '''
        only one agent controls all the variables and functions
    '''
    agent = Agent(agent_id)  
    
    nodeVariable = None
    nodefunction = None
    functionEvaluator = None     
    '''
        it is True if it is possible to create an edge between node j and node u
     ''' 
    found = False
    '''
        it is True if it is possible to color the node u
    '''
    colored = False
    '''
        if It is true you can create an edge with the next variable (bigger id)
        else you can't do it
    '''
    k = 0   
    '''
        activation probability (random) to create an edge
    '''
    p = None
     
    '''
        create nVariables dcop variables
    '''
    for j in range(nVariables):
        '''
            create new NodeVariable with variable_id
        '''     
        nodeVariable = NodeVariable(variable_id)
        '''
            create the variable's domain with 3 values (0,1,2)
        '''
        nodeVariable.addIntegerValues(number_of_values)
        '''
            append this variable to Dcop's list of variable
        '''
        nodeVariables.append(nodeVariable)
            
        '''
           add the variable under its control
        '''
        agent.addNodeVariable(nodeVariable)
            
        variable_id = variable_id + 1  
  
    
    '''
        for each variable in Dcop's list
    '''
    for j in range(0, len(nodeVariables)):        
        '''
            if the variable j has not taken on a color
        '''
        if(((nodeVariables[j]).getColor()) == -1):
            '''
                choose a random color between 0 and 2
            '''
            val = random.randint(0, 100)
            if(val < 50):
                '''
                    choose 0
                '''
                (nodeVariables[j]).setColor(0)
            elif(val >= 50 & val < 70):
                '''
                    choose 1
                '''
                (nodeVariables[j]).setColor(1)
            else:
                '''
                    choose 2
                '''
                (nodeVariables[j]).setColor(2)     
        
        ''''
            if it is the first node variable
            it can create an edge with the next node.
            So there is no cycle
        '''          
        if ((nodeVariables[j]).getId() == 0):
            k = j + 1
        else:
            '''
                else you can't create an edge with the next node variable, to 
                avoid cycles
            '''
            k = j + 2
        
        '''
            for each variable close to variable j with bigger id 
        '''
        for u in range(k, len(nodeVariables)):   
            
            color_neighbour_j = list()        
            '''
                neighbors can assume one in three color types (0,1,2)
            '''
            color_neighbour_j.append(0)
            color_neighbour_j.append(1)
            color_neighbour_j.append(2)
            '''
                remove the variable j's color
            '''
            color_neighbour_j.remove(nodeVariables[j].getColor())  
            
            '''
                function nodes close to the variable j
            '''
            function_neighbour_j = (nodeVariables[j]).getNeighbour()
            
            '''
                remove the colors of the neighbors at the variable j
            '''
            for function in function_neighbour_j:
                for variable in function.getNeighbour():
                        if(not((variable.getId()) == (nodeVariables[j].getId()))):
                            '''
                                if you can remove a color
                            '''
                            if(len(color_neighbour_j) > 0):
                                index = search_Index(color_neighbour_j, variable.getColor())
                                if(index > -1):
                                    color_neighbour_j.remove(color_neighbour_j[index])

            found = False 
            colored = False                   
                
            '''
                generate a random value to enable the edge (if p > 50)
            '''                
            p = random.randrange(0, 100)    
                
            '''
                if the two nodes have different colors
            '''  
            if((not((nodeVariables[j].getColor()) == (nodeVariables[u].getColor()))) & (p > 50)):
                '''
                    if variable u doesn't have a color and variable j has neighbours
                '''
                if(((nodeVariables[u]).getColor()) == -1):        
                    '''
                        in variable j has 2 available colors
                    '''                   
                    if(len(color_neighbour_j) == 2):
                        index = 0
                        '''
                            choose the color index to select, choose a color from those left
                        '''
                        val = random.randint(0, 100)
                        if(val < 50):
                            index = 0
                        else:
                            index = 1
                           
                        '''
                            set the color based on the index choosen
                        ''' 
                        (nodeVariables[u]).setColor(color_neighbour_j[index])
                        color_neighbour_j.remove(color_neighbour_j[index])

                        '''
                            it is possible to color node u
                        '''
                        colored = True
                    elif(len(color_neighbour_j) == 1):
                        '''
                            if there is only one available color for variable u
                        '''
                        (nodeVariables[u]).setColor(color_neighbour_j[0])
                        color_neighbour_j.remove(color_neighbour_j[0])
                                     
                        '''
                            it is possible to color node u
                        '''
                        colored = True
                elif(((nodeVariables[u].getColor()) > -1) & (p > 50)):
                    
                    if(len(function_neighbour_j) == 0):
                    
                        color_neighbour_u = list() 
                        '''
                            neighbors can assume one in three color types (0,1,2)
                        ''' 
                        color_neighbour_u.append(0)
                        color_neighbour_u.append(1)
                        color_neighbour_u.append(2)
                            
                        '''
                            the color of node u can not be used
                        '''           
                        color_neighbour_u.remove(nodeVariables[u].getColor())
                        
                        function_neighbour_u = (nodeVariables[u]).getNeighbour()   
                            
                        '''
                            remove the colors of the neighbors at the variable u
                        '''
                        for function in function_neighbour_u:
                            for variable in function.getNeighbour():
                                if(not((variable.getId()) == (nodeVariables[u].getId()))):
                                    if(len(color_neighbour_u) > 0):
                                        index = search_Index(color_neighbour_u, variable.getColor())
                                        if(index > -1):
                                            color_neighbour_u.remove(color_neighbour_u[index])    
                            
                        '''
                            if node u has at least an available color
                        '''                
                        if(len(color_neighbour_u) > 0):
                            for color in color_neighbour_u:
                                '''
                                    if there is the color in the available colors of variable j
                                '''
                                if(color == (nodeVariables[j].getColor())):
                                    '''
                                        you can create an adge between node j and node u
                                        because they have different colors and their neighbours
                                        don't use color
                                    '''
                                    found = True
                                
                    elif((len(function_neighbour_j) > 0)):
                        
                        color_neighbour_u = list() 
                                                
                        '''
                            neighbors can assume one in three color types (0,1,2)
                        '''                                     
                        color_neighbour_u.append(0)
                        color_neighbour_u.append(1)
                        color_neighbour_u.append(2)
                            
                        '''
                            the color of node u can not be used
                        '''           
                        color_neighbour_u.remove(nodeVariables[u].getColor())
                        
                        function_neighbour_u = (nodeVariables[u]).getNeighbour()          
                            
                        '''
                            remove the colors of the neighbors at the variable u
                        '''
                        for function in function_neighbour_u:
                            for variable in function.getNeighbour():
                                if(not((variable.getId()) == (nodeVariables[u].getId()))):
                                    if(len(color_neighbour_u) > 0):
                                        index = search_Index(color_neighbour_u, variable.getColor())
                                        if(index > -1):
                                            color_neighbour_u.remove(color_neighbour_u[index])                              
                            
                        '''
                            if node u and node j have at least an available color
                        ''' 
                        if((len(color_neighbour_u) > 0) & (len(color_neighbour_j)) > 0):   
                            found_j = False
                            found_u = False
                            
                            '''
                                if color j is available in color_u
                            '''
                            for color in color_neighbour_u:
                                if((nodeVariables[j].getColor()) == color):
                                    found_j = True
                            '''
                                if color u is available in color_j
                            '''            
                            for color in color_neighbour_j:
                                if(color == (nodeVariables[u].getColor())):
                                    found_u = True
                            
                            '''
                                you can create an edge between the two variables
                            '''        
                            if((found_j == True) & (found_u == True)):
                                found = True
                            else:
                                found = False
                        
                if ((colored == True) | (found == True)):    
                    '''
                        if you can create an edge between the two node
                    '''
                                           
                    '''
                       list of the arguments of the function 
                       each function is binary
                    '''          
                    argumentsOfFunction = list()
                                
                    nodefunction = NodeFunction(function_id)
                                
                    functionEvaluator = TabularFunction()  
                    nodefunction.setFunction(functionEvaluator)
                                
                    '''
                        id variable in the function
                    '''
                    variable_to_function = nodeVariables[j].getId()
                                
                                
                    '''
                        add the function_id function to the neighbors 
                        of variable_to_function
                    '''    
                    for v in range(len(nodeVariables)):
                        if nodeVariables[v].getId() == variable_to_function:
                            '''
                                add this nodefunction to the actual nodevariable's neighbour
                            '''
                            nodeVariables[v].addNeighbour(nodefunction)
                                        
                            '''
                                add this variable as nodefunction's neighbour
                            '''
                            nodefunction.addNeighbour(nodeVariables[v])
                            '''
                                add the variable as an argument of the function
                            '''      
                            argumentsOfFunction.append(nodeVariables[v])
            
            
                    '''
                        id variable in the function
                    '''
                    variable_to_function = nodeVariables[u].getId()
                                
                    '''
                        add the function_id function to the neighbors of variable_to_function
                    '''    
                    for v in range(len(nodeVariables)):
                        if nodeVariables[v].getId() == variable_to_function:
                                
                            '''
                                add the function as close to the variable
                            '''
                            nodeVariables[v].addNeighbour(nodefunction)
                                
                            '''
                                add this variable as nodefunction's neighbour
                            '''
                            nodefunction.addNeighbour(nodeVariables[v])
                            '''
                                add the variable as an argument of the function
                            '''             
                            argumentsOfFunction.append(nodeVariables[v])
              
                    '''
                        add the function parameters
                    '''
                    nodefunction.getFunction().setParameters(argumentsOfFunction) 
                                
                                
                    for index in range(0, 9):
                        parameters_list = list()   
                        for v in range(0, 2):
                            '''
                                insert the function parameters: 0 0 ,0 1, 0 2 ...
                            '''
                            if v == 0:
                                parameters_list.insert(v, NodeArgument(arguments[(index * 2)]))
                            else:
                                parameters_list.insert(v, NodeArgument(arguments[(index * 2) + 1]))
                            
                
                        '''
                            if the colorability constraint is not respected
                        '''
                        if(parameters_list[0].equals(parameters_list[1])):
                            cost = -1
                        else:
                            '''
                                if it is respected
                            '''
                            cost = 0
                         
                        '''
                            add to the cost function: [parameters -> cost]
                        '''        
                        nodefunction.getFunction().addParametersCost(parameters_list, cost)
                                
                    '''
                        add the function node
                    '''
                    nodeFunctions.append(nodefunction) 
                                
                    '''
                        add the function node to the agent
                    '''
                    agent.addNodeFunction(nodefunction)
                
                    '''
                        update the id of the next function node
                    '''
                    function_id = function_id + 1                              
    
    '''
        for each variable add a fictitious function
        to break symmetry. A fictitious function is
        an unary function (0, 1, 2) with a domain
        built with very small random numbers
    '''  
    for variable in nodeVariables:
        '''
            creates an unary function linked to the variable
        '''
        nodefunction = NodeFunction(function_id)
            
        functionevaluator = TabularFunction()  
        nodefunction.setFunction(functionevaluator) 
        
        '''
            list of the arguments of the function
        ''' 
        argumentsOfFunction = list()
        
        '''
            Id of the variable associated with the function
        '''
        variable_to_function = variable.getId()
        
        '''
            add the function_id function to the neighbors 
            of variable_to_function
        '''    
        for v in range(len(nodeVariables)):
            if nodeVariables[v].getId() == variable_to_function:
                '''
                    add this nodefunction to the actual nodevariable's neighbour
                '''
                nodeVariables[v].addNeighbour(nodefunction)
                '''
                    add this variable as nodefunction's neighbour
                '''
                nodefunction.addNeighbour(nodeVariables[v])
                '''
                    add the variable as an argument of the function
                '''     
                argumentsOfFunction.append(nodeVariables[v])
        
        parameters_list = list()
        
        '''
            create the fictitious functions
        '''       
        for i in range(0, 3):
                
            parameters_list = list()
                
            parameters_list.append(NodeArgument(i))
            '''
                assigns a small random value to each value of the domain
            '''
            cost = random.random() / (10 ^ 6)
            '''
                add to the cost function: [parameters -> cost]
            ''' 
            nodefunction.getFunction().addParametersCost(parameters_list, cost)  
            
        '''
            add the neighbors of the function node
        '''
        nodefunction.getFunction().setParameters(argumentsOfFunction)
        '''
            add the function node
        '''
        nodeFunctions.append(nodefunction) 
        
        '''
            add the function node to the agent
        '''
        agent.addNodeFunction(nodefunction)
        '''
            update the id of the next function node
        '''        
        function_id = function_id + 1  
    
    '''
        there is only one agent in this Dcop
    '''    
    agents.append(agent)
          
    string = ""         
    
    '''
        create the COP: list of variables, list of functions, agents
    '''                
    cop = COP_Instance(nodeVariables, nodeFunctions, agents)
    
    string = string + "How many agents?" + str(len(agents)) + "\n"
    
    '''
        create the factor graph report
    '''
    for agent in agents:
            string = string + "\nAgent Id: " + str(agent.getId()) + "\n\n"
            string = string + "How many NodeVariables?" + str(len(agent.getVariables())) + "\n"
            for variable in agent.getVariables():
                string = string + "Variable: " + str(variable.toString()) + "\n"
                
            string = string + "\n"
            
            for function in agent.getFunctions():
                string = string + "Function: " + str(function.toString()) + "\n"
                
            string = string + "\n"    
    
    for variable in nodeVariables:
            string = string + "Variable: " + str(variable.getId()) + "\n"
            for neighbour in variable.getNeighbour():
                string = string + "Neighbour: " + str(neighbour.toString()) + "\n"
            string = string + "\n"
    
    for function in nodeFunctions:
            string = string + "\nFunction: " + str(function.getId()) + "\n"
            string = string + "Parameters Number: " + str(function.getFunction().parametersNumber()) + "\n"
            for param in function.getFunction().getParameters():
                string = string + "parameter:" + str(param.toString()) + "\n"
                
            string = string + "\n\tCOST TABLE\n"
            
            string = string + str(function.getFunction().toString()) + "\n" 
    
    string = string + "\t\t\t\t\t\t\tFACTOR GRAPH\n\n" + str(cop.getFactorGraph().toString())
    
    info_graph_file = open(infoGraphPathFile + "FactorGraph/factor_graph_run_" + str(run) + ".txt", "w")
    info_graph_file.write(string)
    info_graph_file.write("\n")
    info_graph_file.close()      
    
    return cop  

'''
    color_list: available colors list that the neighbors can use
    color: color that must be found in the color_list
    returns the color index in the list
'''
def search_Index(color_list, color):
    for i in range(len(color_list)):
        '''
            if you finds the color
        '''
        if(color_list[i] == color):
            '''
                return the index
            '''
            return i
    '''
        you did not find it
    '''
    return -1


def getParser():
    '''
        This is the Parser that takes the parameters of Command Line
    '''
    parser = argparse.ArgumentParser(description="MaxSum-Algorithm")
    
    parser.add_argument("-iterations", metavar='iterations', type=int,
                        help="number of iterations")
    
    parser.add_argument("-instances", metavar='instances', type=int,
                        help="number of instances in Dcop")
    
    parser.add_argument("-variables", metavar='variables', type=int,
                        help="number of variables in Dcop")
    
    parser.add_argument("-op", metavar='op',
                        help="operator (max/min)")
    
    parser.add_argument("-reportMaxSum", metavar='reportMaxSum',
                        help="FILE of reportMaxSum")
    
    parser.add_argument("-reportFactorGraph", metavar='reportFactorGraph',
                        help="FILE of reportFactorGraph")
    
    parser.add_argument("-reportCharts", metavar='reportCharts',
                        help="FILE of reportCharts")
    
    
    args = parser.parse_args()

    '''
        All parameters ARE REQUIRED!!
        if the parameters are correct
    '''
    if  ((args.iterations > 0 & (not(args.iterations == None))) & 
        (args.instances > 0 & (not(args.instances == None))) & 
        (args.variables > 0 & (not(args.variables == None))) & 
        (not(args.op == None) & ((args.op == 'max') | (args.op == 'min'))) & (not(args.reportMaxSum == None)) & 
        (not(args.reportFactorGraph == None)) & (not(args.reportCharts == None))):
        
        return args
    else:
        printUsage()
        sys.exit(2)
        
        

def printUsage():
    
    description = '\n----------------------------------- MAX SUM ALGORITHM ---------------------------------------\n\n'
    
    description = description + 'This program is a testing about Colored Graphs, 3-colorability.\nThe colored Graphs'
    description = description + ' have 10 and many more variables.\nThe aim is to analyze the average of the rmessages'
    description = description + 'differences which tends to 0,\nand that the number of conflicts tends to 0.\n'
    description = description + 'The results are: report about the average of the rmessages differences,\n' 
    description = description + 'factor graph of Dcop, the charts about the average of the rmessages differences\n'
    description = description + 'and the conflicts during the iterations.\n'
    description = description + 'The results are saved as chart (.png) and as log file (.txt)\n'
    
    usage = 'All parameters ARE REQUIRED!!\n\n'
    
    usage = usage + 'Usage: python -iterations=Iter -instances=Inst -variables=V -op=O -reportMaxSum=reportM -reportFactorGraph=reportG -reportCharts=reportC [-h]\n\n'
    
    usage = usage + '-iterations Iter\tThe number of MaxSum iterations\n'
    usage = usage + '-instances Inst\t\tThe number of instances of Dcop to create\n'
    usage = usage + '-variables V\t\tThe number of variables in each instance\n'
    usage = usage + '-op O\t\t\tmax/min (maximization or minimization of conflicts)\n'
    usage = usage + '-reportMaxSum reportM\t\tFILE where writing the report of the MaxSum execution (FILE location with final /)\n'
    usage = usage + '-reportFactorGraph reportG\tFILE where writing the factorGraph and information about MaxSum execution (FILE location with final /)\n'
    usage = usage + '-reportCharts reportC\t\tFILE where saving the average of the rmessagesdifferences and the number of conflicts of the MaxSum execution\n\t\t\t\t(FILE location with final /)\n'
    usage = usage + '-h help\tInformation about parameters\n'
    
    print(description)
    
    print(usage)
    

    
if __name__ == '__main__':
    main()
