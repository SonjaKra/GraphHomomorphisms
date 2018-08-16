import os
import GraphUtil
import AllDifferent
import time
#version of the subgraph isomorphism with all different filtering commented

def create_and_filter_domains(p_adjacency_matrix,p_adjacency_list,t_adjacency_matrix, t_adjacency_list):
    p_neighbourdgs = []
    t_neighbourdgs = []
    # create the neighbour degree sequence for every vertex in pattern and target graph fur use in domain filtering
    for vertex in range(len(p_adjacency_matrix)):
        pattern_degree_sequence = [p_adjacency_list[neighbour][0] for neighbour in p_adjacency_list[vertex][1:]]
        pattern_degree_sequence.sort(reverse=True)
        p_neighbourdgs.append(pattern_degree_sequence)        
    for vertex in range(len(t_adjacency_matrix)):
        target_degree_sequence = [t_adjacency_list[neighbour][0] for neighbour in t_adjacency_list[vertex][1:]]
        target_degree_sequence.sort(reverse=True)
        t_neighbourdgs.append(target_degree_sequence)

    domains = {}
    for i in range(len(p_adjacency_matrix)):
        # domain consists of vertices with at least the degree of the variable
        # where loops are mapped to loops
        # and neighbour degree sequences have to be compatible
        domains[i] = [j for j in range(len(t_adjacency_matrix)) if t_adjacency_list[j][0]>=p_adjacency_list[i][0]
                      and not (p_adjacency_matrix[i][i] and not t_adjacency_matrix[j][j])
                      and neighbour_degree_sequence_fits(p_neighbourdgs[i],t_neighbourdgs[j])]
    return domains

def neighbour_degree_sequence_fits(pattern_degree_sequence,target_degree_sequence):
    pattern_index = 0
    while pattern_index < len(pattern_degree_sequence):
        if pattern_degree_sequence[pattern_index] <= target_degree_sequence[pattern_index]:
            pattern_index+=1
        else:
            return False
    return True


def neighbour_degree_sequence_fits2(pattern_vertex, target_vertex, pattern_adjacency_list, target_adjacency_list):
    #TODO: change away from python default sort
    pattern_degree_sequence = [pattern_adjacency_list[neighbour][0] for neighbour in pattern_adjacency_list[pattern_vertex][1:]]
    target_degree_sequence = [target_adjacency_list[neighbour][0] for neighbour in target_adjacency_list[target_vertex][1:]]
    pattern_degree_sequence.sort(reverse=True)
    target_degree_sequence.sort(reverse=True)
    pattern_index = 0
    while pattern_index < len(pattern_degree_sequence):
        if pattern_degree_sequence[pattern_index] <= target_degree_sequence[pattern_index]:
            pattern_index+=1
        else:
            return False
    return True

# comment
def smallest_domain(domains,p_graph_degrees):
    items = domains.items()
    d_r,value_r = items[0]
    for d,value in domains.iteritems():
        if len(value) < len(value_r) or (len(value)==len(value_r) and p_graph_degrees[d][0]>p_graph_degrees[d_r][0]):
            value_r = value
            d_r = d
    return d_r,value_r

# if there exists a subgraph isomorphism from P to T, returns true, else false
def sg_isomorphic(domains, p_adjacency_matrix,p_adjacency_list,t_adjacency_matrix, t_adjacency_list):
    if not domains:
        # all vertices have been mapped
        return True
    d,value = smallest_domain(domains,p_adjacency_list)
    value.sort(key= lambda vertex:t_adjacency_list[vertex][0], reverse=True)
    for v in value:
        # if d and vertex i adjacent in pattern graph then v and map(i) adjacent in targetGraph
        # since d->v, d is excluded from domaind_copy and no other domain contains v to satisfy injectivity
        domains_copy = {i:[u for u in domains[i] if u!=v and (not p_adjacency_matrix[d][i] or t_adjacency_matrix[v][u]) ] for i in domains.keys() if i!=d}
        # check for dead end
        if [] not in domains_copy.values():
            if AllDifferent.counting_all_different(domains_copy) and sg_isomorphic(domains_copy, p_adjacency_matrix,p_adjacency_list,t_adjacency_matrix, t_adjacency_list):
                return True              
    return False
        
p_adjacency_matrix=[]
root_dir = "newSIPBenchmarks/scalefree"            
for directory in os.listdir(root_dir):
    if directory != ".DS_Store" and directory != ".gitignore" and directory != "F.08":
        p = root_dir + "/" + directory
        print p
        time1=time.time()
        p_adjacency_matrix,p_adjacency_list = GraphUtil.create_graph(p+"/"+"pattern")
        t_adjacency_matrix,t_adjacency_list = GraphUtil.create_graph(p+"/"+"target")
        time2=time.time()
        print time2-time1
        domains = create_and_filter_domains(p_adjacency_matrix,p_adjacency_list,t_adjacency_matrix,t_adjacency_list)
        time3=time.time()
        print time3-time2
        alldiff = AllDifferent.counting_all_different(domains)
        if alldiff:
            print sg_isomorphic(domains, p_adjacency_matrix,p_adjacency_list,t_adjacency_matrix,t_adjacency_list)
        else:
            print "False, at the beginning"
        endtime = time.time()
        print endtime-time3
