def alt1_weights(G, M, E, D):
    '''
    In-progress script to compute w_{xy} values.
    '''
    weights = dict()
    T = G + M + E + D
#     weights['wmm'] = 1
    if T == 0:
        raise RuntimeError('Total bandwidth T is 0!')
    if (M > T/3): # Unable to balance positions
    # 
        if G >= M: # Must have G >= M > E because M > T/3
        #1.a
            # Sec. 5.1
            # Lemma 5.1
#             case_str = "Lemma 5.1"
            case_str = "Alt1 1.a"
            Gg = (G+M)/2
            Gm = (G-M)/2
            Mm = M
            Ee = E
            Em = 0
            Dg = 0
            Dm = 0
            De = D
        else: # M > G
        # 1.b
            if E >= M: # Must have E >= M > G because M > T/3 and we're not in G>=M
            # 1.b.i
                # Sec. 5.2
                # Lemma 5.2
#                 case_str = "Lemma 5.2"
                case_str = "Alt1 1.b.i"
                Gg = G
                Gm = 0
                Mm = M
                Ee = (E+M)/2
                Em = (E-M)/2
                Dg = D
                Dm = 0
                De = 0
            else: # M > E, G
            # 1.b.i
                if G >= E: # Must have M > G, E because not in above cases
                # 1.b.i.A
                    if G >= E + D:
                    # 1.b.i.A.I
                        # Lemma 5.3
#                         case_str = "Lemma 5.3"
                        case_str = "Alt1 1.b.i.A.I"
                        Gg = G
                        Gm = 0
                        Mm = M
                        Ee = E
                        Em = 0
                        Dg = 0
                        Dm = 0
                        De = D
                    else: # E + D > G:
                    # 1.b.i.A.II
                        # M > G >= E, E+D > G
                        # Lemma 5.4
#                         case_str = "Lemma 5.4"
                        case_str = "Alt1 1.b.i.A.I"
                        Gg = G
                        Gm = 0
                        Mm = M
                        Ee = E
                        Em = 0
                        Dg = (D+E-G)/2
                        Dm = 0
                        De = (D+G-E)/2
                else: # E > G: # Must have M > E > G because we're not in E >= M
                # 1.b.i.B
                    # Sec. 5.4
                    if E >= G + D:
                    # 1.b.i.B.I
                        # Lemma 5.5
#                         case_str = "Lemma 5.5"
                        case_str = "Alt1 1.b.i.B.I"
                        Gg = G
                        Gm = 0
                        Mm = M
                        Ee = E
                        Em = 0
                        Dg = D
                        Dm = 0
                        De = 0
                    else: # G + D > E
                    # 1.b.i.B.II
                        # Lemma 5.6
#                         case_str = "Lemma 5.6"
                        case_str = "Alt1 1.b.i.B.II"
                        Gg = G
                        Gm = 0
                        Mm = M
                        Ee = E
                        Em = 0
                        Dg = (D+E-G)/2
                        Dm = 0
                        De = (D-E+G)/2
    else: # M <= T/3
    # 2
        # We'll start with the cases in which we're unable to balance the positions
        # E+D < T/3 or G+D < T/3 means we cannot balance the positions
        # Note that we cannot have both of these simultaneously as well as M <= T/3,
        # else we'd have G + M + E + 2*D < T
        if E + D < T/3: # M <= T/3 but unable to balance positions
        # 2.a
            # Lemma 6.1
#             case_str = "Lemma 6.1"
            case_str = "Alt1 2.a"
            Gg = (G+M)/2
            Gm = (G-M)/2
            Mm = M
            Ee = E
            Em = 0
            Dg = 0
            Dm = 0
            De = D
        elif G + D < T/3: # M <= T/3 but unable to balance positions
        # 2.b
            # Lemma 6.2
#             case_str = "Lemma 6.2"
            case_str = "Alt1 2.b"
            Gg = G
            Gm = 0
            Mm = M
            Ee = (E+M)/2
            Em = (E-M)/2
            Dg = D
            Dm = 0
            De = 0
        else: # M <= T/3, E+D >= T/3, and G+D >= T/3
        # 2.c
            # Now, we're able to balance the positions
            if D <= T/3:
            # 2.c.i
                if G < T/3: # Thus G+D < 2*T/3
                # 2.c.i.A
                    # Lemma 7.4
#                     case_str = "Lemma 7.4 (D<=T/3)"
                    case_str = "Alt1 2.c.i.A"
                    Gg = G
                    Gm = 0
                    Mm = M
                    Ee = 2*T/3 - D - G
                    Em = E + D + G - 2*T/3
                    Dg = T/3 - G
                    Dm = 0
                    De = D + G - T/3
                else: # G >= T/3
                # 2.c.i.B
                    # Lemma 7.1
#                     case_str = "Lemma 7.1"
                    case_str = "Alt1 2.c.i.B"
                    Gg = T/3
                    Gm = G - T/3
                    Mm = M
                    Ee = (T-3*D)/3
                    Em = E - Ee # = E - (T-3*D)/3
                    Dg = 0 # Corrected from D
                    Dm = 0
                    De = D # Corrected from 0
            else: # D > T/3
            # 2.c.ii
                if G+D <= 2*T/3: # Must have G < T/3
                # 2.c.ii.A
                    # Lemma 7.4
#                     case_str = "Lemma 7.4 (D>T/3)"
                    case_str = "Alt1 2.c.ii.A"
                    Gg = G
                    Gm = 0
                    Mm = M
                    Ee = 2*T/3 - D - G
                    Em = E + D + G - 2*T/3
                    Dg = T/3 - G
                    Dm = 0
                    De = D + G - T/3
                else: # G+D > 2*T/3
                # 2.c.ii.B
                    if D >= G:
                    # 2.c.ii.B.I
                        # Lemma 7.2
#                         case_str = "Lemma 7.2"
                        case_str = "Alt1 2.c.ii.B.I"
                        Gg = (2*T/3)*(G/(D+G))
                        Gm = G - Gg
                        Mm = M
                        Ee = 0
                        Em = E
                        Dg = T/3 - Gg
                        Dm = D - 2*T/3 + (2*T/3)*(G/(D+G))
                        De = T/3
                    else: # D < G:
                    # 2.c.ii.B.II
                        # Lemma 7.3
#                         case_str = "Lemma 7.3"
                        case_str = "Alt1 2.c.ii.B.II"
                        Gg = T/3
                        Gm = G - T/3
                        Mm = M
                        Ee = 0
                        Em = E
                        Dg = 0
                        Dm = D - T/3
                        De = T/3

    if G > 0:
        weights['wgg'] = Gg / G
        weights['wmg'] = Gm / G
    else:
        weights['wgg'] = float("NaN")
        weights['wmg'] = float("NaN")

    if M > 0:
        weights['wmm'] = Mm / M
    else:
        weights['wmm'] = float("NaN")

    if E > 0:
        weights['wme'] = Em / E
        weights['wee'] = Ee / E
    else:
        weights['wme'] = float("NaN")
        weights['wee'] = float("NaN")

    if D > 0:
        weights['wgd'] = Dg / D
        weights['wmd'] = Dm / D
        weights['wed'] = De / D
    else:
        weights['wgd'] = float("NaN")
        weights['wmd'] = float("NaN")
        weights['wed'] = float("NaN")



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
        weights1 = alt1_weights(bws['G'], bws['M'], bws['E'], bws['D'])
#         weights2 = alt2_weights(bws['G'], bws['M'], bws['E'], bws['D'])
        print_allocation(bws, weights1)
