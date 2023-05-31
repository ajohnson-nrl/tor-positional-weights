import os
import stem
import stem.descriptor
import os.path
import argparse
import json


def relay_filter(rel_stat):
    """Filter for relays to ever be used in a position.
    """

    return (stem.Flag.RUNNING in rel_stat.flags) and\
        (stem.Flag.VALID in rel_stat.flags)


def process_consensus(filename):
    cons_f = open(filename, 'rb')
    print(filename)

    # read in consensus document
    consensus = None
    i = 0
    for document in stem.descriptor.parse_file(cons_f, validate=True,
        document_handler='DOCUMENT'):
        if (i > 0):
            raise ValueError('Unexpectedly found more than one consensus in file: {}'.format(pathname))
        consensus = document

        # store total weights in each relay class
        bw_data = {'G':0, 'num_G':0, 'M':0, 'num_M':0, 'E':0,
            'num_E':0, 'D':0, 'num_D':0}
        for fprint, rel_stat in document.routers.items():
            if not relay_filter(rel_stat):
                continue
            if (stem.Flag.GUARD in rel_stat.flags) and\
                (not stem.Flag.EXIT in rel_stat.flags):
                bw_data['G'] += rel_stat.bandwidth
                bw_data['num_G'] += 1
            elif (not stem.Flag.GUARD in rel_stat.flags) and\
                (not stem.Flag.EXIT in rel_stat.flags):
                bw_data['M'] += rel_stat.bandwidth
                bw_data['num_M'] += 1
            elif (not stem.Flag.GUARD in rel_stat.flags) and\
                (stem.Flag.EXIT in rel_stat.flags):
                bw_data['E'] += rel_stat.bandwidth
                bw_data['num_E'] += 1
            elif (stem.Flag.GUARD in rel_stat.flags) and\
                (stem.Flag.EXIT in rel_stat.flags):
                bw_data['D'] += rel_stat.bandwidth
                bw_data['num_D'] += 1
        # code to investigate positional weights
        if ('bwweightscale' in document.params):
            bw_data['bwweightscale'] = document.params['bwweightscale']
        else:
            bw_data['bwweightscale'] = None # Tor clients will default to 10000
        bw_data['bandwidth_weights'] = document.bandwidth_weights
        i += 1

    cons_f.close()

    return bw_data

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Process Tor consensuses into bandwidth class values')
    parser.add_argument('year_start', type=int,
                    help='start year (integer)')
    parser.add_argument('month_start', type=int,
                    help='start month (integer 1 to 12)')
    parser.add_argument('year_end', type=int,
                    help='end year (integer)')
    parser.add_argument('month_end', type=int,
                    help='end month (integer 1 to 12)')
    parser.add_argument('--day', type=int,
                    help='day to pick in each month, omit for all days (integer 1 to 31)')
    parser.add_argument('--hour', type=int,
                    help='hour to pick in each day, omit for all days (integer 0 to 23)')
    args = parser.parse_args()

    month = args.month_start
    for year in range(args.year_start, args.year_end+1):
        while ((year < args.year_end) and (month <= 12)) or\
            (month <= args.month_end):
            month_bw_data = dict()
            month_str = '{:0>2d}'.format(month)
            day_strs = []
            if (args.day is not None):
                day_strs.append('{:0>2d}'.format(args.day))
            else:
                day_strs = os.listdir('consensuses/consensuses-{}-{}/'.format(year, month_str))
            for day_str in day_strs:
                hms_strs = []
                if (args.hour is not None):
                    hms_strs.append('{:0>2d}-00-00'.format(args.hour))
                else:
                     filenames = os.listdir('consensuses/consensuses-{}-{}/{}/'.format(year, month_str, day_str))
                     for filename in filenames:
                         filename_parts = filename.split('-')
                         # include minute-second because exist minute-second != 00-00
                         hms_strs.append('{}-{}-{}'.format(filename_parts[3], filename_parts[4],
                            filename_parts[5]))
                for hms_str in hms_strs:
                    filename = 'consensuses/consensuses-{}-{}/{}/{}-{}-{}-{}-consensus'.format(year, month_str, day_str, year, month_str, day_str, hms_str)
                    if (os.path.isfile(filename)):
                        bw_data = process_consensus(filename)
                        month_bw_data['{}-{}-{}-{}'.format(year, month_str,
                            day_str, hms_str)] = bw_data
                    else:
                        print('Consensus does not exist: {}'.format(filename))
            # write output for month to JSON file
            output_filename = 'consensuses-bwdata-{}-{}'.format(year,
                month_str)
            if (args.day is not None):
                output_filename = '{}-{}'.format(output_filename, args.day)
            if (args.hour is not None):
                output_filename = '{}-{}h'.format(output_filename, args.hour)
            output_filename = '{}.json'.format(output_filename)
            with open(output_filename, 'w') as f:
                json.dump(month_bw_data, f)
            month += 1
        month = 1

#    pathnames.sort()
#    for pathname in pathnames:
#        filename = os.path.basename(pathname)
#        if (filename[0] == '.'):
#            continue
#    for pathname in pathnames:
#        process_consensus(pathname)
