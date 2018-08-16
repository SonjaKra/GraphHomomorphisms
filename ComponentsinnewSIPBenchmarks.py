import os
import copy
import sys
import math
import GraphUtil
import GraphStats

sys.setrecursionlimit(8000)

task_to_do = "countingComponents.txt"
result = open(task_to_do,"w")
root_dir = "newSIPbenchmarks"
# at index i the #graphs with i+1 components are stored
stats_on_components = []
for directory in os.listdir(root_dir):
    p = root_dir + "/" + directory
    for subdir, dirs, files in os.walk(p):
        for file in files:
            if not file == ".DS_Store" and not file ==".gitignore":
                total_path = subdir + "/" + file
                print total_path
                result.write(total_path+"\n")
                adjacency_matrix = GraphUtil.create_graph(total_path)
                al = GraphUtil.create_adjacency_list(adjacency_matrix)
                num = GraphStats.number_of_components(al)

                #extend 
                while num>len(stats_on_components):
                    stats_on_components += [0]
                # one more graph with #num components
                stats_on_components[num-1]+=1
                result.write("number of components:  " + str(num)+"\n")
    path = root_dir
result.write("\n")
for i in range(len(stats_on_components)):
    if stats_on_components[i] >= 1:
        result.write("number of graphs with" +str(i+1)+" components: "+str(stats_on_components[i])+"\n")
    
result.close()
