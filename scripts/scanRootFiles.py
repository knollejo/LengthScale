from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/LengthScale')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Scan over ROOT files to find those '+ \
                            'belonging to a lumisection interval.')
    parser.add_argument('-b', action='store_true', help='enable batch mode')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016', \
                        '2015ReRecoJan2017', '2016ReRecoJan2017'], \
                        help='specify data-taking period and reconstruction')
    parser.add_argument('-mini', dest='actions', action='append_const', \
                        const='minitrees', help='look for minitrees')
    parser.add_argument('-full', dest='actions', action='append_const', \
                        const='fulltrees', help='look for full trees')
    args = parser.parse_args()

    from importlib import import_module
    from lsctools import config, prepare
    getattr(config, 'PCC'+args.dataset)()
    for action in args.actions:
        prepare.findRootFiles(action)

if __name__ == '__main__':
    main()
