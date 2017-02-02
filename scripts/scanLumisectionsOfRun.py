from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/lsc')
__ARGV__.append('-b')

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Scan over ROOT files to find the '+ \
                            'lumisections belonging to a specific run.')
    parser.add_argument('-b', action='store_true', help='enable batch mode')
    parser.add_argument('--dataset', required=True, choices=['PromptReco2015', \
                        'ReRecoOct2015', 'ReRecoDec2015', 'PromptReco2016', \
                        '2015ReRecoJan2017', '2016ReRecoJan2017'], \
                        help='specify data-taking period and reconstruction')
    parser.add_argument('-n', nargs=1, default=1, type=int, help='Specify '+ \
                        'the number of ZeroBias datasets to be included')
    parser.add_argument('-run', nargs=1, required=True, type=int, \
                        help='Specify the run number for the selection of '+ \
                        'the lumisections')
    parser.add_argument('-X', dest='coords', action='append_const', \
                        const='vtx_x', help='look for vtx_x')
    parser.add_argument('-Y', dest='coords', action='append_const', \
                        const='vtx_y', help='look for vtx_y')
    parser.add_argument('-noscan', action='store_const', const=True, \
                        default=False, help='don\'t repeat the scan of the '+ \
                        'ROOT files, just do the plotting')
    args = parser.parse_args()

    from importlib import import_module
    from lsctools import config
    from lsctools.config import options as O, EOSPATH as eos
    from lsctools.tools import openRootFileU, closeRootFile, writeFiles, \
                               plotName, plotTitle, loadFiles
    from lsctools.prepare import loopOverRootFiles
    from ROOT import TChain, TObject, TProfile
    getattr(config, 'PCC'+args.dataset)()
    O['fulltrees'] = O['fulltrees'][:args.n]
    run =args.run[0]
    files = []
    if args.noscan:
        files = loadFiles('fulltrees_'+str(run))
    else:
        def action(tree, filename):
            condition = 'run == ' + str(run)
            if tree.GetEntries(condition) > 0:
                files.append(filename)
                print '<<< Found file:', filename
        loopOverRootFiles(action, 'fulltrees')
        writeFiles(files, 'fulltrees_'+str(run))
    chain = TChain(O['treename']['fulltrees'])
    for filename in files:
        chain.Add(eos+filename)
    name = 'vtxPos_perLS'
    title = 'run' + str(run) + '_perLS'
    f = openRootFileU(name)
    for coord in args.coords:
        print '<<< Analyze coordinate', coord
        histname = plotName(coord+'_'+title, timestamp=False)
        histtitl = plotTitle()
        hist = TProfile(histname, histtitl, 250, -0.3, 0.3)
        chain.Draw(coord+':LS>>'+histname, 'run == ' + str(run), 'goff')
        hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

if __name__ == '__main__':
    main()
