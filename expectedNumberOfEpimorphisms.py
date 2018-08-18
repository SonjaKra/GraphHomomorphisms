# Author: Sonja Kraiczy
# Definition of a Graph epimorphism:
# Let P=(V_p,E_p) and T=(V_t,E_t) be graphs.
# A Graph epimorphism is a surjective function k: V_p->V_t s.t.
#  - for all x,y in V_p, if (x,y) in E_P, also (k(x),k(y)) in E_T (adjacency is preserved)
#  - for all u,v in V_T if (u,v) in E_T, there exist x,y in V_T s.t. k(x)=u,k(y)=v and (x,y) in E_P (we have edge surjection)
#
# Now suppose P and T are Erdos-Renyi random graphs with edge probabilities d_p and d_t respectively.
# Furthermore P and T are loopless, and the vertices in each are distinguishable.
# We want to calculate the expected number of epimorphisms given that all vertex surjections are equally likely.


# recursive function that calculates the expected number of epimorphisms
# generates all possible ways of assigning a nonzero number of vertices
# to each target vertex where the target vertices are distinguishable i.e. [3,1,1] is considered different from [1,3,1]
# in the base case p=0 (i.e. no vertices are left to distribute) we multiply by the number of ways of achieving
# this distribution assuming the pattern vertices are distinguishable (multinomial coefficient)
# multiplied by the probability that it satisfy the remaining properties of a graph epimorphism
from decimal import *
from scipy.special import gamma, factorial
import math

def expected_number_of_epimorphisms(v_p,v_t,d_p,d_t):
    t = [1]*v_t
    t[0]+=v_p-v_t
    expectation = Decimal(0)
    while t!=[]:
        # number of ways of assigning v_p distinguishable vertices to v_t indistinguishable vertices according to the partition t
        poss = multinomial_coeff(t)
        poss *= prob_of_A_and_B(t,d_p,d_t)
        poss *= prob_no_edge_to_vertex(t,d_t,d_p)
        # count distinct values: t=[3,1,1] results in temp = [2,0,1] (2 times 1, 0 times 2, 1 times 3)
        temp = [0]*(v_p-v_t+1)
        for e in t:
            temp[e-1]+=1
        # multiply by distinct permutations of t
        poss *= multinomial_coeff(temp)
        expectation += poss
        t = nextPartition(t)
    return expectation

# computes probability that the given surjection (as represented by the list t, assume distinguishable vertices have been chosen)
# preserves both is edge surjective (A) and preserves adjacency (B)
def prob_of_A_and_B(t,d_t,d_p):
    prob = Decimal(1)
    # product over all pairs of target vertices
    for i in xrange(len(t)):
        for j in xrange(i+1,len(t)):
            prob *= Decimal(d_t+(1-2*d_t)*(1-d_p)**(t[i]*t[j])) # simplfied formula
    return prob

# computes multinomial coefficient: (n,(partition[0],...,partition[-1]))
def multinomial_coefficient(n,partition):
    result = Decimal(gamma(n+1))
    for x_i in partition:
        if x_i>1:
            result /= Decimal(gamma(x_i+1))
    return result

def multinomial_coeff(partition):
    result = Decimal(1)
    i = Decimal(1)
    for x in partition:
        for j in xrange(1,x+1):
            result *= Decimal(i)
            result /= Decimal(j)
            i += Decimal(1)
    return result
        
# returns the probability that given a fixed vertex surjection k:V_p->V_t
# for every v in V_t, for every x,y in k**(-1)(v) (preimage of v under k)
# and x!=y, (x,y) not in E_p
def prob_no_edge_to_vertex(t,d_t,d_p):
    prob = Decimal(1)
    for i in xrange(len(t)):
        prob *= Decimal((1-d_p)**((t[i]*(t[i]-1))/2))
    return prob

# returns the factorial of n (assume n > 1)
def factorial(n):
    return Decimal(gamma(n+1))
    product = Decimal(1)
    for i in xrange(2,n+1):
        product *= Decimal(i)
    return product

# returns the next partition into len(t) sets in lexicographical order
def nextPartition(t):
    for i in xrange(1,len(t)):
        if t[0]>t[i]+1:
            t[0]-=1
            t[i]+=1
            for k in xrange(1,i):
                diff = t[k]-t[i]
                t[k]=t[i]
                t[0]+=diff
            return t
    return []

# returns n choose k, assume n>=k
def binomial(n,k):
    if k ==0:
        return 1
    res = Decimal(gamma(n+1))
    res /= Decimal(gamma(k+1))
    res /= Decimal(gamma(n-k+1))
    return res

# returns the number of possible surjections V_p -> V_t   
def number_of_surjections(v_p,v_t):
    sign = 1
    Sum = Decimal(0)
    for i in xrange(v_t+1):
        Sum+= Decimal(sign) * Decimal((v_t-i)**v_p) * binomial(v_t,i)
        sign *= -1
    return Sum

def main():
    # |V_T| - number of target vertices
    v_t = 4
    # |V_P| - number of pattern vertices
    v_p = 14
    # preimages of target vertices should be non-empty
    t = [1]*v_t
    # edge probability in the targer graph
    d_t = 0
    # edge probability in the target graph
    filename = "15_6_0to1and0to1.txt"
    f = open(filename,"w")
    while d_t<=1:
        d_p = 0
        while (d_p <= 1):
            #print d_p
            res = expected_number_of_epimorphisms(v_p,v_t,d_p,d_t)
 #           res /= number_of_surjections(v_p,v_t)
            #print res
            f.write(str(d_t)+" "+str(d_p)+" "+str(res)+"\n")
            d_p+=0.01
        f.write("\n")
        d_t+=0.01
    f.close()

def matrix():
    Vt = 5
    Vp = 10
    f = "10P5Texpectation.txt"
    f = open(f,"w")
    dt = 0
    while dt <= 1:
        dp=0
        while dp <= 1:
            res = expected_number_of_epimorphisms(Vp,Vt,dp,dt)
            f.write(str(math.modf(res)[1])+" ")
            dp+=0.1
        f.write("\n")
        dt+=0.1
    f.close()

            

matrix()
    
#v_p = 8
#v_t = 3
#print number_of_surjections(v_p,v_t)
#t = [6,1,1]
#count = Decimal(0)
#while (t!=[]):
#    print t
#    temp = [0]*t[0]
#    for e in t:
#        temp[e-1]+=1
#    mc = Decimal(gamma(v_t+1))
#    for el in temp:
#        if el>1:
#            mc/=Decimal(gamma(el+1))
#    count+=multinomial_coefficient(v_p,t)*mc
    
#    t = nextPartition(t)
#print count
    
