from sys import path as __SYSPATH__, argv as __ARGV__
from os.path import dirname
__SYSPATH__.append(dirname(__file__)+'/..')
__ARGV__.append('-b')

from lsctools import config
config.PCC()
config.options['vtxisgood'] = 'goodVertex'
config.options['scans'] = ['X1', 'Y1']
config.options['runs'] = {'X1': 263234, 'Y1': 263234}
config.options['fill'] = 4689
config.options['lumisections'] = {'X1': [336, 367], 'Y1': [302, 334]}
config.options['crossings'] = []
config.options['plotsig'] = 'Fill 4689 (2015, PbPb)'
config.options['fulltrees'] = [
    '/comm_luminosity/PCC/ForLumiComputation/2015/NormalFills/4689/'+
    'HIMinimumBias'+str(i)+'/crab_CMSSW_7_5_8_patch4_HIMinimumBias'+
    str(i)+'_splitPerBXFalse/181003_1'+str(time)+'/0000' for (i, time) in
    [(1, 92804), (3, 91128), (4, 91201), (5, 93806)]
]
config.options['minitrees'] = []
config.options['dataset'] = ['hidata15', 'Heavy Ion Data 2015']
config.options['begin'] = {
    'X1': [1449157563, 1449157643, 1449157733, 1449157825,
           1449157919, 1449157991, 1449158073, 1449158175],
    'Y1': [1449156790, 1449156870, 1449156952, 1449157034,
           1449157144, 1449157246, 1449157336, 1449157414],
}
config.options['end'] = {
    'X1': [1449157623, 1449157713, 1449157810, 1449157890,
           1449157989, 1449158071, 1449158153, 1449158245],
    'Y1': [1449156850, 1449156942, 1449157034, 1449157116,
           1449157226, 1449157316, 1449157395, 1449157472],
}
config.options['LS'] = {
    'X1': [[338], [342], [346], [349],
           [353], [357], [361], [364]],
    'Y1': [[305], [309], [312], [316],
           [320], [324], [328], [331]],
}
posBeam1 = [-63.286, -31.643, 0.0, 31.643,
            63.286, 31.643, 0.0, -31.643]
posBeam2 = [-31.643, 0.0, 31.643, 63.286,
            31.643, 0.0, -31.643, -63.286]
config.options['nominalPos'] = dict(zip(config.options['scans'], [[
    (a+b)/2. for a,b in zip(posBeam1, posBeam2)
] for scanname in config.options['scans']]))
config.options['nominalDif'] = dict(zip(config.options['scans'], [[
    b-a for a,b in zip(posBeam1, posBeam2)
] for scanname in config.options['scans']]))

run = {
    'prepare': False,
    'gather': True,
    'fit': True,
    'analyze': True,
    'plot': True,
}
scans = ('X1', 'Y1')

# Find ROOT files (needs to be executed only once)
if run['prepare']:
    from lsctools import prepare, tools
    files = dict([(scan, []) for scan in config.options['scans']])
    def action(tree, filename):
        for scan in config.options['scans']:
            condition = 'run == ' + str(config.options['runs'][scan]) + \
                        ' && LS >= ' + str(config.options['lumisections'][scan][0]) + \
                        ' && LS <= ' + str(config.options['lumisections'][scan][1]) + \
                        ' && vtx_y'
            if tree.GetEntries(condition) > 0:
                files[scan].append(filename)
                print '<<< Found file:', filename
    prepare.loopOverRootFiles(action, 'fulltrees')
    tools.writeFiles(files, 'fulltrees')

# Prepare data from ROOT files
if run['gather']:
    from lsctools import gather
    for scan in scans:
        # gather.vertexPositionPerBxStep(scan, alternative=False, all=True)
        gather.vertexPositionPerBxStep(scan, alternative=True, all=True)

# Fit data at each scan step
if run['fit']:
    from lsctools import fit
    for scan in scans:
        # fit.vertexPosition(scan, fitmethod='L', alternative=False, all=True)
        fit.vertexPosition(scan, fitmethod='L', alternative=True, all=True)

# Analyze full scan
if run['analyze']:
    from lsctools import analyze
    for scan in scans:
        # analyze.vertexPosition(scan, fitted='L', alternative=False, all=True)
        # analyze.vertexPosition(scan, alternative=False, all=True)
        analyze.vertexPosition(scan, fitted='L', alternative=True, all=True)
        analyze.vertexPosition(scan, alternative=True, all=True)

# Plot all results
if run['plot']:
    from lsctools import plot
    for scan in scans:
        # plot.vertexPositionPerBxStep(scan, fit='L', alternative=False, all=True)
        plot.vertexPositionPerBxStep(scan, fit='L', alternative=True, all=True)
        # plot.vertexPositionPerDirectionBx(scan, fitted='L', alternative=False, all=True, final='wip')
        plot.vertexPositionPerDirectionBx(scan, fitted='L', alternative=True, all=True, final='wip')
        # plot.vertexPositionPerDirectionBx(scan, alternative=False, all=True, final='wip')
        plot.vertexPositionPerDirectionBx(scan, alternative=True, all=True, final='wip')
