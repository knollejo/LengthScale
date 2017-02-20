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
    parser.add_argument('-ls', nargs=2, type=int, help='Specify a range '+ \
                        'in lumisections')
    parser.add_argument('-files', nargs=2, type=int, help='Specify a range '+ \
                        'in file numbers')
    parser.add_argument('-run', nargs=1, required=True, type=int, \
                        help='Specify the run number for the selection of '+ \
                        'the lumisections')
    args = parser.parse_args()

    from importlib import import_module
    from lsctools import config
    from lsctools.config import options as O, EOSPATH as eos
    from os import listdir
    from ROOT import TChain, TH1I
    getattr(config, 'PCC'+args.dataset)()
    chain = TChain(O['treename']['minitrees'])
    for directory in O['minitrees']:
        print '<<< Enter directory', directory
        for filename in listdir(eos+directory+'/'):
            for i in range(args.files[0], args.files[1]+1):
                if not filename.endswith(str(i)+'.root'):
                    continue
                chain.Add(eos+directory+'/'+filename)
    histo = TH1I('hist', '', 1001, -0.5, 1000.5)
    cond = 'run == ' + str(args.run[0]) + ' && LS >= ' + str(args.ls[0]) + \
           ' && LS <= ' + str(args.ls[1])
    chain.Draw('nCluster>>hist', cond, 'goff')
    print histo.GetMean(), '+-', histo.GetMeanError()

if __name__ == '__main__':
    main()
