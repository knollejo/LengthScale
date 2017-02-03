from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/lsc')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
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
    parser.add_argument('-combined', action='store_true', help='use '+ \
                        'combined data of all bunch crossings')
    parser.add_argument('-all', action='store_true', help='only use data of '+ \
                        'all bunch crossings at once')
    parser.add_argument('-analyze', action='store_true', help='collect mean '+ \
                        'and mean error from histograms')
    parser.add_argument('-plot', action='store_true', help='save plot to PDF')
    parser.add_argument('-truncate', action='store_true', help='compute '+ \
                        'truncated mean')
    parser.add_argument('-truncated', action='append_const', dest='fitted', \
                        const='T', help='use truncated mean')
    parser.add_argument('-fitted', action='append', nargs=1, help='use fit '+ \
                        'parameters instead of mean, mean error, give F for '+ \
                        'standard fit or L for log-likelihood fit, add R for'+ \
                        'fits with restricted range')
    parser.add_argument('-nCluster', dest='actions', action='append_const', \
                        const='numberClusters', help='evaluate number of '+ \
                        'pixel clusters')
    parser.add_argument('-nVtx', dest='actions', action='append_const', \
                        const='numberVertices', help='evaluate number of '+ \
                        'reconstructed vertices')
    parser.add_argument('-vtxPos', dest='actions', action='append_const', \
                        const='vertexPosition', help='evaluate transverse '+ \
                        'position of reconstructed vertices')
    parser.add_argument('-vtxPosSig', dest='actions', action='append_const', \
                        const='vertexPositionSigma', help='evaluate sigma '+ \
                        'of transverse position of reconstructed vertices')
    parser.add_argument('-perLs', action='store_true', help='use only full '+ \
                        'lumisections', dest='alternative')
    args = parser.parse_args()

    from importlib import import_module
    from lsctools import config, plot, analyze
    getattr(config, 'PCC'+args.dataset)()
    allbx = bool(args.all)
    if args.analyze:
        for action in args.actions:
            for scan in args.scans:
                if args.truncate:
                    getattr(analyze, action)(scan, truncated=True, \
                            combine=args.combined, all=allbx)
                elif args.fitted:
                    for fitted in args.fitted:
                        if args.alternative:
                            getattr(analyze, action)(scan, fitted=fitted[0], \
                                    combine=args.combined, alternative=True,
                                    all=allbx)
                        else:
                            getattr(analyze, action)(scan, fitted=fitted[0], \
                                    combine=args.combined, all=allbx)
                else:
                    if args.alternative:
                        getattr(analyze, action)(scan, combine=args.combined, \
                                alternative=True, all=allbx)
                    else:
                        getattr(analyze, action)(scan, combine=args.combined, \
                                all=allbx)
    if args.truncate:
        if not args.fitted:
            args.fitted = ['T']
        elif not 'T' in args.fitted:
            args.fitted.append('T')
    if args.plot:
        for action in args.actions:
            for scan in args.scans:
                if args.fitted:
                    for fitted in args.fitted:
                        if args.alternative:
                            getattr(plot, action+'PerDirectionBx')(scan, \
                                    fitted=fitted[0], combine=args.combined, \
                                    alternative=True, all=allbx)
                        else:
                            getattr(plot, action+'PerDirectionBx')(scan, \
                                    fitted=fitted[0], combine=args.combined, \
                                    all=allbx)
                else:
                    if args.alternative:
                        getattr(plot, action+'PerDirectionBx')(scan, \
                                combine=args.combined, alternative=True, \
                                all=allbx)
                    else:
                        getattr(plot, action+'PerDirectionBx')(scan, \
                                combine=args.combined, all=allbx)

if __name__ == '__main__':
    main()
