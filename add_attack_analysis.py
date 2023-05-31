import os
import os.path
import argparse
import json
import posweight_analysis
import math
import sys
import calc_cur_weights

def valid_weights(weights):
    """Check if all weights are in [0,1] and weights for a position sum to 1."""
    tol = 1e-3
    g_weights = [weights['wgg'], weights['wmg']]
    m_weights = [weights['wmm']]
    d_weights = [weights['wgd'], weights['wmd'], weights['wed']]
    e_weights = [weights['wme'], weights['wee']]
    for p_weights in [g_weights, m_weights, d_weights, e_weights]:
        for w in p_weights:
            if (w < 0) or (w > 1):
                return False
        if (abs(sum(p_weights)-1) > tol):
            return False
    return True

def calc_throughput_sat_min(G, M, E, D, weights):
    """Calculate throughput at which some relay class (G, M, E, or D) saturates its total
    throughput. For optimal weightings, there will be a "bottleneck" position at which all classes
    used in that position simultaneously saturate. For some sub-optimal weightings, there may not
    be a position at which all classes simultaneously saturate, and so some clients will by chance
    experience limits before others."""
    # Check if weights are valid, default to naive selection if not
    if (valid_weights(weights)):
        wgg = weights['wgg']
        wmg = weights['wmg']
        wmm = weights['wmm']
        wme = weights['wme']
        wee = weights['wee']
        wgd = weights['wgd']
        wmd = weights['wmd']
        wed = weights['wed']
    else:
        wgg = 1
        wmg = 1
        wmm = 1
        wme = 1
        wee = 1
        wgd = 1
        wmd = 1
        wed = 1

    # calculate total traffic multiple (in [0,3] due to 3-hop paths) carried by each relay class
    guard_tot = G*wgg + D*wgd
    middle_tot = G*wmg + M*wmm + E*wme + D*wmd
    exit_tot = E*wee + D*wed
    G_multiple = G*wgg/guard_tot + G*wmg/middle_tot
    M_multiple = M*wmm/middle_tot
    E_multiple = E*wme/middle_tot + E*wee/exit_tot
    D_multiple = D*wgd/guard_tot + D*wmd/middle_tot + D*wed/exit_tot
    # calculate traffic level at which each relay class would be saturated
    G_sat = G/G_multiple if G_multiple>0 else float('inf')
    M_sat = M/M_multiple if M_multiple>0 else float('inf')
    E_sat = E/E_multiple if E_multiple>0 else float('inf')
    D_sat = D/D_multiple if D_multiple>0 else float('inf')

    return min(G_sat, M_sat, E_sat, D_sat)

def print_attack(start_case, end_case, G_orig, M_orig, E_orig, D_orig, G_add, M_add, E_add, D_add):
    T_orig = G_orig + M_orig + E_orig + D_orig
    T_add = G_add + M_add + E_add + D_add
    print('\tAttack {} -> {}'.format(start_case, end_case))
    print('\t\tG: {:.2e} -> {:.2e} (+{:.2e}, +{:.2f}%)'.format(G_orig, G_orig+G_add, G_add,
        100*G_add/G_orig))
    print('\t\tM: {:.2e} -> {:.2e} (+{:.2e}, +{:.2f}%)'.format(M_orig, M_orig+M_add, M_add,
        100*M_add/M_orig))
    print('\t\tE: {:.2e} -> {:.2e} (+{:.2e}, +{:.2f}%)'.format(E_orig, E_orig+E_add, E_add,
        100*E_add/E_orig))
    print('\t\tD: {:.2e} -> {:.2e} (+{:.2e}, +{:.2f}%)'.format(D_orig, D_orig+D_add, D_add,
        100*D_add/D_orig))
    print('\t\tT: {:.2e} -> {:.2e} (+{:.2e}, +{:.2f}%)'.format(T_orig, T_orig+T_add, T_add,
        100*T_add/T_orig))

def print_attack_tput(tput_sat_min, attack_tput_sat_min, alt_attack_tput_sat_min):
    print('\t\tThroughput saturation min: {:.2e} -> {:.2e} (diff {:.2e}, {:.2f}%)'.\
        format(tput_sat_min, attack_tput_sat_min, attack_tput_sat_min-tput_sat_min,
        100*(attack_tput_sat_min-tput_sat_min)/tput_sat_min))
    print('\t\tAlt. throughput saturation min: {:.2e} -> {:.2e} (diff {:.2e}, {:.2f}%)'.\
        format(tput_sat_min, alt_attack_tput_sat_min, alt_attack_tput_sat_min-tput_sat_min,
        100*(alt_attack_tput_sat_min-tput_sat_min)/tput_sat_min))

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Analyze attacks manipulating Tor positional weights in consensuses')
    parser.add_argument('year_start', type=int,
                    help='start year (integer)')
    parser.add_argument('month_start', type=int,
                    help='start month (integer 1 to 12)')
    parser.add_argument('year_end', type=int,
                    help='end year (integer)')
    parser.add_argument('month_end', type=int,
                    help='end month (integer 1 to 12)')
    parser.add_argument('--print_all', action='store_true',
                    help='print attack results for each consensus')
    args = parser.parse_args()

    # invalid (-> 2.b.iii.B) weight attack results
    attack_results_2b3b = dict()

    month = args.month_start
    for year in range(args.year_start, args.year_end+1):
        while ((year < args.year_end) and (month <= 12)) or\
            (month <= args.month_end):
            month_str = '{:0>2d}'.format(month)
            filename = 'processed-consensuses/consensuses-bwdata-{}-{}.json'.format(year, month_str)
            if (os.path.isfile(filename)):
                f = open(filename, 'r')
                month_bw_data = json.load(f)
                f.close()
                # bw_data = {'G':0, 'num_G':0, 'M':0, 'num_M':0, 'E':0, 'num_E':0, 'D':0, 'num_D':0}
                # bw_data['bwweightscale'] = document.params['bwweightscale']
                # bw_data['bandwidth_weights'] = document.bandwidth_weights
                # month_bw_data['{}-{}-{}-{}'.format(year, month_str, day_str, hour_str)] = bw_data
                for datetime in sorted(month_bw_data.keys()):
                    bw_data = month_bw_data[datetime]
                    case = posweight_analysis.bandwidth_weight_case(bw_data['G'], bw_data['M'],
                        bw_data['E'], bw_data['D'])
                    # calculate weights
                    weights, _ = calc_cur_weights.tor_weights(bw_data['G'], bw_data['M'], bw_data['E'],
                        bw_data['D'])
                    # calculate throughput saturation min
                    tput_sat_min = calc_throughput_sat_min(bw_data['G'], bw_data['M'],
                        bw_data['E'], bw_data['D'], weights)
                    if (args.print_all):
                        print('{}: Case {}'.format(datetime, case))
                    # analyze attack pushing to error state
                    if (case == '3.a.ii.B'):
                        # Attack 3.a.ii.B -> 2.b.iii.A
                        end_case = '2.b.iii.A'
                        G = bw_data['G']
                        M = bw_data['M']
                        E = bw_data['E']
                        D = bw_data['D']
                        G_add = 0
                        M_add = 0
                        E_add = 0
                        D_add = 0
                        E_add += (G-D) - E
                        E += E_add
                        M_add += (G+1) - M
                        M += M_add
                        D_add += 1
                        D += 1
                        # calculate weights in error state
                        attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D)
                        # calculate throughput saturation min
                        attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D, attack_weights)
                        # calculate alternative weights that fix errors (ie valid and balanced)
                        alt_attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D, alt=True)
                        alt_attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D,
                            alt_attack_weights)
                        # sanity check: desired attack state was reached
                        attack_case = posweight_analysis.bandwidth_weight_case(G, M, E, D)
                        if (attack_case != end_case):
                            print('Unexpected attack case: {}'.format(attack_case))
                            sys.exit()
                        # print results
                        if (args.print_all):
                            print_attack(case, end_case, bw_data['G'], bw_data['M'], bw_data['E'],
                                bw_data['D'], G_add, M_add, E_add, D_add)
                            print_attack_tput(tput_sat_min, attack_tput_sat_min,
                                alt_attack_tput_sat_min)

                        # Attack 3.a.ii.B -> 2.b.iii.B
                        end_case = '2.b.iii.B'
                        G = bw_data['G']
                        M = bw_data['M']
                        E = bw_data['E']
                        D = bw_data['D']
                        G_add = 0
                        M_add = 0
                        E_add = 0
                        D_add = 0
                        E_add += (G-D) - E
                        E += E_add
                        M_add += (G+1) - M
                        M += M_add
                        # calculate weights in error state
                        attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D)
                        # calculate throughput saturation min
                        attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D, attack_weights)
                        # calculate alternative weights that fix errors (ie valid and balanced)
                        alt_attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D, alt=True)
                        alt_attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D,
                            alt_attack_weights)
                        # sanity check: desired attack state was reached
                        attack_case = posweight_analysis.bandwidth_weight_case(G, M, E, D)
                        if (attack_case != end_case):
                            print('Unexpected attack case: {}'.format(attack_case))
                            sys.exit()
                        # save results
                        attack_results_2b3b[datetime] = {'T_add':(G_add + M_add + E_add + D_add),
                            'T_orig':(bw_data['G']+bw_data['M']+bw_data['E']+bw_data['D']),
                            'attack_tput_sat_min':attack_tput_sat_min,
                            'orig_tput_sat_min':tput_sat_min}
                        # print results
                        if (args.print_all):
                            print_attack(case, end_case, bw_data['G'], bw_data['M'], bw_data['E'],
                                bw_data['D'], G_add, M_add, E_add, D_add)
                            print_attack_tput(tput_sat_min, attack_tput_sat_min,
                                alt_attack_tput_sat_min)
                    elif (case == '3.b.ii'):
                        # Attack 3.b.ii -> 2.b.iii.A
                        end_case = '2.b.iii.A'
                        G = bw_data['G']
                        M = bw_data['M']
                        E = bw_data['E']
                        D = bw_data['D']
                        G_add = 0
                        M_add = 0
                        E_add = 0
                        D_add = 0
                        D_E = D + E # treat D and E as one class temporarily
                        D_E_add = 0
                        if (D+E < G):
                            D_E_add += G - (D+E)
                            D_E += D_E_add
                        M_add += math.floor((G+D_E)/2) + 1 - M
                        M += M_add
                        if (D_E == G):
                            D_E_add +=1
                            D_E += 1
                        # put as much of D_E_add in E as possible (constraint is E<T/3)
                        E_add = min(D_E_add, math.ceil((G+M+D_E)/3 - 1 - E))
                        E += E_add
                        D_add = D_E_add - E_add
                        D += D_add
                        # calculate weights in error state
                        attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D)
                        # calculate throughput saturation min
                        attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D, attack_weights)
                        # calculate alternative weights that fix errors (ie valid and balanced)
                        alt_attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D, alt=True)
                        alt_attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D,
                            alt_attack_weights)
                        # sanity check: desired attack state was reached
                        attack_case = posweight_analysis.bandwidth_weight_case(G, M, E, D)
                        if (attack_case != end_case):
                            print('Unexpected attack case: {}'.format(attack_case))
                            sys.exit()
                        # print results
                        if (args.print_all):
                            print_attack(case, end_case, bw_data['G'], bw_data['M'], bw_data['E'],
                                bw_data['D'], G_add, M_add, E_add, D_add)
                            print_attack_tput(tput_sat_min, attack_tput_sat_min,
                                alt_attack_tput_sat_min)

                        # Attack 3.b.ii -> 2.b.iii.B
                        end_case = '2.b.iii.B'
                        G = bw_data['G']
                        M = bw_data['M']
                        E = bw_data['E']
                        D = bw_data['D']
                        G_add = 0
                        M_add = 0
                        E_add = 0
                        D_add = 0
                        D_E = D + E # treat D and E as one class temporarily
                        D_E_add = 0
                        if (D+E < G):
                            D_E_add += G - (D+E)
                            D_E += D_E_add
                        if (G == D_E):
                            M_add += G + 1 - M
                            M += M_add
                        else: # G < D_E
                            M_add += (D_E+(D_E-G)+1) - M
                            M += M_add
                        # put as much of D_E_add in E as possible (constraint is E<T/3)
                        E_add = min(D_E_add, math.ceil((G+M+D_E)/3 - 1 - E))
                        E += E_add
                        D_add = D_E_add - E_add
                        D += D_add
                        # calculate weights in error state
                        attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D)
                        # calculate throughput saturation min
                        attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D, attack_weights)
                        # calculate alternative weights that fix errors (ie valid and balanced)
                        alt_attack_weights, _ = calc_cur_weights.tor_weights(G, M, E, D, alt=True)
                        alt_attack_tput_sat_min = calc_throughput_sat_min(G, M, E, D,
                            alt_attack_weights)
                        # sanity check: desired attack state was reached
                        attack_case = posweight_analysis.bandwidth_weight_case(G, M, E, D)
                        if (attack_case != end_case):
                            print('Unexpected attack case: {}'.format(attack_case))
                            sys.exit()
                        # save results
                        attack_results_2b3b[datetime] = {'T_add':(G_add + M_add + E_add + D_add),
                            'T_orig':(bw_data['G']+bw_data['M']+bw_data['E']+bw_data['D']),
                            'attack_tput_sat_min':attack_tput_sat_min,
                            'orig_tput_sat_min':tput_sat_min}
                        # print results
                        if (args.print_all):
                            print_attack(case, end_case, bw_data['G'], bw_data['M'], bw_data['E'],
                                bw_data['D'], G_add, M_add, E_add, D_add)
                            print_attack_tput(tput_sat_min, attack_tput_sat_min,
                                alt_attack_tput_sat_min)
            else:
                print('Processed consensus does not exist: {}'.format(filename))
            month += 1
        month = 1

    ### print invalid-state attack (-> 2.b.iii.B) summary ###
    print('\nSummary of invalid-state attack (-> 2.b.iii.B)')
    # print absolute and relative bandwidth added stats
    sorted_by_T_add = sorted(attack_results_2b3b, key = lambda x: attack_results_2b3b[x]['T_add'])
    min_T_add = attack_results_2b3b[sorted_by_T_add[0]]
    print('\t Min. absolute added bandwidth: {:.2e} ({:.2f}%)'.format(min_T_add['T_add'],
        100*min_T_add['T_add']/min_T_add['T_orig']))
    median_T_add = attack_results_2b3b[sorted_by_T_add[(len(sorted_by_T_add)-1)//2]]
    print('\t Median absolute added bandwidth: {:.2e} ({:.2f}%)'.format(median_T_add['T_add'],
        100*median_T_add['T_add']/median_T_add['T_orig']))
    max_T_add = attack_results_2b3b[sorted_by_T_add[(len(sorted_by_T_add)-1)]]
    print('\t Max. absolute added bandwidth: {:.2e} ({:.2f}%)'.format(max_T_add['T_add'],
        100*max_T_add['T_add']/max_T_add['T_orig']))
    sorted_by_T_add_rel = sorted(attack_results_2b3b,
        key = lambda x: attack_results_2b3b[x]['T_add']/attack_results_2b3b[x]['T_orig'])
    min_T_add_rel = attack_results_2b3b[sorted_by_T_add_rel[0]]
    print('\t Min. relative added bandwidth: {:.2e} ({:.2f}%)'.format(min_T_add_rel['T_add'],
        100*min_T_add_rel['T_add']/min_T_add_rel['T_orig']))
    median_T_add_rel = attack_results_2b3b[sorted_by_T_add_rel[(len(sorted_by_T_add_rel)-1)//2]]
    print('\t Median relative added bandwidth: {:.2e} ({:.2f}%)'.format(median_T_add_rel['T_add'],
        100*median_T_add_rel['T_add']/median_T_add_rel['T_orig']))
    max_T_add_rel = attack_results_2b3b[sorted_by_T_add_rel[len(sorted_by_T_add)-1]]
    print('\t Max. relative added bandwidth: {:.2e} ({:.2f}%)'.format(max_T_add_rel['T_add'],
        100*max_T_add_rel['T_add']/max_T_add_rel['T_orig']))
    # print absolute and relative throughput reduction stats
    sorted_by_tput_delta = sorted(attack_results_2b3b,
        key = lambda x: attack_results_2b3b[x]['orig_tput_sat_min']-attack_results_2b3b[x]['attack_tput_sat_min'])
    max_tput_delta = attack_results_2b3b[sorted_by_tput_delta[-1]]
    print('\t Max absolute reduction throughput saturation min.: {:.2e} ({:.2f}%)'.format(\
        max_tput_delta['orig_tput_sat_min']-max_tput_delta['attack_tput_sat_min'],
        100*(max_tput_delta['orig_tput_sat_min']-max_tput_delta['attack_tput_sat_min'])/max_tput_delta['orig_tput_sat_min']))
    median_tput_delta = attack_results_2b3b[sorted_by_tput_delta[(len(sorted_by_tput_delta)-1)//2]]
    print('\t Median absolute reduction throughput saturation min.: {:.2e} ({:.2f}%)'.format(\
        median_tput_delta['orig_tput_sat_min']-median_tput_delta['attack_tput_sat_min'],
        100*(median_tput_delta['orig_tput_sat_min']-median_tput_delta['attack_tput_sat_min'])/median_tput_delta['orig_tput_sat_min']))
    min_tput_delta = attack_results_2b3b[sorted_by_tput_delta[0]]
    print('\t Min absolute reduction throughput saturation min.: {:.2e} ({:.2f}%)'.format(\
        min_tput_delta['orig_tput_sat_min']-min_tput_delta['attack_tput_sat_min'],
        100*(min_tput_delta['orig_tput_sat_min']-min_tput_delta['attack_tput_sat_min'])/min_tput_delta['orig_tput_sat_min']))
    sorted_by_tput_delta_rel = sorted(attack_results_2b3b,
        key = lambda x: (attack_results_2b3b[x]['orig_tput_sat_min']-attack_results_2b3b[x]['attack_tput_sat_min'])/attack_results_2b3b[x]['orig_tput_sat_min'])
    max_tput_delta_rel = attack_results_2b3b[sorted_by_tput_delta_rel[-1]]
    print('\t Max relative reduction throughput saturation min.: {:.2e} ({:.2f}%)'.format(\
        max_tput_delta_rel['orig_tput_sat_min']-max_tput_delta_rel['attack_tput_sat_min'],
        100*(max_tput_delta_rel['orig_tput_sat_min']-max_tput_delta_rel['attack_tput_sat_min'])/max_tput_delta_rel['orig_tput_sat_min']))
    median_tput_delta_rel =\
        attack_results_2b3b[sorted_by_tput_delta_rel[(len(sorted_by_tput_delta_rel)-1)//2]]
    print('\t Median relative reduction throughput saturation min.: {:.2e} ({:.2f}%)'.format(\
        median_tput_delta_rel['orig_tput_sat_min']-median_tput_delta_rel['attack_tput_sat_min'],
        100*(median_tput_delta_rel['orig_tput_sat_min']-median_tput_delta_rel['attack_tput_sat_min'])/median_tput_delta_rel['orig_tput_sat_min']))
    min_tput_delta_rel = attack_results_2b3b[sorted_by_tput_delta_rel[0]]
    print('\t Min relative reduction throughput saturation min.: {:.2e} ({:.2f}%)'.format(\
        min_tput_delta_rel['orig_tput_sat_min']-min_tput_delta_rel['attack_tput_sat_min'],
        100*(min_tput_delta_rel['orig_tput_sat_min']-min_tput_delta_rel['attack_tput_sat_min'])/min_tput_delta_rel['orig_tput_sat_min']))
