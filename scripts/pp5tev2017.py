from sys import path as __SYSPATH__, argv as __ARGV__
from os.path import dirname
__SYSPATH__.append(dirname(__file__)+'/..')
__ARGV__.append('-b')

from lsctools import config
config.PCC()
config.options['scans'] = ['X1', 'Y1']
config.options['runs'] = {'X1': 306553, 'Y1': 306553}
config.options['fill'] = 6381
config.options['lumisections'] = {'X1': [496, 535], 'Y1': [550, 590]}
config.options['crossings'] = [183, 1536, 2366, 3295, 3309]
config.options['plotsig'] = 'Fill 6381 (2017, 5 TeV)'
if True: #ReReco
    config.options['fulltrees'] = [
        '/comm_luminosity/PCC/ForLumiComputation/2017/VdMFills/6381/'+
        'HIZeroBias'+str(i)+'/crab_CMSSW_9_4_4_HIZeroBias'+str(i)+
        '_splitPerBXTrue/180'+time+'/0000' for (i, time) in enumerate([
            '318_112731', '318_112757', '327_100708', '319_101305',
            '327_100801', '327_100827', '327_100853', '314_121031',
            '415_202559', '316_140727', '318_112825',
        ], start=1)
    ]
    config.options['minitrees'] = []
    config.options['dataset'] = ['data5tev2017', '5TeV 2017']
else: #Prompt
    config.options['fulltrees'] = [
        '/comm_luminosity/PCC/ForLumiComputation/2017/VdMFills/6381/'+
        'HIZeroBias'+str(i)+'/crab_CMSSW_9_2_6_HIZeroBias'+str(i)+
        '_splitPerBXTrue/180305_143'+str(time)+'/0000' for (i, time)
        in enumerate([159, 319, 338, 404, 425, 450, 517, 538, 557,
        218, 236, 259], start=1)
    ]
    config.options['minitrees'] = []
    config.options['dataset'] = ['prompt5tev2017', 'Prompt 5TeV 2017']
config.options['begin'] = {
    'X1': [1510482174, 1510482266, 1510482358, 1510482449, 1510482543,
           1510482636, 1510482729, 1510482821, 1510482913, 1510483004],
    'Y1': [1510483439, 1510483530, 1510483624, 1510483715, 1510483807,
           1510483902, 1510483994, 1510484085, 1510484177, 1510484269],
}
config.options['end'] = {
    'X1': [1510482242, 1510482334, 1510482426, 1510482519, 1510482611,
           1510482706, 1510482798, 1510482889, 1510482981, 1510483074],
    'Y1': [1510483508, 1510483600, 1510483692, 1510483784, 1510483876,
           1510483970, 1510484062, 1510484154, 1510484246, 1510484338],
}
config.options['LS'] = {
    'X1': [[497, 498], [501, 502], [505, 506], [509, 510], [513, 514],
           [517, 518], [521, 522], [525, 526], [529, 530], [533, 534]],
    'Y1': [[551, 552], [555, 556], [559, 560], [563, 564], [567, 568],
           [571, 572], [575, 576], [579, 580], [583, 584], [587, 588]],
}
posBeam1 = [-159.489, -95.693, -31.898, 31.898, 95.693,
            185.007, 121.211, 57.416, -6.380, -70.175]
posBeam2 = [-70.175, -6.380, 57.416, 121.211, 185.077,
            95.693, 31.898, -31.898, -95.693, -159.489]
config.options['nominalPos'] = dict(zip(config.options['scans'], [[
    (a+b)/2. for a,b in zip(posBeam1, posBeam2)
] for scanname in config.options['scans']]))
config.options['nominalDif'] = dict(zip(config.options['scans'], [[
    b-a for a,b in zip(posBeam1, posBeam2)
] for scanname in config.options['scans']]))

run = {
    'prepare': False,
    'gather': False,
    'fit': True,
    'analyze': True,
    'plot': True,
}
scans = ('X1', 'Y1')

# Find ROOT files (needs to be executed only once)
if run['prepare']:
    from lsctools import prepare
    prepare.findRootFiles('fulltrees')

# Prepare data from ROOT files
if run['gather']:
    from lsctools import gather
    for scan in scans:
        gather.vertexPositionPerBxStep(scan, alternative=False, all=True)
        gather.vertexPositionPerBxStep(scan, alternative=True, all=True)

# Fit data at each scan step
if run['fit']:
    from lsctools import fit
    for scan in scans:
        fit.vertexPosition(scan, fitmethod='L', alternative=False, all=True)
        # fit.vertexPosition(scan, fitmethod='F', alternative=False, all=True)
        fit.vertexPosition(scan, fitmethod='L', alternative=True, all=True)
        # fit.vertexPosition(scan, fitmethod='F', alternative=True, all=True)

# Analyze full scan
if run['analyze']:
    from lsctools import analyze
    for scan in scans:
        analyze.vertexPosition(scan, fitted='L', alternative=False, all=True)
        # analyze.vertexPosition(scan, fitted='F', alternative=False, all=True)
        analyze.vertexPosition(scan, alternative=False, all=True)
        analyze.vertexPosition(scan, fitted='L', alternative=True, all=True)
        # analyze.vertexPosition(scan, fitted='F', alternative=True, all=True)
        analyze.vertexPosition(scan, alternative=True, all=True)

# Plot all results
if run['plot']:
    from lsctools import plot
    for scan in scans:
        # plot.vertexPositionPerBxStep(scan, fit='L', alternative=False, all=True)
        # plot.vertexPositionPerBxStep(scan, fit='L', alternative=True, all=True)
        plot.vertexPositionPerDirectionBx(scan, fitted='L', alternative=False, all=True, final='wip')
        # plot.vertexPositionPerDirectionBx(scan, fitted='F', alternative=False, all=True, final='wip')
        plot.vertexPositionPerDirectionBx(scan, fitted='L', alternative=True, all=True, final='wip')
        # plot.vertexPositionPerDirectionBx(scan, fitted='F', alternative=True, all=True, final='wip')
        plot.vertexPositionPerDirectionBx(scan, alternative=False, all=True, final='wip')
        plot.vertexPositionPerDirectionBx(scan, alternative=True, all=True, final='wip')
