from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/lsc')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Store results from plots to a tex '+ \
                            'table')
    parser.add_argument('-b', action='store_true', help='enable batch mode')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016'], \
                        help='specify data-taking period and reconstruction')
    parser.add_argument('-X1', dest='scan', action='store_const', const='X1', \
                        help='use LSC scan X1')
    parser.add_argument('-Y1', dest='scan', action='store_const', const='Y1', \
                        help='use LSC scan Y1')
    parser.add_argument('-X2', dest='scan', action='store_const', const='X2', \
                        help='use LSC scan X2')
    parser.add_argument('-combined', action='store_true', help='use '+ \
                        'combined data of all bunch crossings')
    parser.add_argument('-fitted', nargs=1, action='store', default='', \
                        help='use fit results')
    parser.add_argument('-nCluster', dest='action', action='store_const', \
                        const='numberClusters', help='use number of '+ \
                        'pixel clusters')
    parser.add_argument('-nVtx', dest='action', action='store_const', \
                        const='numberVertices', help='use number of '+ \
                        'reconstructed vertices')
    parser.add_argument('-vtxPos', dest='action', action='store_const', \
                        const='vertexPosition', help='use transverse '+ \
                        'position of reconstructed vertices')
    args = parser.parse_args()

    from importlib import import_module
    from lsctools import config, extract
    getattr(config, 'PCC'+args.dataset)()
    table = getattr(extract, args.action+'TexTable')(args.scan, \
                    fitted=args.fitted[0], combined=args.combined)
    from lsctools.tools import plotName, plotDir
    name = args.scan + '_' + args.action + args.fitted[0] + '_collected'
    filename = plotDir() + '/' + plotName(name) + '.tex'
    print '<<< Save to file:', filename
    f = open(filename, 'w')
    f.write(table)
    f.close()

if __name__ == '__main__':
    main()
