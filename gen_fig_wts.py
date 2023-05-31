from calc_cur_weights import tor_weights
from calc_alt1_weights import alt1_weights
from calc_alt2_weights import alt2_weights

def compute_weights_and_bw(G,M,E,D,tor=False,alta=False,altb=False,toralt=False):
    '''
    Compute the weights W_{xy} and the bandwidth allocations C_p (how much bandwidth
    from class C is in position p) using Tor's current weighting, the Alt1 weights, and
    the Alt2 weights.

    The tor, alta, and altb parameters indicate which weights (Tor, Alt1, and Alt2) to
    include.  The toralt parameter indicates whether to use our proposed fixes to Tor's
    weights or to allow it to compute possibly invalid weights as currently specified.
    '''

    # Set up the computation of the allocations C_p from a weight dict w whose keys are
    # listed in wxy_list.
    # The allocation of Cp_list[i] will be given by
    # C_list[i] * w[wxy_list[i]]
    C_list = [G,G,E,E,D,D,D]
    wxy_list = ['wgg','wmg','wme','wee','wgd','wmd','wed']
    Cp_list = ['Gg', 'Gm', 'Em', 'Ee', 'Dg', 'Dm', 'De']

    print("  (G,M,E,D) = ({0:d},{1:d},{2:d},{3:d})".format(G,M,E,D))
    
    if tor:
        w0, s0 = tor_weights(G,M,E,D,toralt)
        if toralt:
            print("  Tor's current weights (WITH our fix):")
        else:
            print("  Tor's current weights (WITHOUT our fix):")
        for i in range(7):
            wxy = wxy_list[i]
            print("    wxy: {0:3s}   value: {1:5.3f}\t BW in {2:2s}: {3:10f}".format(wxy, w0[wxy], Cp_list[i], C_list[i]*w0[wxy]))
        print("                           \t BW in Mm: {0:10f}".format(M))

    if alta:
        w1, s1 = alt1_weights(G,M,E,D)
        print("  Alt1 weights:")
        for i in range(7):
            wxy = wxy_list[i]
            print("    wxy: {0:3s}   value: {1:5.3f}\t BW in {2:2s}: {3:10f}".format(wxy, w1[wxy], Cp_list[i], C_list[i]*w1[wxy]))
        print("                           \t BW in Mm: {0:10f}".format(M))

    if altb:
        w2, s2 = alt2_weights(G,M,E,D)
        print("  Alt2 weights:")
        for i in range(7):
            wxy = wxy_list[i]
            print("    wxy: {0:3s}   value: {1:5.3f}\t BW in {2:2s}: {3:10f}".format(wxy, w2[wxy], Cp_list[i], C_list[i]*w2[wxy]))
        print("                           \t BW in Mm: {0:10f}".format(M))



print("Compute weights for Fig. 2")
G = 50
M = 120
E = 40
D = 90
compute_weights_and_bw(G,M,E,D,True,False,False,False)

print("Compute weights for Fig. 3")
G = 1
M = 4
E = 1
D = 1
compute_weights_and_bw(G,M,E,D,True,True,True,True)


print("Compute weights for Fig. 4")
G = 50
M = 120
E = 40
D = 90
compute_weights_and_bw(G,M,E,D,True,True,True,True)

print("Compute weights for Fig. 5")
G = 1
M = 1
E = 1
D = 1
compute_weights_and_bw(G,M,E,D,True,True,True,False)

print("Compute weights for Fig. 6")
G = 48376320
M = 8230344
E = 7022395
D = 21332550
compute_weights_and_bw(G,M,E,D,True,True,True,False)

print("Compute weights for Fig. 7")
G = 800
M = 301
E = 599
D = 200
compute_weights_and_bw(G,M,E,D,True,True,True,False)