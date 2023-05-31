import pycurl
import argparse


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Download some Tor consensuses')
    parser.add_argument('year_start', type=int,
                    help='start year (integer)')
    parser.add_argument('year_end', type=int,
                    help='end year (integer)')
    parser.add_argument('month_start', type=int,
                    help='start month (integer 1 to 12)')
    parser.add_argument('month_end', type=int,
                    help='end month (integer 1 to 12)')
    args = parser.parse_args()

    for year in range(args.year_start, args.year_end+1):
        for month in range(args.month_start, args.month_end+1):
            filename = 'consensuses-{}-{:0>2d}.tar.xz'.format(year, month)
            file = open(filename,'wb')
            crl = pycurl.Curl()
            crl.setopt(crl.URL, 'https://collector.torproject.org/archive/relay-descriptors/consensuses/{}'.format(filename))
            crl.setopt(crl.WRITEDATA, file)
            print('Downloading {}'.format(filename))
            crl.perform()
            crl.close()
            print('Finished downloading {}'.format(filename))
