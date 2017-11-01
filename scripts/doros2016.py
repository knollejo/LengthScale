from sys import path as __SYSPATH__, argv as __ARGV__
__SYSPATH__.append('/afs/cern.ch/user/j/joknolle/LengthScale')
__ARGV__.append('-b')

from lsctools import config
config.PCC2016ReRecoJan2017()
config.VdM2016DorosPositions()
scans = ('X1', 'Y1')

run = {
    'prepare': False,
    'gather': False,
    'fit': False,
    'analyze': True,
    'plot': True
}

# Find ROOT files (needs to be executed only once)
if run['prepare']:
    from lsctools import prepare
    prepare.findRootFiles('fulltrees')
    prepare.findRootFiles('minitrees')

# Prepare data from ROOT files
if run['gather']:
    from lsctools import gather
    for scan in scans:
        gather.vertexPositionPerBxStep(scan, alternative=True, all=True)
        gather.numberClustersPerBxStep(scan, alternative=True, all=True)

# Fit data at each scan step
if run['fit']:
    from lsctools import fit
    for scan in scans:
        fit.vertexPosition(scan, fitmethod='L', alternative=True, all=True)

# Analyze full scan
if run['analyze']:
    from lsctools import analyze
    for scan in scans:
        analyze.vertexPosition(scan, fitted='L', alternative=True, all=True)
        analyze.numberClusters(scan, alternative=True, all=True)

# Plot all results
if run['plot']:
    from lsctools import plot
    for scan in scans:
        plot.vertexPositionPerBxStep(scan, fit='L', alternative=True, all=True)
        plot.numberClustersPerBxStep(scan, alternative=True, all=True)
        plot.vertexPositionPerDirectionBx(scan, fitted='L', alternative=True, all=True)
        plot.numberClustersPerDirectionBx(scan, alternative=True, all=True)
