from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/LengthScale')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Calculate the average event rate '+ \
                            'of specific lumisections in specific files.')
    parser.add_argument('-b', action='store_true', help='enable batch mode')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016', \
                        '2015ReRecoJan2017', '2016ReRecoJan2017'], \
                        help='specify data-taking period and reconstruction')
    parser.add_argument('-n', nargs=1, default=1, type=int, help='Specify '+ \
                        'the number of ZeroBias datasets to be included')
    parser.add_argument('-ls', nargs=2, type=int, help='Specify a range '+ \
                        'in lumisections')
    parser.add_argument('-files', nargs=2, type=int, help='Specify a range '+ \
                        'in file numbers')
    args = parser.parse_args()

from importlib import import_module
from lsctools import config
from lsctools.config import options as O, EOSPATH as eos
from os import listdir
from ROOT import TChain, TH1I
getattr(config, 'PCC'+args.dataset)()
O['fulltrees'] = O['fulltrees'][:args.n]
chain = TChain(O['treename']['fulltrees'])
for directory in O['fulltrees']:
    print '<<< Enter directory', directory
    for filename in listdir(eos+directory+'/'):
        for i in range(args.files[0], args.files[1]+1):
            if not filename.endswith(str(i)+'.root'):
                continue
            chain.Add(eos+directory+'/'+filename)
histo = TH1I('hist', '', 1001, -0.5, 1000.5)
cond = 'LS >= ' + str(args.ls[0]) + ' && LS <= ' + str(args.ls[1])
chain.Draw('nCluster>>hist', cond, 'goff')
print histo.GetMean(), '+-', histo.GetMeanError()
