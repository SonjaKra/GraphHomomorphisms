import GraphUtil
import copy
#currently assuming looplessness of both graphs
# TODO: add comments/ big description

def graph_epimorphism(pattern_am,target_am):
#    print pattern_am
#    print target_am
    # TODO: consider connected components individually
    #pattern_am and target_am assumed to be loopless
    if len(pattern_am) < len(target_am):
        return False
    if edge_number(pattern_am) < edge_number(target_am):
        return False
    # check for two-colourability
    # chromatic number of target graph has to be at least the chromatic number of the pattern graph
    if not two_colourable(pattern_am) and two_colourable(target_am):
        return False
    #for i in xrange(len(pattern_am)):
#        for j in xrange(i+1,len(pattern_am)):
#            if pattern_am[i][j]==1
    t_edge_domains = create_t_edge_domains(pattern_am,target_am)
    p_vertex_domains = create_p_vertex_domains(pattern_am,target_am)
    mapping = {}
    result = graph_epimorphism_exists(p_vertex_domains,t_edge_domains,pattern_am,target_am,mapping)
#    print mapping
    return result
#________________________________________________________________
# MAIN RECURSIVE BACKTRACKING ALGORITHM

def graph_epimorphism_exists(p_vertex_domains,t_edge_domains,pattern_am,target_am,mapping):
    # all edges in the target graph have been mapped to, i.e. surjectivity has been satisfied
    if not t_edge_domains:
        # all vertices in the pattern graph have all been mapped to target vertices satisfying the adjacency constraint
        if not p_vertex_domains:
            return True
        
        # all target edges are mapped to, but there is still at least one unmapped pattern vertex
        # so we select the one with the smallest domain
#        variable_value_pair = p_vertex_domains.items()[0]
        variable_value_pair = smallest_domain(p_vertex_domains.items())
        variable = variable_value_pair[0] # vertex to map
        domain = variable_value_pair[1] # possible values
        for poss_vertex in domain:
            #save assignement
            mapping[variable] = poss_vertex
#            print "vertex assignement"
#            print str(variable) +" -> " + str(poss_vertex)
#            print
            # propagation: adapt domains
            p_vertex_domains_copy = propagate_adjacency_after_vertex_assignement(p_vertex_domains,variable,poss_vertex,pattern_am,target_am)
            # check for dead end
            if [] not in p_vertex_domains_copy.values():
                solution = graph_epimorphism_exists(p_vertex_domains_copy,t_edge_domains,pattern_am,target_am, mapping)
                if solution:
                    return True
#        print "backtracking vertex assignement"
        return False
            
    # there is still an unmatched target edge
    # so we select one
#    variable_value_pair = t_edge_domains[0]
    variable_value_pair = smallest_domain(t_edge_domains)
    edge_to_map = variable_value_pair[0]
    domain = variable_value_pair[1] # possible edges to map to
    for poss_edge in domain:
        # save assignement
        mapping[poss_edge[0]] = edge_to_map[0]
        mapping[poss_edge[1]] = edge_to_map[1]
#        print "edge assignement"
#        print str(poss_edge[0]) +" -> "+str(edge_to_map[0])
#        print str(poss_edge[1])+ " -> " +str(edge_to_map[1])
#        print
        # map edge_to_map -> possedge (in the order vertices are listed)
        # propagation: adapt domains
        t_edge_domains_copy=propagate_surjectivity_after_edge_assignement(t_edge_domains,edge_to_map,poss_edge,pattern_am,target_am)
        if [] in [variable_value_pair[1] for variable_value_pair in t_edge_domains_copy]:
            continue
        p_vertex_domains_copy = propagate_adjacency_after_edge_assignement(p_vertex_domains,poss_edge,edge_to_map,pattern_am,target_am)
        if [] not in p_vertex_domains_copy.values():
            solution = graph_epimorphism_exists(p_vertex_domains_copy,t_edge_domains_copy,pattern_am,target_am, mapping)
            if solution:
                return True
#    print "backtracking edge assignement"
    return False
#___________________________________________________________
# HELPER FUNCTIONS
# accepts domains as a list of tuples, where the first element of the tuple is the variable and the second element of the tuple is the domain (of possible values)
# TODO: move some of these to graph util or graph stats
def smallest_domain(domains):
    smallest_domain = domains[0]
    for i in xrange(1,len(domains)):
        if len(domains[i][1])< len(smallest_domain[1]):
            smallest_domain = domains[i]
    return smallest_domain

def edge_number(am):
    edge_count = 0
    for i in xrange(len(am)):
        for j in xrange(i,len(am)):
            if am[i][j]==1:
                edge_count+=1
    return edge_count
# bock begin
def two_colourable(graph_am):
    colours = [0]*len(graph_am)
    for vertex in xrange(len(graph_am)):
        #print colours
        if colours[vertex]==0:
            colours[vertex]=1
            if not colour_recursively(graph_am,colours,1,vertex):
                #print colours
                return False
    return True

def colour_recursively(graph_am,colours,colour_used,vertex):
    next_colour = get_next_colour(colour_used)
    for i in xrange(len(graph_am)):
        if graph_am[vertex][i]==1 and vertex!=i:
            if colours[i]==colour_used:
                return False
            if colours[i]==0:
                colours[i]=next_colour
                if not colour_recursively(graph_am,colours,next_colour,i):
                    return False
    return True

def get_next_colour(colour):
    if colour==1:
        return 2
    return 1

#what about loops
#def distance_matrix(am,radius):
#    # create matrix filled with zeros
#    dist_m = [[0 for i in xrange(len(am))] for j in xrange(len(am))]
#    for i in xrange(len(am)):
#        visited = [0]*len(am)
#        visited[i]=1
#        calculate_distances(am,i,i,dist_m,1,radius,visited)
#    return dist_m

#def calculate_distances(am,orig,i,dist_m,curr_dist,radius,visited):
#    for j in xrange(len(am)):
#        if am[i][j]==1:
#            if visited[j]==0 or dist_m[orig][j]>curr_dist:
#                visited[j]=1
#                if dist_m[orig][j]==0 or dist_m[orig][j]>curr_dist:
#                    dist_m[orig][j] = curr_dist
#                    dist_m[j][orig] = curr_dist
#                elif dist_m[orig][j]<curr_dist:
#                    curr_dist = dist_m[orig][j]
#                if curr_dist < radius:
#                    calculate_distances(am,orig,j,dist_m,curr_dist+1,radius,visited)

def distance_matrix(am):
    dist = [[float("Inf") for i in xrange(len(am))] for j in xrange(len(am))]
    for i in xrange(len(am)):
        for j in xrange(i+1,len(am)):
            if am[i][j]==1:
                dist[i][j]=1
                dist[j][i]=1
            
    for k in xrange(len(am)):
        for i in xrange(len(am)):
            for j in xrange(i+1,len(am)):
                if dist[i][j] > dist[i][k]+dist[k][j]:
                    dist[i][j] = dist[i][k] +  dist[k][j]
                    dist[j][i] = dist[i][k] + dist[k][j]
    return dist
                
#block end           
#___________________________________________________________
# PROPAGATION FUNCTIONS

# currently assuming looplessness
def propagate_adjacency_after_vertex_assignement(p_vertex_domains,mapped_vertex,mapped_to_vertex,pattern_am,target_am):
#    print "def propagate_adjacency_after_vertex_assignement(p_vertex_domains,mapped_vertex,mapped_to_vertex,pattern_am,target_am)"
#    print p_vertex_domains
    p_vertex_domains_copy = {}
    for p_vertex in p_vertex_domains.keys():
        if p_vertex!=mapped_vertex:
            domain_copy = []
            for t_vertex in p_vertex_domains[p_vertex]:
                # should take care of loops?
                if pattern_am[mapped_vertex][p_vertex]==0 or target_am[mapped_to_vertex][t_vertex]==1:
                    domain_copy.append(t_vertex)
            p_vertex_domains_copy[p_vertex]=domain_copy
#    print p_vertex_domains_copy
#    print
    return p_vertex_domains_copy
    
def propagate_adjacency_after_edge_assignement(p_vertex_domains,p_edge,t_edge,pattern_am,target_am):
#    print "def propagate_adjacency_after_edge_assignement(p_vertex_domains,p_edge,t_edge,pattern_am,target_am)"
#    print p_vertex_domains
    p_vertex_domains_copy = {}
    for p_vertex in p_vertex_domains.keys():
        if not (p_vertex==p_edge[0] or p_vertex==p_edge[1]):
            domain_copy = []
            for t_vertex in p_vertex_domains[p_vertex]:
                # let u,v = p_edge[0],p_edge[1]
                # let a,b = t_edge[0],t_edge[1]
                # u -> a, v -> b
                # should take care of loops?
                if (pattern_am[p_vertex][p_edge[0]]==0 or target_am[t_vertex][t_edge[0]]==1) and (pattern_am[p_vertex][p_edge[1]]==0 or target_am[t_vertex][t_edge[1]]==1):
                    domain_copy.append(t_vertex)
            p_vertex_domains_copy[p_vertex] = domain_copy
#    print p_vertex_domains_copy
#    print
    return p_vertex_domains_copy
def propagate_surjectivity_after_edge_assignement(t_edge_domains,edge_to_map,poss_edge,pattern_am,target_am):
#    print "def propagate_surjectivity_after_edge_assignement(t_edge_domains,edge_to_map,poss_edge,pattern_am)"
#    print t_edge_domains
    t_edge_domains_copy = []
    for variable in t_edge_domains:
        t_edge = variable[0]
        if t_edge!=edge_to_map:
            if t_edge[0]==edge_to_map[0]:
                domain_copy = []
                for p_edge in variable[1]:
                    if (p_edge!=poss_edge) and not (p_edge[0]==poss_edge[1] and p_edge[1]==poss_edge[0]):
                        if p_edge[1]!=poss_edge[1]:
                            if pattern_am[p_edge[1]][poss_edge[1]]==0 or target_am[t_edge[1]][edge_to_map[1]]==1:
                                if pattern_am[p_edge[0]][poss_edge[0]]==0 or target_am[t_edge[0]][edge_to_map[0]]==1:
                                    domain_copy.append(p_edge)
            elif t_edge[0]==edge_to_map[1]:
                domain_copy = []
                for p_edge in variable[1]:
                    if (p_edge!=poss_edge) and not (p_edge[0]==poss_edge[1] and p_edge[1]==poss_edge[0]):
                        if p_edge[1]!=poss_edge[0]:
                            if pattern_am[p_edge[1]][poss_edge[0]]==0 or target_am[t_edge[1]][edge_to_map[0]]==1:
                                if pattern_am[p_edge[0]][poss_edge[1]]==0 or target_am[t_edge[0]][edge_to_map[1]]==1:
                                    domain_copy.append(p_edge)
            elif t_edge[1]==edge_to_map[1]:
                domain_copy = []
                for p_edge in variable[1]:
                    if (p_edge!=poss_edge) and not (p_edge[0]==poss_edge[1] and p_edge[1]==poss_edge[0]):
                        if p_edge[0]!=poss_edge[0]:
                            if pattern_am[p_edge[0]][poss_edge[0]]==0 or target_am[t_edge[0]][edge_to_map[0]]==1:
                                if pattern_am[p_edge[1]][poss_edge[1]]==0 or target_am[t_edge[1]][edge_to_map[1]]==1:
                                    domain_copy.append(p_edge)
            elif t_edge[1]==edge_to_map[0]:
                domain_copy = []
                for p_edge in variable[1]:
                    if (p_edge!=poss_edge) and not (p_edge[0]==poss_edge[1] and p_edge[1]==poss_edge[0]):
                        if p_edge[0]!=poss_edge[1]:
                            if pattern_am[p_edge[0]][poss_edge[1]]==0 or target_am[t_edge[0]][edge_to_map[1]]==1:
                                if pattern_am[p_edge[1]][poss_edge[0]]==0 or target_am[t_edge[1]][edge_to_map[0]]==1:
                                    domain_copy.append(p_edge)
            else:
                domain_copy = []
                for p_edge in variable[1]:
                    if len(set(poss_edge).union(set(p_edge)))==4:
                        if pattern_am[p_edge[0]][poss_edge[0]]==0 or target_am[t_edge[0]][edge_to_map[0]]==1:
                            if pattern_am[p_edge[0]][poss_edge[1]]==0 or target_am[t_edge[0]][edge_to_map[1]]==1:
                                if pattern_am[p_edge[1]][poss_edge[1]]==0 or target_am[t_edge[1]][edge_to_map[1]]==1:
                                    if pattern_am[p_edge[1]][poss_edge[0]]==0 or target_am[t_edge[1]][edge_to_map[0]]==1:
                                        domain_copy.append(p_edge)
            t_edge_domains_copy.append((t_edge,domain_copy))
#    print t_edge_domains_copy
#    print
    return t_edge_domains_copy

# loops not considered here       
def propagate_surjectivity_after_edge_assignement2(t_edge_domains,edge_to_map,poss_edge,pattern_am,target_am):
    print "def propagate_surjectivity_after_edge_assignement(t_edge_domains,edge_to_map,poss_edge,pattern_am)"
    print t_edge_domains
    t_edge_domains_copy = []
    for variable in t_edge_domains:
        t_edge = variable[0]
        if t_edge!=edge_to_map and not (t_edge[0]==edge_to_map[1] and t_edge[1]==edge_to_map[0]):
            if len(set(edge_to_map).union(set(t_edge)))==4:
                domain_copy = []
                for p_edge in variable[1]:
                    if len(set(poss_edge).union(set(p_edge)))==4:
                        domain_copy.append(p_edge)
                t_edge_domains_copy.append((t_edge,domain_copy))
                # edge_to_map:[u,v], t_edge :[w,z]
                #case u==w
            elif edge_to_map[0]==t_edge[0]:
                domain_copy = []
                for p_edge in variable[1]:
                    if p_edge[0]!=poss_edge[1] and p_edge[1]!=poss_edge[0] and p_edge[1]!=poss_edge[1]:
                        # IMPORTANT: no loops considered currently
                        if p_edge[0]==poss_edge[0] or pattern_am[p_edge[0]][poss_edge[0]]==0:
                            domain_copy.append(p_edge)
                t_edge_domains_copy.append((t_edge,domain_copy))
            elif edge_to_map[0]==t_edge[1]:
                domain_copy = []
                for p_edge in variable[1]:
                    if p_edge[1]!=poss_edge[1] and p_edge[0]!=poss_edge[1] and p_edge[0]!=poss_edge[0]:
                        if poss_edge[0]==p_edge[1] or pattern_am[poss_edge[0]][p_edge[1]]==0:
                            domain_copy.append(p_edge)
                t_edge_domains_copy.append((t_edge,domain_copy))
            elif edge_to_map[1]==t_edge[0]:
                domain_copy = []
                for p_edge in variable[1]:
                    if p_edge[0]!=poss_edge[0] and p_edge[1]!=poss_edge[0] and p_edge[1]!=poss_edge[1]:
                        if poss_edge[1]==p_edge[0] or pattern_am[poss_edge[1]][p_edge[0]]==0:
                            domain_copy.append(p_edge)
                t_edge_domains_copy.append((t_edge,domain_copy))
            elif edge_to_map[1]==t_edge[1]:
                domain_copy = []
                for p_edge in variable[1]:
                    if p_edge[1]!=poss_edge[0] and p_edge[0]!=poss_edge[1] and p_edge[0]!=poss_edge[0]:
                        if poss_edge[1]==p_edge[1] or pattern_am[poss_edge[1]][p_edge[1]]==0:
                            domain_copy.append(p_edge)
                t_edge_domains_copy.append((t_edge,domain_copy))
    print t_edge_domains_copy
    print
    return t_edge_domains_copy

#_______________________________________________________
# SET UP FUNCTIONS

# every pattern vertex gets assigned all target vertices in its domain
def create_p_vertex_domains(pattern_am,target_am):
    p_vertex_domains = {}
    for i in xrange(len(pattern_am)):
        p_vertex_domains[i] = range(len(target_am))
    return p_vertex_domains

#currently every edge int he target graph is assigned all possible (directed) edges in the pattern graph to its domain
def create_t_edge_domains(pattern_am,target_am):
    t_edge_domains = []
    pattern_edges = []
    for i in xrange(len(pattern_am)-1):
        for j in xrange(i+1,len(pattern_am)):
            if pattern_am[i][j]==1:
                pattern_edges.append([i,j])
                pattern_edges.append([j,i])
                
    for i in xrange(len(target_am)-1):
        for j in xrange(i+1,len(target_am)):
            if target_am[i][j]==1:
                t_edge_domains.append(([i,j],copy.deepcopy(pattern_edges)))
    #print t_edge_domains
    return t_edge_domains

#__________________________________________________________
# MAIN
def main():
    p = GraphUtil.create_graph("GraphsToTestEpimorphismOn/P12.txt")
    t = GraphUtil.create_graph("GraphsToTestEpimorphismOn/P4.txt")
        
    pattern_am = p[0]
 #   print pattern_am
    target_am = t[0]
#    pattern_am = GraphUtil.create_ErdosRenyi_graph(5,0.6)
#    target_am = GraphUtil.create_ErdosRenyi_graph(3,0.6)
    print pattern_am
    print target_am
#    print two_colourable(pattern_am)
#    print two_colourable(target_am)
#    p_vertex_domains = create_p_vertexdomains(pattern_am,target_am)
#    t_edge_domains = create_t_
#    print graph_epimorphism_exists(p_vertex_domains,t_edge_domains,pattern_am,target_am)
    print graph_epimorphism(pattern_am,target_am)
    
main()

#am = [[0,1,0,0,0,0,0],[1,0,1,1,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,1,1,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,1],[0,0,0,0,0,1,0]]
#print am
#print distance_matrix(am)
