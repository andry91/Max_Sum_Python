## MaxSum Algorithm in Python ##

----------


## Introduction ##

The **Max-Sum algorithm** is a GDL (_Generalized Distributive Law_) algorithm that operates on a factor graph. A factor graph is a bipartite graph in which the nodes represent variables and constraints. Each node representing a variable of the original DCOP is connected to all function nodes that represent constraints that it is involved in.

Similarly, a function-node is connected to all variable-nodes that represent variables in the original DCOP that are included in the constraint it represents. Agents in Max-sum perform the roles of different nodes in the factor graph. We will assume a single one agent takes the role of the variable-nodes that represent its own variables and for each function-node, the same agent whose variable is involved in the constraint it represents, performs its role. 

Variable-nodes and function-nodes are controlled by one “agent" in Max-sum, i.e., they can send messages, read messages and perform computation.

----------------
## Empirical methodology ##

This code was tested on Graph Colouring, a standard benchmarking problem for COPs and DCOPs. In particular, the graphs are generated randomly and they are colourable. The Colored Graphs have a range from 10 to 50 variables. Each variable has a ternary domain (0, 1, 2) and each function is binary. For breaking the simmetry that is presente in the graph colouring problem, we use a fictitious function that is connected to each variable. Such fictitious function is an unary function with a domain built with very small random numbers. This function always sends the same messsages to variables. 

----------
## Metrics ##

The _average of the rmessages differences_ and the _number of conflicts_ tend to 0 when MaxSum finds the optimal solution, in same cases they don't tent to 0 because MaxSum doesn't find the optimal solution. The aim is to analize these charts according to solution found by MaxSum.

**The average of the rmessages differences** is the average of the rmessages difference after n iterations for each link in Dcop in the instance.

**The number of conflicts** is the number of adjacent variables that have the same color calculated by MaxSum.

When the number of conflicts and the average of the rmessages differences tends to 0, MaxSum algorithm should converge and it should terminate.

By default the results for each run are: _factor_graph_run_x.txt_ is a report that provides a textual description of the factor graph and _TestingColoring_Report_RUN_x.txt_ is a report where for each iteration of the run there are the number of conflicts and the rmessages difference (x represents the number of instance). Moreover, after each run the program creates two graphs that plot the average message difference _ChartMediaDiffLink_RUN_x.png_ and the number of conflicts _ConflictsChart_RUN_x.png_ (y axis) against the iterations (x axis). 

----------

## OUTPUT FILE LIST ##
Each Dcop instance creates these FILES as Outuput:

 - **TestingColoring_Report.txt**:  FILE about the average of the rmessages differences. 
 - **factor_graph.txt**:  FILE about the Factor Graph, cost tables and other information about Dcop
 - **ChartMediaDiffLink.png**:  Chart with the trend of the average of the differences in the rmessages during the iterations 
 - **ConflictsChart.png**:  Chart with the trend of the MaxSum values during the iterations 

----------

## Requirements ##
To execute the Colored_Graph_Testing.py is necessary to install **matplotlib module**.
Matplotlib module permits to create the charts.

To install this module follow the instructions:
```
sudo pip install matplotlib
```

## Usage ##

All parameters **are required**. The Test file (Main) is located in _Max_Sum_Python/Testing/Colored_Graph_Coloring.py_
```
python Colored_Graph_Testing.py -iterations=Iter -instances=Inst -variables=V -op=O -reportMaxSum=reportM -reportFactorGraph=reportG -reportCharts=reportC [-h]
```

 - **iterations**: number of iterations
 - **instances**: number of Dcop instances for the testing
 -  **variables**: number of variables in each instance
 -  **op**: max/min (maximization or minimization operator) 
 -  **reportMaxSum**: path ( with final '/')  where saving the average of the rmessages differences
 -  **reportFactorGraph**: path (with final '/') where saving the Factor Graph and information about the cost tables 
 -  **reportCharts**: path (with final '/') where saving the Charts about the average of the rmessages differences and  the MaxSum values during the iterations 
 - **h** [optional]: help, information about parameters

