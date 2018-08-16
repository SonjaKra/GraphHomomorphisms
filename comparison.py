# expected number of subgraph isomorphisms
from scipy.special import gamma, factorial
from decimal import *

def expectedNumOfSisos(v_t,v_p,d_p,d_t):
    t_p = injections(v_t,v_p)
    power = (v_p*(v_p-1))/2
    if power!=0:
        sol = Decimal(1-(1-d_t)*d_p)**Decimal(power)
    else:
        sol = 1
    sol = t_p*sol
    return sol

def expectedNumOfSisosapprox(v_t,v_p,d_p,d_t):
    t_p = injections(v_t,v_p)
    power = d_p*(v_p*(v_p-1))/2
    if power!=0:
        sol = Decimal(d_t)**Decimal(power)
    else:
        sol = 1
    sol= sol *t_p
    return sol

def injections(v_t,v_p):
    factor = v_t
    result = Decimal(1)
    while factor >= v_t-v_p+1:
        result *= Decimal(factor)
        factor -= 1
    return result

def expectedNumOfIndSisos(v_t,v_p,d_p,d_t):
    t_p = injections(v_t,v_p)
    power = (v_p*(v_p-1))/2
    if power != 0:
        sol = Decimal((1-(1-d_t)*d_p-(1-d_p)*d_t))**(Decimal(power))
    else:
        sol = 1
    sol = t_p*sol
    return sol

def expectedNumOfIndSisosapprox(v_t,v_p,d_p,d_t):
    sol = expectedNumOfSisosapprox(v_t,v_p,d_p,d_t)
    power = (1-d_p)*(v_p*(v_p-1))/2
    if power!=0:
        sol = sol * Decimal(1-d_t)**(Decimal(power))
    return sol

v_p = 30
#f1 = open("exp_siso_exact_abs_30_150.txt","w")
v_t = 150
f2 = open("exp_siso_approx_abs_30_150_1.txt","w")
#f3 = open("exp_siso_diff_abs1.txt","w")
#f4 = open("exp_ind_siso_exact_rel_30_150surface.txt","w")
#f5 = open("exp_ind_siso_approx_abs1.txt","w")
#f6 = open("exp_ind_siso_diff_abs1.txt","w")
d_t = 0
while (d_t<=1):
    d_p = 0
    while (d_p<=1):
#        siso = expectedNumOfSisos(v_t,v_p,d_p,d_t)
        siso_approx = expectedNumOfSisosapprox(v_t,v_p,d_p,d_t)
        #print "exact: "+ str(siso)
        #print "approx: " + str(siso_approx)
       # print "d_t "+str(d_t)+" ; d_p " + str(d_p)
#        siso_ind = expectedNumOfIndSisos(v_t,v_p,d_p,d_t)
#        siso_ind_approx = expectedNumOfIndSisosapprox(v_t,v_p,d_p,d_t)
#        t_p = injections(v_t,v_p)
#        f1.write(str(d_t)+" "+str(d_p)+" "+str(siso)+"\n")
#        f1.write(str(siso/t_p)+" ")
#        f2.write(str(d_t)+" "+str(d_p)+" "+str(siso_approx)+"\n")
        f2.write(str(siso_approx)+" ")
#        f3.write(str(d_t)+" "+str(d_p)+" "+str((siso-siso_approx))+"\n")
#        f4.write(str(d_t)+" "+str(d_p)+" "+str(siso_ind)+"\n")
#        f4.write(str(siso_ind)+" ")
#        f5.write(str(d_t)+" "+str(d_p)+" "+str(siso_ind_approx)+"\n")
#        f6.write(str(d_t)+" "+str(d_p)+" "+str((siso_ind-siso_ind_approx))+"\n")
        d_p+=0.01
#    f1.write("\n")
    f2.write("\n")
#    f3.write("\n")
#    f4.write("\n")
#    f5.write("\n")
#    f6.write("\n")
#    break
    d_t+=0.01
#f1.close()
f2.close()
#f3.close()
#f4.close()
