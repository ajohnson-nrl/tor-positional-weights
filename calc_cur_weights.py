def tor_weights(G, M, E, D, alt=False):
    """
    Calculate Tor positional weights. If alt parameter is True, use alternate weights
    that are correct and maximize throughput in error cases 2.b.iii.A
    and 2.b.iii.B.
    """
    weights = dict()
    T = G + M + E + D
    weights['wmm'] = 1
    if (E >= T/3) and (G >= T/3):
        case_str = "T.1"
        weights['wgg'] = (G+E+M)/(3*G)
        weights['wmg'] = (2*G-E-M)/(3*G)
        weights['wme'] = (2*E-G-M)/(3*E)
        weights['wee'] = (E+G+M)/(3*E)
        weights['wgd'] = 1/3
        weights['wmd'] = 1/3
        weights['wed'] = 1/3
    elif (E < T/3) and (G < T/3):
        R = min(G,E)
        S = max(G,E)
        if (R+D < S):
            if (G > E):
                case_str = "T.2.a.i"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = 0
                weights['wee'] = 1
                weights['wgd'] = 0
                weights['wmd'] = 0
                weights['wed'] = 1
            else:
                case_str = "T.2.a.ii"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = 0
                weights['wee'] = 1
                weights['wgd'] = 1
                weights['wmd'] = 0
                weights['wed'] = 0
        else:
            if (G >= M) and (E >= (G-M)):
                case_str = "T.2.b.i"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = (G-M)/E
                weights['wee'] = (E-G+M)/E
                weights['wgd'] = (2*D+2*E-4*G+2*M)/(6*D)
                weights['wmd'] = (2*D+2*E-4*G+2*M)/(6*D)
                weights['wed'] = (D-2*E+4*G-2*M)/(3*D)
            elif ((G < M) or (E < G-M)) and (M <= T/3):
                case_str = "T.2.b.ii"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = 0
                weights['wee'] = 1
                weights['wgd'] = (D+E-2*G+M)/(3*D)
                weights['wmd'] = (D-2*M+G+E)/(3*D)
                weights['wed'] = (D-2*E+G+M)/(3*D)
            else:
                if (T/3-E <= D):
                    if (not alt):
                        # produces unbalanced weights (balance is possible)
                        case_str = "T.2.b.iii.A"
                        weights['wgg'] = 1
                        weights['wmg'] = 0
                        weights['wme'] = 0
                        weights['wee'] = 1
                        weights['wgd'] = (2*D+2*E-G-M)/(3*D)
                        weights['wmd'] = 0
                        weights['wed'] = (D-2*E+G+M)/(3*D)
                    else:
                        # produces balanced weights
                        case_str = "T.2.b.iii.A (alt)"
                        weights['wgg'] = 1
                        weights['wmg'] = 0
                        weights['wme'] = 0
                        weights['wee'] = 1
                        weights['wgd'] = (E-G+D)/(2*D)
                        weights['wmd'] = 0
                        weights['wed'] = (D+G-E)/(2*D)
                else: # T/3 - E > D
                    if (not alt):
                        # produces invalid weights
                        case_str = "T.2.b.iii.B"
                        weights['wgg'] = 1
                        weights['wmg'] = 0
                        weights['wme'] = 0
                        weights['wee'] = 1
                        weights['wgd'] = (2*D+2*E-G-M)/(3*D)
                        weights['wmd'] = 0
                        weights['wed'] = (D-2*E+G+M)/(3*D)
                    else:
                        # candidate valid weights
                        case_str = "T.2.b.iii.B (alt)"
                        weights['wgg'] = 1
                        weights['wmg'] = 0
                        weights['wme'] = 0
                        weights['wee'] = 1
                        weights['wgd'] = (E-G+D)/(2*D)
                        weights['wmd'] = 0
                        weights['wed'] = (D+G-E)/(2*D)
    else: # E < T/3 XOR G < T/3
        S = min(G,E)
        if (S+D < T/3):
            if (G < E):
                if (E < M):
                    case_str = "T.3.a.i.A"
                    weights['wgg'] = 1
                    weights['wmg'] = 0
                    weights['wme'] = 0
                    weights['wee'] = 1
                    weights['wgd'] = 1
                    weights['wmd'] = 0
                    weights['wed'] = 0
                else: # E >= M
                    case_str = "T.3.a.i.B"
                    weights['wgg'] = 1
                    weights['wmg'] = 0
                    weights['wme'] = (E-M)/(2*E)
                    weights['wee'] = (E+M)/(2*E)
                    weights['wgd'] = 1
                    weights['wmd'] = 0
                    weights['wed'] = 0
            else: # G >= E
                if (G < M):
                    case_str = "T.3.a.ii.A"
                    weights['wgg'] = 1
                    weights['wmg'] = 0
                    weights['wme'] = 0
                    weights['wee'] = 1
                    weights['wgd'] = 0
                    weights['wmd'] = 0
                    weights['wed'] = 1
                else: # G >= M
                    case_str = "T.3.a.ii.B"
                    weights['wgg'] = (G+M)/(2*G)
                    weights['wmg'] = (G-M)/(2*G)
                    weights['wme'] = 0
                    weights['wee'] = 1
                    weights['wgd'] = 0
                    weights['wmd'] = 0
                    weights['wed'] = 1
        else: # S+D >= T/3
            if (G < E):
                case_str = "T.3.b.i"
                weights['wgg'] = 1
                weights['wmg'] = 0
                weights['wme'] = (E-M)/(2*E)
                weights['wee'] = (E+M)/(2*E)
                weights['wgd'] = (D-2*G+E+M)/(3*D)
                weights['wmd'] = (2*D+2*G-E-M)/(6*D)
                weights['wed'] = (2*D+2*G-E-M)/(6*D)
            else: # G >= E
                case_str = "T.3.b.ii"
                weights['wgg'] = (G+M)/(2*G)
                weights['wmg'] = (G-M)/(2*G)
                weights['wme'] = 0
                weights['wee'] = 1
                weights['wgd'] = (2*D+2*E-G-M)/(6*D)
                weights['wmd'] = (2*D+2*E-G-M)/(6*D)
                weights['wed'] = (D-2*E+G+M)/(3*D)

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
    cases_bws = dict()
    cases_bws['1'] = {'G':120, 'M':20, 'E':100, 'D':60}
    cases_bws['2.a.i'] = {'G':90, 'M':140, 'E':20, 'D':50}
    cases_bws['2.a.ii'] = {'G':20, 'M':140, 'E':90, 'D':50}
    cases_bws['2.b.i'] = {'G':90, 'M':70, 'E':60, 'D':80}
    cases_bws['2.b.ii'] = {'G':70, 'M':80, 'E':60, 'D':90}
    cases_bws['2.b.iii.A'] = {'G':50, 'M':120, 'E':40, 'D':90}
    cases_bws['2.b.iii.B'] = {'G':80, 'M':130, 'E':40, 'D':50}
    cases_bws['3.a.i.A'] = {'G':30, 'M':120, 'E':110, 'D':40}
    cases_bws['3.a.i.B'] = {'G':30, 'M':90, 'E':120, 'D':60}
    cases_bws['3.a.ii.A'] = {'G':110, 'M':120, 'E':30, 'D':40}
    cases_bws['3.a.ii.B'] = {'G':120, 'M':90, 'E':30, 'D':60}
    cases_bws['3.b.i'] = {'G':50, 'M':70, 'E':110, 'D':70}
    cases_bws['3.b.ii'] = {'G':110, 'M':70, 'E':50, 'D':70}
    error_cases = ['2.b.iii.A', '2.b.iii.B']

    print('Tor positional weights')
    for case in sorted(cases_bws):
        bws = cases_bws[case]
        print('')
        print('Case {}'.format(case))
        weights = pos_weights(bws['G'], bws['M'], bws['E'], bws['D'])
        print_allocation(bws, weights)
    print('\nAlternative weights for error cases')
    for case in error_cases:
        bws = cases_bws[case]
        print('')
        print('Error case {}'.format(case))
        weights = pos_weights(bws['G'], bws['M'], bws['E'], bws['D'], True)
        print_allocation(cases_bws[case], weights)
