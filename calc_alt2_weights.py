def alt2_weights(G, M, E, D):
    weights = dict()
    T = G + M + E + D
    weights['wmm'] = 1
    if (M > T/3):
        if (D >= abs(G-E)):
            if (G >= E):
                case_str = "1.a.i"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = 0
                weights['wee'] = 1
                weights['wgd'] = (D-(G-E))/(2*D)
                weights['wmd'] = 0
                weights['wed'] = (D+(G-E))/(2*D)
            else: # G < E
                case_str = "1.a.ii"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = 0
                weights['wee'] = 1
                weights['wgd'] = (D+(E-G))/(2*D)
                weights['wmd'] = 0
                weights['wed'] = (D-(E-G))/(2*D)
        else: # D < abs(G-E)
            if max(G,E) >= M:
                if (G >= E):
                    case_str = "1.b.i.A"
                    weights['wgg'] = (G+M)/(2*G)
                    weights['wmg'] = (G-M)/(2*G)
                    weights['wme'] = 0
                    weights['wee'] = 1
                    weights['wgd'] = 0
                    weights['wmd'] = 0
                    weights['wed'] = 1
                else: # G < E
                    case_str = "1.b.i.B"
                    weights['wgg'] = 1
                    weights['wmg'] = 0
                    weights['wme'] = (E-M)/(2*E)
                    weights['wee'] = (E+M)/(2*E)
                    weights['wgd'] = 1
                    weights['wmd'] = 0
                    weights['wed'] = 0
            else: # max(G,E) < M
                if (G >= E):
                    case_str = "1.b.ii.A"
                    weights['wgg'] = 1
                    weights['wmg'] = 0
                    weights['wme'] = 0
                    weights['wee'] = 1
                    weights['wgd'] = 0
                    weights['wmd'] = 0
                    weights['wed'] = 1
                else: # G < E
                    case_str = "1.b.ii.B"
                    weights['wgg'] = 1
                    weights['wmg'] = 0
                    weights['wme'] = 0
                    weights['wee'] = 1
                    weights['wgd'] = 1
                    weights['wmd'] = 0
                    weights['wed'] = 0
    elif (D + min(G,E) < T/3): # and M <= T/3
        if (G >= E):
            case_str = "2.a"
            weights['wgg'] = (G+M)/(2*G)
            weights['wmg'] = (G-M)/(2*G)
            weights['wme'] = 0
            weights['wee'] = 1
            weights['wgd'] = 0
            weights['wmd'] = 0
            weights['wed'] = 1
        else: # G < E
            case_str = "2.b"
            weights['wgg'] = 1
            weights['wmg'] = 0
            weights['wme'] = (E-M)/(2*E)
            weights['wee'] = (E+M)/(2*E)
            weights['wgd'] = 1
            weights['wmd'] = 0
            weights['wed'] = 0
    else: # M <= T/3 and D + min(G,E) >= T/3
        if (D >= abs(G-E)):
            case_str = "3.a"
            x = 2*T/(3*(T-M))
            weights['wgg'] = x
            weights['wmg'] = 1-x
            weights['wme'] = 1-x
            weights['wee'] = x
            weights['wgd'] = (T/3 - x*G)/D
            weights['wmd'] = 1-x
            weights['wed'] = (T/3-x*E)/D
        else: # D < abs(G-E)
            if (G >= E):
                case_str = "3.b.i"
                x = T/(3*(E+D))
                weights['wgg'] = (T/3)/G
                weights['wmg'] = (G-T/3)/G
                weights['wme'] = 1-x
                weights['wee'] = x
                weights['wgd'] = 0
                weights['wmd'] = 1-x
                weights['wed'] = x
            else: # G < E
                case_str = "3.b.ii"
                x = T/(3*(G+D))
                weights['wgg'] = x
                weights['wmg'] = 1-x
                weights['wme'] = (E-T/3)/E
                weights['wee'] = (T/3)/E
                weights['wgd'] = x
                weights['wmd'] = 1-x
                weights['wed'] = 0

    return weights, case_str



if __name__ == '__main__':

    def print_allocation(bws, weights):
        print('G->g: {}'.format(bws['G']*weights['wgg']))
        print('G->m: {}'.format(bws['G']*weights['wmg']))
        print('M->m: {}'.format(bws['M']*weights['wmm']))
        print('E->m: {}'.format(bws['E']*weights['wme']))
        print('E->e: {}'.format(bws['E']*weights['wee']))
        print('D->g: {}'.format(bws['D']*weights['wgd']))
        print('D->m: {}'.format(bws['D']*weights['wmd']))
        print('D->e: {}'.format(bws['D']*weights['wed']))
        print('\\bwplot{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}{{{:.1f}}}'.\
            format(bws['G']*weights['wgg'], bws['G']*weights['wmg'],
                bws['M']*weights['wmm'], bws['E']*weights['wme'],
                bws['E']*weights['wee'], bws['D']*weights['wgd'],
                bws['D']*weights['wmd'], bws['D']*weights['wed'],
                (bws['G']+bws['M']+bws['E']+bws['D'])/3))

    # example of bws for each weight case
    cases_bws = []
    cases_bws.append(('1.a.i', {'G':30, 'M':150, 'E':20, 'D':100}))
    cases_bws.append(('1.a.ii', {'G':20, 'M':150, 'E':30, 'D':100}))
    cases_bws.append(('1.b.i.A', {'G':130, 'M':110, 'E':20, 'D':40}))
    cases_bws.append(('1.b.i.B', {'G':20, 'M':110, 'E':130, 'D':40}))
    cases_bws.append(('1.b.ii.A', {'G':90, 'M':150, 'E':20, 'D':40}))
    cases_bws.append(('1.b.ii.B', {'G':20, 'M':150, 'E':90, 'D':40}))
    cases_bws.append(('2.a', {'G':150, 'M':80, 'E':30, 'D':40}))
    cases_bws.append(('2.b', {'G':30, 'M':80, 'E':150, 'D':40}))
    cases_bws.append(('3.a', {'G':75, 'M':65, 'E':60, 'D':100}))
    cases_bws.append(('3.b.i', {'G':130, 'M':50, 'E':55, 'D':65}))
    cases_bws.append(('3.b.ii', {'G':55, 'M':50, 'E':130, 'D':65}))

    for case, bws in cases_bws:
        print('')
        print('Case {}'.format(case))
        weights = alt2_weights(bws['G'], bws['M'], bws['E'], bws['D'])
        print_allocation(bws, weights)
