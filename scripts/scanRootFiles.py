from sys import path as __SYSPATH__
__SYSPATH__.append('..')

from argparse import ArgumentParser
from importlib import import_module
from lsctools import config, prepare

def main():
    parser = ArgumentParser()
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016'])
    parser.add_argument('-mini', dest='actions', action='append_const', \
                        const='minitrees')
    parser.add_argument('-full', dest='actions', action='append_const', \
                        const='fulltrees')
    args = parser.parse_args()
    getattr(config, 'PCC'+args.dataset)()
    for action in args.actions:
        prepare.findRootFiles(action)

if __name__ == '__main__':
    main()
