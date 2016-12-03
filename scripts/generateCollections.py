from sys import path as __SYSPATH__
__SYSPATH__.append('..')

from argparse import ArgumentParser
from importlib import import_module
from lsctools import config, plot, analyze

def main():
    parser = ArgumentParser()
    parser.add_argument('-b', action='store_true')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016'])
    parser.add_argument('-X1', dest='scans', action='append_const', const='X1')
    parser.add_argument('-Y1', dest='scans', action='append_const', const='Y1')
    parser.add_argument('-X2', dest='scans', action='append_const', const='X2')
    parser.add_argument('-analyze', action='store_true')
    parser.add_argument('-plot', action='store_true')
    parser.add_argument('-fitted', action='append', nargs=1)
    parser.add_argument('-nCluster', dest='actions', action='append_const', \
                        const='numberClusters')
    parser.add_argument('-nVtx', dest='actions', action='append_const', \
                        const='numberVertices')
    parser.add_argument('-vtxPos', dest='actions', action='append_const', \
                        const='vertexPosition')
    args = parser.parse_args()
    getattr(config, 'PCC'+args.dataset)()
    if args.analyze:
        for action in args.actions:
            for scan in args.scans:
                if args.fitted:
                    for fitted in args.fitted:
                        getattr(analyze, action)(scan, fitted[0])
                else:
                    getattr(analyze, action)(scan)
    if args.plot:
        for action in args.actions:
            for scan in args.scans:
                if args.fitted:
                    for fitted in args.fitted:
                        getattr(plot, action+'PerDirectionBx')(scan, fitted[0])
                else:
                    getattr(plot, action+'PerDirectionBx')(scan)

if __name__ == '__main__':
    main()
