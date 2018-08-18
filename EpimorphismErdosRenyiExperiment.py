import GraphUtil
import Graphepimorphism
import GraphEpimorphismWithDistanceFiltering

V_t = 5
V_p = 10
dt = 0
times = 1
#f = "10P5TsatisfiableEpiproportion.txt"
#f = open(f,"w")
while dt<=1:
    dp = 0
    while dp <=1:
        count = 0.0
        for i in xrange(times):
            target_am = GraphUtil.create_ErdosRenyi_graph(V_t,dt)
            pattern_am = GraphUtil.create_ErdosRenyi_graph(V_p,dp)
            print pattern_am
            print
            print target_am
            if Graphepimorphism.graph_epimorphism(pattern_am,target_am):
                print "true"
            else:
                print "false"
            if GraphEpimorphismWithDistanceFiltering.graph_epimorphism(pattern_am,target_am):
                print "true"
            else:
                print "false"
            print
 #               count+=1
#        f.write(str(count/times)+" ")
        dp+=0.1
#    f.write("\n")
    dt+=0.1
#f.close()
            
            
