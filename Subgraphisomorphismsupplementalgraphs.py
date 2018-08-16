import os
import GraphUtil
import time
# version of subgraph isoorphism with supplemental graphs commented        
def create_and_filter_domains(pattern,target):
    domains = {}
    for i in range(len(pattern[0])):
        domains[i] = [j for j in range(len(target[0])) if all([target[2*k+1][j][0]>=pattern[2*k+1][i][0] for k in range(len(pattern)/2)])
                      # domain consists of vertices s.t. they have degree at least of the variable in every pattern-target graph pair
                      and not (pattern[0][i][i] and not target[0][j][j]) # loops mapped to loops
                      and all([neighbour_degree_sequence_fits(i,j,pattern[2*k+1],target[2*k+1]) for k in range(len(pattern)/2)])]
                      # neighbour degree sequences have to be compatible in all graph pairs

    return domains

def neighbour_degree_sequence_fits(pattern_vertex, target_vertex, pattern_adjacency_list, target_adjacency_list):
    #TODO: change away from python default sort
    pattern_degree_sequence = [pattern_adjacency_list[neighbour][0] for neighbour in pattern_adjacency_list[pattern_vertex][1:]]
    target_degree_sequence = [target_adjacency_list[neighbour][0] for neighbour in target_adjacency_list[target_vertex][1:]]
    pattern_degree_sequence.sort(reverse=True)
    target_degree_sequence.sort(reverse=True)
    pattern_index = 0
    while (pattern_index < len(pattern_degree_sequence)):
        if pattern_degree_sequence[pattern_index] <= target_degree_sequence[pattern_index]:
            pattern_index+=1
        else:
            return False
    return True

# comment
def smallest_domain(domains,little_graph_degrees):
    items = domains.items()
    d_r,value_r = items[0]
    for d,value in domains.iteritems():
        if len(value) < len(value_r) or (len(value)==len(value_r) and little_graph_degrees[d][0]>little_graph_degrees[d_r][0]):
            value_r = value
            d_r = d
    return d_r,value_r

def sg_isomorphic(domains, pattern, target):
    print "recursing"
    if not domains:
        return True
    d,value = smallest_domain(domains,pattern[1])
    degrees = [target[1][vertex][0] for vertex in value]
    # do own sort
    temp = zip(degrees,value)
    temp.sort(reverse=True)
    value = [j for i,j in temp]
    for v in value:
        # if d and vertex i adjacent in littleGraph then v and map(i) adjacent in bigGraph
        domains_copy = {i:[u for u in domains[i] if u!=v and all([(not pattern[2*k][d][i] or target[2*k][v][u]) for k in range(len(pattern)/2)])] for i in domains.keys() if i!=d}
        if domains_copy==domains:
            print "shit"
        # check for dead end
        if not([] in domains_copy.values()):
            #change
            solution = sg_isomorphic(domains_copy, pattern,target)
            if solution:
                  return True              
    return False

p_adjacency_matrix=[]
root_dir = "newSIPBenchmarks/scalefree"            
for directory in os.listdir(root_dir):
    if directory != ".DS_Store" and directory != ".gitignore" and directory != "F.08" and directory!="F.13":
        p = root_dir + "/" + directory
        print p
        time1 = time.time()
        p_adjacency_matrix = GraphUtil.create_graph(p+"/"+"pattern")
        p_adjacency_list = GraphUtil.create_adjacency_list(p_adjacency_matrix)
        t_adjacency_matrix = GraphUtil.create_graph(p+"/"+"target")
        t_adjacency_list = GraphUtil.create_adjacency_list(t_adjacency_matrix)
        pattern = [p_adjacency_matrix,p_adjacency_list] + GraphUtil.build_supplemental_graphs(p_adjacency_matrix,p_adjacency_list,2)
        target = [t_adjacency_matrix,t_adjacency_list] + GraphUtil.build_supplemental_graphs(t_adjacency_matrix,t_adjacency_list,2)
        time2 = time.time()
        print time2-time1
        domains = create_and_filter_domains(pattern,target)
        time3=time.time()
        print time3-time2
        print sg_isomorphic(domains, pattern,target)
        time4=time.time()
        print time4-time3
