from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('..')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Generate histograms of data stored '+ \
                            'in selected ROOT files.')
    parser.add_argument('-b', action='store_true', help='enable batch mode')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016'], \
                        help='specify data-taking period and reconstruction')
    parser.add_argument('-X1', dest='scans', action='append_const', const='X1', \
                        help='apply to LSC scan X1')
    parser.add_argument('-Y1', dest='scans', action='append_const', const='Y1', \
                        help='apply to LSC scan Y1')
    parser.add_argument('-X2', dest='scans', action='append_const', const='X2', \
                        help='apply to LSC scan X2')
    parser.add_argument('-gather', action='store_true', help='extract data '+ \
                        'from ROOT file')
    parser.add_argument('-combine', action='store_true', help='combine data '+ \
                        'of all bunch crossings')
    parser.add_argument('-fit', action='append', nargs='?', const='F', \
                        help='fit histogram, give L for log-likelihood fit')
    parser.add_argument('-plot', action='store_true', help='save histograms '+ \
                        'to PDF')
    parser.add_argument('-nCluster', dest='actions', action='append_const', \
                        const='numberClusters', help='evaluate number of '+ \
                        'pixel clusters')
    parser.add_argument('-nVtx', dest='actions', action='append_const', \
                        const='numberVertices', help='evaluate number of '+ \
                        'reconstructed vertices')
    parser.add_argument('-vtxPos', dest='actions', action='append_const', \
                        const='vertexPosition', help='evaluate transverse '+ \
                        'position of reconstructed vertices')
    args = parser.parse_args()
    
    from importlib import import_module
    from lsctools import config, gather, fit, plot
    getattr(config, 'PCC'+args.dataset)()
    if args.gather:
        for action in args.actions:
            for scan in args.scans:
                getattr(gather, action)(scan)
                if args.combine:
                    getattr(gather, action)(scan, combine=True)
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
