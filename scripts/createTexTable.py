from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/lsc')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
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
    parser.add_argument('-o', dest='output', required=True, nargs=1, \
                        help='specify output file name')
    args = parser.parse_args()
    
    from importlib import import_module
    from lsctools import config, extract
    getattr(config, 'PCC'+args.dataset)()
    table = getattr(extract, args.action+'TexTable')(args.scan, \
                    fitted=args.fitted, combined=args.combined)
    print '<<< Save to file:', args.output
    f = open(args.output, 'w')
    f.write(table)
    f.close()
