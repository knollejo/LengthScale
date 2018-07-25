from sys import path as __SYSPATH__, argv as __ARGV__
from os.path import dirname
__SYSPATH__.append(dirname(__file__)+'/..')
__ARGV__.append('-b')

from lsctools import config
config.PCC()
config.options['scans'] = ['X1', 'Y1']
config.options['runs'] = {'X1': 319019, 'Y1': 319019}
config.options['fill'] = 6868
config.options['lumisections'] = {'X1': [326, 385], 'Y1': [386, 445]}
config.options['crossings'] = [265, 865, 1780, 2192, 3380]
config.options['plotsig'] = 'Fill 6868 (2018, 13 TeV)'
config.options['fulltrees'] = [
    '/comm_luminosity/PCC/ForLumiComputation/2018/NormalFills/'+
    '6847_And_6854_And_6868/ZeroBias'+str(i)+'/crab_CMSSW_10_1_7_ZeroBias'+
    str(i)+'_splitPerBXTrue/180716_1'+str(time)+'/0000' for (i, time) in
    enumerate([85816, 85835, 85857, 85923, 85943, 90006, 90034, 90100], start=1)
]
config.options['minitrees'] = [
    s+'/minituples_v1' for s in config.options['fulltrees']
]
config.options['dataset'] = ['promptreco18', 'Prompt Reco 2018']
config.options['begin'] = {
    'X1': [1530413319, 1530413436, 1530413552, 1530413667, 1530413784,
           1530413915, 1530414041, 1530414157, 1530414274, 1530414389],
    'Y1': [1530414711, 1530414829, 1530414947, 1530415063, 1530415181,
           1530415314, 1530415432, 1530415548, 1530415666, 1530415784],
}
config.options['end'] = {
    'X1': [1530413388, 1530413504, 1530413621, 1530413736, 1530413853,
           1530413984, 1530414110, 1530414225, 1530414342, 1530414457],
    'Y1': [1530414779, 1530414897, 1530415015, 1530415132, 1530415250,
           1530415382, 1530415500, 1530415618, 1530415735, 1530415853],
}
config.options['LS'] = {
    'X1': [[332], [337], [342], [347], [352],
           [357], [363], [368], [373], [378]],
    'Y1': [[392], [397], [402], [407], [412],
           [418], [423], [428], [433], [438]],
}
posBeam1 = [-246.048, -147.629, -49.2096, 49.2096, 147.629,
            285.415, 186.996, 88.5772, -9.84191, -108.261]
posBeam2 = [-108.261, -9.84191, -88.5772, 186.996, 285.415,
            147.629, 49.2096, -49.2096, -147.629, -246.048]
config.options['nominalPos'] = dict(zip(config.options['scans'], [[
    (a+b)/2. for a,b in zip(posBeam1, posBeam2)
] for scanname in config.options['scans']]))
config.options['nominalDif'] = dict(zip(config.options['scans'], [[
    b-a for a,b in zip(posBeam1, posBeam2)
] for scanname in config.options['scans']]))

run = {
    'prepare': True,
    'gather': False,
    'fit': False,
    'analyze': False,
    'plot': False,
}

# Find ROOT files (needs to be executed only once)
if run['prepare']:
    from lsctools import prepare
    prepare.findRootFiles('fulltrees')
