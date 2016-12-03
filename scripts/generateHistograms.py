from sys import path as __SYSPATH__
__SYSPATH__.append('..')

from argparse import ArgumentParser
from importlib import import_module
from lsctools import config, gather, fit, plot

def main():
    parser = ArgumentParser()
    parser.add_argument('-b', action='store_true')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016'])
    parser.add_argument('-X1', dest='scans', action='append_const', const='X1')
    parser.add_argument('-Y1', dest='scans', action='append_const', const='Y1')
    parser.add_argument('-X2', dest='scans', action='append_const', const='X2')
    parser.add_argument('-gather', action='store_true')
    parser.add_argument('-fit', action='append', nargs='?', const='F')
    parser.add_argument('-plot', action='store_true')
    parser.add_argument('-nCluster', dest='actions', action='append_const', \
                        const='numberClusters')
    parser.add_argument('-nVtx', dest='actions', action='append_const', \
                        const='numberVertices')
    parser.add_argument('-vtxPos', dest='actions', action='append_const', \
                        const='vertexPosition')
    args = parser.parse_args()
    getattr(config, 'PCC'+args.dataset)()
    if args.gather:
        for action in args.actions:
            for scan in args.scans:
                getattr(gather, action)(scan)
    if args.fit:
        for action in args.actions:
            for scan in args.scans:
                for method in args.fit:
                    getattr(fit, action)(scan, fitmethod=method)
    if args.plot:
        for action in args.actions:
            for scan in args.scans:
                if args.fit:
                    for method in args.fit:
                        getattr(plot, action+'PerBxStep')(scan, fit=method)
                else:
                    getattr(plot, action+'PerBxStep')(scan)

if __name__ == '__main__':
    main()
