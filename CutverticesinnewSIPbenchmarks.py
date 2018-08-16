import os
import copy
import sys
import math
import GraphUtil
import GraphStats

sys.setrecursionlimit(8000)

task_to_do = "countingCutVertices.txt"
result = open(task_to_do,"w")
root_dir = "newSIPbenchmarks"
stats_on_cut_vertices = []
for directory in os.listdir(root_dir):
    p = root_dir + "/" + directory
    for subdir, dirs, files in os.walk(p):
        for file in files:
            if not file == ".DS_Store" and not file ==".gitignore":
                total_path = subdir + "/" + file
                print total_path
                # current file
                result.write(total_path +"\n")

                # setup graph for analysis of cut vertices
                adjacency_matrix = GraphUtil.create_graph(total_path)
                adjacency_list = GraphUtil.create_adjacency_list(adjacency_matrix)
                length = len(adjacency_matrix)
                disc = [0]*length
                low = [length*length]*length
                visited = [0]*length
                parent = [None]*length
                AP = [0]*length
                
                for i in range(len(visited)):
                    if visited[i]==0:
                        GraphStats.find_all_cut_vertices(adjacency_list,disc, low,visited,parent,AP,i,0)
                cut_vertex_num = sum(AP)
                result.write("number of cut vertices: " +str(cut_vertex_num)+ "\n")

                # summary statistics
                while len(stats_on_cut_vertices)<=cut_vertex_num:
                    stats_on_cut_vertices+=[0]
                stats_on_cut_vertices[cut_vertex_num]+=1

                    
    path = root_dir
result.write("\n")
for i in range(len(stats_on_cut_vertices)):
    if stats_on_cut_vertices[i] >= 1:
        result.write("number of graphs with" +str(i)+" cut vertices: "+str(stats_on_cut_vertices[i])+"\n")
    
result.close()
