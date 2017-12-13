## MaxSum Algorithm in Python##

----------


## Introduction ##

The **Max-Sum algorithm** is a GDL (_Generalized Distributive Law_) algorithm that operates on a factor graph that is a bipartite graph in which the nodes represent variables and constraints. Each node representing a variable of the original DCOP is connected to all function nodes that represent constraints that it is involved in.

Similarly, a function-node is connected to all variable-nodes that represent variables in the original DCOP that are included in the constraint it represents. Agents in Max-sum perform the roles of different nodes in the factor graph. We will assume a single one agent takes the role of the variable-nodes that represent its own variables and for each function-node, the same agent whose variable is involved in the constraint it represents, performs its role. 

Variable-nodes and function-nodes are controlled by one “agent" in Max-sum, i.e., they can send messages, read messages and perform computation.

----------------
## Design ##

This code is a testing about Colored Graphs, 3-colorability. The graphs are generated randomly and they are colourable.
The Graphs colored can have 10 and many more variables. Each variable has three values in its domain: 0, 1, 2 and each function is binary. For breaking the simmetry caused by coloration, a fictitious function has been added to each variable variable. A fictitious function is an unary function (0, 1, 2) with a domain built with very small random numbers. This function always sends the same messsages to variables. 

----------
## Goal ##

The aim is to analyze _the average of the rmessages differences_ which tends to 0, and that _the number of conflicts_ tends to 0. 

**The average of the rmessages differences** is the average of the rmessages difference after n iterations for each link in Dcop in the instance.

**The number of conflicts** are the values calculated by MaxSum  during the iterations.

When the number of conflicts and the average of the rmessages differences tends to 0, MaxSum algorithm should converge and it should terminate.

The results are: report about the average of the rmessages differences,  factor graph of Dcop, the charts about the average of the rmessages differences and the conflicts during the iterations. The results are saved as chart (.png) and as log file (.txt).

----------

## OUTPUT FILE LIST ##
Each Dcop instance has these FILE:

 - **TestingColoring_Report.txt**:  FILE about the average of the rmessages differences. 
 - **factor_graph.txt**:  FILE about the Factor Graph, cost tables and other information about Dcop
 - **ChartMediaDiffLink.png**:  Chart with the trend of the average of the differences in the rmessages during the iterations 
 - **ConflictsChart.png**:  Chart with the trend of the MaxSum values during the iterations 

----------

## Examples ##

An example about **ChartMediaDiffLink.png**
![enter image description here](https://lh3.googleusercontent.com/Lyt3Y_I10kLt-4vzOaNXACTJJfzDOLbmSeYlIqaJFEN6qfQq4fUygKAyFY1HQw7cQrfWvtDsvmMe=s800 "ChartMediaDiffLink_RUN_0.png")

An example about **ConflictsChart.png**

![enter image description here](https://lh3.googleusercontent.com/JyYrQXxgLmEHyQACzC1IoMKp5tz0bdz1p1yDZDF6Qg7VQLxHq5t5I_h0Fx9UFxf_q9ZgSQp1Lo7s=s800 "ConflictsChart_RUN_0.png")


----------

## Usage ##

All parameters **are required**. The Test file (Main) is located in _Max_Sum_Python/Testing/Colored_Graph_Coloring.py_
```
python Colored_Graph_Testing -iterations=Iter   -instances=Inst -variables=V -op=O  -reportMaxSum=reportM -reportFactorGraph=reportG -reportCharts=reportC [-h]
```

 - **iterations**: number of iterations
 - **instances**: number of Dcop instances for the testing
 -  **variables**: number of variables in each instance
 -  **op**: max/min (maximization or minimization operator) 
 -  **reportMaxSum**: path ( with final '/')  where saving the average of the rmessages differences
 -  **reportFactorGraph**: path (with final '/') where saving the Factor Graph and information about the cost tables 
 -  **reportCharts**: path (with final '/') where saving the Charts about the average of the rmessages differences and  the MaxSum values during the iterations 
 - **h** [optional]: help, information about parameters

