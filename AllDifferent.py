import time
def maximal_matching():
    sink = len(graph)-1
    augmenting_path=[None]*len(graph)
    find_augmenting_path(graph,sink,augmenting_path)
    while augmenting_path[-1]!=None:
        vertex = sink
        parent = augmenting_path[sink]
        while parent != None:
            graph[parent][vertex]=0
            graph[vertex][parent]=1
            vertex=parent
            parent = augmenting_path[parent]

def counting_all_different(domains):
    variables = domains.items()
    variables.sort(key = lambda variable: len(variable[1]))
    union_of_domains = set()
    hall_set = set()
    n = 0
    for i in range(len(variables)):
        n+=1
        stripped_domain = set(variables[i][1]).difference(hall_set)
        union_of_domains = union_of_domains.union(stripped_domain)
        if len(union_of_domains)==n:
            hall_set = hall_set.union(union_of_domains)
            union_of_domains = set()
            n=0
        elif len(union_of_domains)<n:
            return False
        domains[variables[i][0]]=sorted(list(stripped_domain))
    return True

domains = {0:[1],1:[2,3],2:[2,3],3:[2,4,5],4:[4,5,6],5:[4,5,6],6:[2,7,9],7:[3,7,8],8:[2,3,5,8,9]}
print domains
print counting_all_different(domains)
print domains
