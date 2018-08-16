import os
import copy
import sys
import math
import GraphUtil
import GraphStats
sys.setrecursionlimit(8000)

task_to_do = "countingCutEdges.txt"
result = open(task_to_do,"w")
root_dir = "newSIPbenchmarks"
stats_on_cut_edges = []
for directory in os.listdir(root_dir):
    p = root_dir + "/" + directory
    for subdir, dirs, files in os.walk(p):
        for file in files:
            if not file == ".DS_Store" and not file ==".gitignore":
                total_path = subdir + "/" + file
                print total_path
                result.write(total_path +"\n")
                adjacency_matrix = GraphUtil.create_graph(total_path)
                adjacency_list = GraphUtil.create_adjacency_list(adjacency_matrix)
                length = len(adjacency_matrix)
                disc = [0]*length
                low = [length*length]*length
                visited = [0]*length
                parent = [None]*length
                cut_edge_count = 0
                
                for i in range(len(visited)):
                    if visited[i]==0:
                        GraphStats.find_all_cut_edges(adjacency_list,disc, low,visited,parent,cut_edge_count,i,0)
                result.write("number of cut edges: " +str(cut_edge_count)+ "\n")

                while len(stats_on_cut_edges)<=cut_edge_count:
                    stats_on_cut_edges+=[0]
                stats_on_cut_edges[cut_edge_count]+=1
    path = root_dir
    result.write("\n")
for i in range(len(stats_on_cut_edges)):
    if stats_on_cut_edges[i] >= 1:
        result.write("number of graphs with" +str(i)+" cut edges: "+str(stats_on_cut_edges[i])+"\n")
    
result.close()
