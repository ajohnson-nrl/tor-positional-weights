import os
import os.path
import argparse
import json

def bandwidth_weight_case(G, M, E, D):
    T = G + M + E + D
    if (E >= T/3) and (G >= T/3):
        return '1'
    elif (E < T/3) and (G < T/3):
        R = min(G, E)
        S = max(G, E)
        if (R+D) < S:
            if (G > E):
                return '2.a.i'
            else:
                return '2.a.ii'
        else:
            if (G >= M) and (E >= G-M):
                return '2.b.i'
            elif ((G < M) or (E < G-M)) and (M <= T/3):
                return '2.b.ii'
            else:
                if (T/3 - E <= D):
                    return '2.b.iii.A'
                else:
                    return '2.b.iii.B'
    else:
        S = min(G, E)
        if (S+D < T/3):
            if (G < E):
                if (E < M):
                    return '3.a.i.A'
                else:
                    return '3.a.i.B'
            else:
                if (G < M):
                    return '3.a.ii.A'
                else:
                    return '3.a.ii.B'
        else:
            if (G < E):
                return '3.b.i'
            else:
                return '3.b.ii'


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Analyze positional weight cases in Tor consensuses')
    parser.add_argument('year_start', type=int,
                    help='start year (integer)')
    parser.add_argument('month_start', type=int,
                    help='start month (integer 1 to 12)')
    parser.add_argument('year_end', type=int,
                    help='end year (integer)')
    parser.add_argument('month_end', type=int,
                    help='end month (integer 1 to 12)')
    args = parser.parse_args()

    posweight_cases = {'1':0, '2.a.i':0, '2.a.ii':0, '2.b.i':0, '2.b.ii':0, '2.b.iii.A':0, '2.b.iii.B':0, '3.a.i.A':0, '3.a.i.B':0, '3.a.ii.A':0, '3.a.ii.B':0, '3.b.i':0, '3.b.ii':0}
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
                for datetime in sorted(month_bw_data.keys()):
                    bw_data = month_bw_data[datetime]
                    case = bandwidth_weight_case(bw_data['G'], bw_data['M'], bw_data['E'],
                        bw_data['D'])
                    print('{}: Case {}'.format(datetime, case))
                    posweight_cases[case] += 1
            else:
                print('Missing processed consensus {}'.format(filename))
            month += 1
        month = 1
    case_total = 0    
    for case, count in posweight_cases.items():
        print('{}: {}'.format(case, count))
        case_total = case_total + count
    print('Case Total:', case_total)
#    in_consensuses_dir = 'consensuses/consensuses-2019-08'
#    num_consensuses = 0
#    pathnames = []
#    for dirpath, dirnames, fnames in os.walk(in_consensuses_dir):
#        for fname in fnames:
#            pathnames.append(os.path.join(dirpath,fname))
#    pathnames.sort()
#    for pathname in pathnames:
#        filename = os.path.basename(pathname)
#        if (filename[0] == '.'):
#            continue
#    for pathname in pathnames:
#        process_consensus(pathname)
