from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/lsc')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Generate histograms of data stored '+ \
                            'in selected ROOT files.')
    parser.add_argument('-b', action='store_true', help='enable batch mode')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016', \
                        '2015ReRecoJan2017', '2016ReRecoJan2017'], \
                        help='specify data-taking period and reconstruction')
    parser.add_argument('-X1', dest='scans', action='append_const', const='X1', \
                        help='apply to LSC scan X1')
    parser.add_argument('-Y1', dest='scans', action='append_const', const='Y1', \
                        help='apply to LSC scan Y1')
    parser.add_argument('-X2', dest='scans', action='append_const', const='X2', \
                        help='apply to LSC scan X2')
    parser.add_argument('-Y2', dest='scans', action='append_const', const='Y2', \
                        help='apply to LSC scan Y2')
    parser.add_argument('-gather', action='store_true', help='extract data '+ \
                        'from ROOT file')
    parser.add_argument('-combine', action='store_true', help='combine data '+ \
                        'of all bunch crossings')
    parser.add_argument('-all', action='store_true', help='only use data of '+ \
                        'all bunch crossings at once')
    parser.add_argument('-combined', action='store_true', help='use combined '+ \
                        'data of all bunch crossings')
    parser.add_argument('-fit', action='append', nargs='?', const='F', \
                        help='fit histogram, give L for log-likelihood fit, '+ \
                        'add R for restricted range')
    parser.add_argument('-fitted', action='append', nargs='?', const='F', \
                        help='use fitted histograms, give F for standard fit '+ \
                        'or L for log-likelihood fit, add R for fits with '+ \
                        'restricted range')
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
    parser.add_argument('-perLs', action='store_true', help='use only full '+ \
                        'lumisections', dest='alternative')
    args = parser.parse_args()

    from importlib import import_module
    from lsctools import config, gather, fit, plot
    getattr(config, 'PCC'+args.dataset)()
    allbx = bool(args.all)
    if args.gather:
        for action in args.actions:
            for scan in args.scans:
                if args.alternative:
                    getattr(gather, action+'PerBxStep')(scan, alternative=True, \
                            all=allbx)
                else:
                    getattr(gather, action+'PerBxStep')(scan, all=allbx)
                if args.combine:
                    if args.alternative:
                        getattr(gather, action+'PerBxStep')(scan, combine=True, \
                                alternative=True, all=allbx)
                    else:
                        getattr(gather, action+'PerBxStep')(scan, combine=True, \
                                all=allbx)
    if args.combine and not args.gather:
        for action in args.actions:
            for scan in args.scans:
                if args.alternative:
                    getattr(gather, action+'PerBxStep')(scan, combine=True, \
                            alternative=True, all=allbx)
                else:
                    getattr(gather, action+'PerBxStep')(scan, combine=True, \
                            all=allbx)
    if args.combine:
        args.combined = True
    if args.fit:
        for action in args.actions:
            for scan in args.scans:
                for method in args.fit:
                    if args.alternative:
                        getattr(fit, action)(scan, fitmethod=method, all=bxall, \
                                combine=args.combined, alternative = True)
                    else:
                        getattr(fit, action)(scan, fitmethod=method, all=bxall, \
                                combine=args.combined)
    if args.fit:
        args.fitted = args.fit
    if args.plot:
        for action in args.actions:
            for scan in args.scans:
                if args.fitted:
                    for method in args.fitted:
                        if args.alternative:
                            getattr(plot, action+'PerBxStep')(scan, fit=method, \
                                    combine=args.combined, alternative=True, \
                                    all=bxall)
                        else:
                            getattr(plot, action+'PerBxStep')(scan, fit=method, \
                                    combine=args.combined, all=bxall)
                else:
                    getattr(plot, action+'PerBxStep')(scan, \
                            combine=args.combined, all=bxall)

if __name__ == '__main__':
    main()
