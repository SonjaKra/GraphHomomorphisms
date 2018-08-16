# Author: Sonja Kraiczy
# description:
import copy
import random

#creates an adjacency matrix from a benchmark data style file
def create_graph(filename):
    file = open(filename, "r")
    vertex_num = int(file.readline()[:-1])
    adjacency_matrix = [[0]*vertex_num for i in range(vertex_num)]
    adjacency_list = []
    current_vertex = 0
    for line in file:
        line = line.split(" ")[:-1]
        adjacency_list.append([0])
        for i in range(1,len(line)):
            neighbour = int(line[i])
            if neighbour==current_vertex:
                adjacency_list[current_vertex][0]=1
            adjacency_list[current_vertex].append(neighbour)
            adjacency_matrix[current_vertex][neighbour] = 1
            adjacency_matrix[neighbour][current_vertex] = 1

        degree = 0
        if adjacency_list[current_vertex][0]==1:
            degree=1
        neighbours = set(adjacency_list[current_vertex][1:])
        adjacency_list[current_vertex]=[degree+len(neighbours)]+list(neighbours)
        current_vertex+=1
    return adjacency_matrix,adjacency_list

# creates the adjacency matrix given an adjacencylist
# of the form [[degree of vertex1,neighbour_1,..neighbour_n],[degree of vertex 2,...]]
def create_adjacency_matrix(adjacency_list):
    am = []
    for i in range(len(adjacency_list)):
        am.append([])
        for j in range(len(adjacency_list)):
            am[i].append(0)
    for i in range(len(adjacency_list)):
        for neighbour in adjacency_list[i][1:]:
            am[i][neighbour]=1
            am[neighbour][i]=1
    return am

# creates and returns the adjacency list given an adjacency matrix
def create_adjacency_list(adjacency_matrix):
    adjacency_list= []        
    for i in range(len(adjacency_matrix)):
        adjacency_list.append([0])
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j]==1:
                if i==j:
                    adjacency_list[i][0]+=2
                else:
                    adjacency_list[i][0]+=1                    
                adjacency_list[i].append(j)
    return adjacency_list

#distance filtering
def create_adjacency_matrix_and_list_2(adjacency_matrix,adjacency_list):
    adjacency_matrix_2 = copy.deepcopy(adjacency_matrix)
    adjacency_list_2 = copy.deepcopy(adjacency_list)
    for i in range(len(adjacency_matrix)):
        for j in range(i+1,len(adjacency_matrix)):
            if adjacency_matrix[i][j]==0:
                for k in range(len(adjacency_matrix)):
                    if adjacency_matrix[i][k] == 1 and adjacency_matrix[k][j]==1:
                        adjacency_matrix_2[i][j] = 1
                        adjacency_matrix_2[j][i] = 1
                        adjacency_list_2[i].append(j)
                        # increase degree
                        adjacency_list_2[i][0] += 1
                        adjacency_list_2[j].append(i)
                        #increase degree
                        adjacency_list_2[j][0] += 1
                        break
    return [adjacency_matrix_2,adjacency_list_2]

#P(2,2),P(3,2),P(4,2)
def build_supplemental_graphs(adjacency_matrix,adjacency_list,paths_num):
    supplemental_matrix = []
    for i in range(len(adjacency_matrix)):
        supplemental_matrix.append([0]*len(adjacency_matrix))

    for vertex in range(len(adjacency_matrix)):
        for neighbour in adjacency_list[vertex][1:]:
            if neighbour!=vertex:
                for neighbour2 in adjacency_list[neighbour][1:]:
                    if neighbour2!=vertex and neighbour2!=neighbour:
                        supplemental_matrix[vertex][neighbour2] += 1
    supplemental_graphs=[]
    for i in range(num):
        supplemental_matrix_i=[]
        supplemental_list_i=[]
        for j in range(len(supplemental_matrix)):
            supplemental_matrix_i.append([])
            supplemental_list_i.append([0])
            for k in range(len(supplemental_matrix)):
                if supplemental_matrix[j][k]>=i+1:
                    supplemental_matrix_i[j].append(1)
                    supplemental_list_i[j][0]+=1
                    supplemental_list_i[j].append(k)
                else:
                    supplemental_matrix_i[j].append(0)
        supplemental_graphs+=[supplemental_matrix_i,supplemental_list_i]
    return supplemental_graphs

# old version, to be deleted
def build_supplemental_graphs2(adjacency_matrix,adjacency_list,paths_num):
    supplemental_matrix = []
    for i in range(len(adjacency_matrix)):
        supplemental_matrix.append([0]*len(adjacency_matrix))
    # TODO: loop through adjacency list instead to make it more efficient
    for i in range(len(adjacency_matrix)):
        for j in range(i+1,len(adjacency_matrix)):
            if i!=j and supplemental_matrix[i][j]<=paths_num:
                for k in range(len(adjacency_matrix)):
                    if adjacency_matrix[i][k] == 1 and adjacency_matrix[k][j]==1:
                        supplemental_matrix[i][j] += 1
                        supplemental_matrix[j][i] += 1
    supplemental_graphs=[]
    for i in range(num):
        supplemental_matrix_i=[]
        supplemental_list_i=[]
        for j in range(len(supplemental_matrix)):
            supplemental_matrix_i.append([])
            supplemental_list_i.append([0])
            for k in range(len(supplemental_matrix)):
                if supplemental_matrix[j][k]>=i+1:
                    supplemental_matrix_i[j].append(1)
                    supplemental_list_i[j][0]+=1
                    supplemental_list_i[j].append(k)
                else:
                    supplemental_matrix_i[j].append(0)
        supplemental_graphs+=[supplemental_matrix_i,supplemental_list_i]
    return supplemental_graphs

def create_ErdosRenyi_graph(n,d):
    am = [[0 for i in xrange(n)] for j in xrange(n)]
    for i in range(n):
        for j in range(i+1,n):
            r = random.random()
            if r<d:
                am[i][j]=1
                am[j][i]=1
    return am
                       
        
#graph = create_ErdosRenyi_graph(4,0.5)
#print graph
