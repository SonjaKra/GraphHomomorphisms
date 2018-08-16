# graph is an adjacency list represenation of the graph
# visited[i]=1 if the ith vertex has been visited else visited[i]=0
# vertex is the vertex currently under consideration
# time+1 is the time this vertex is first visited
# cut_vertices[i]=1 is the ith vertex is found to be a cut vertex else cut_vertices[i]=0
def find_all_cut_vertices(graph, disc, low, visited, parent, cut_vertices, vertex, time):
    visited[vertex] = 1
    disc[vertex] = time+1
    low[vertex] = time+1
    child = 0
    for neighbour in graph[vertex][1:]:
        if visited[neighbour] == 0:
            child = child + 1
            parent[neighbour] = vertex
            find_all_cut_vertices(graph, disc, low, visited, parent, cut_vertices, neighbour, time+1)
            low[vertex] = min(low[vertex], low[neighbour])
            if parent[vertex] == None and child > 1:
                cut_vertices[vertex] = 1
            elif parent[vertex] != None and low[neighbour] >= disc[vertex]:
                cut_vertices[vertex] = 1
        elif parent[vertex] != neighbour:
            low[vertex] = min(low[vertex], disc[neighbour])

def number_of_components(graph):
    visited = [False]*len(graph)
    component_num = 0
    for i in range(len(visited)):
        if not visited[i]:
            visit_component(i,graph,visited)
            component_num+=1
    return component_num

#recursive function that visits the connected component vertex is in
def visit_component(vertex,graph,visited):
    visited[vertex] = True
    for neighbour in graph[vertex][1:]:
        if not visited[neighbour]:
            visit_component(neighbour,graph, visited)

def find_all_cut_edges(graph, disc, low, visited, parent, count, vertex, time):
    visited[vertex] = 1
    disc[vertex] = time+1
    low[vertex] = time+1
    for neighbour in graph[vertex][1:]:
        if visited[neighbour] == 0:
            parent[neighbour] = vertex
            find_all_cut_edges(graph, disc, low, visited, parent, count, neighbour, time+1)
            low[vertex] = min(low[vertex], low[neighbour])
            if low[neighbour] > disc[vertex]:
                count+=1
                print "true"
        elif parent[vertex] != neighbour:
            low[vertex] = min(low[vertex], disc[neighbour])
