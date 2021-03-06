from math import copysign
from os.path import dirname

options = {'nominalTitle': 'Nominal Position [#mum]'}
EOSPATH = '/eos/cms/store/group'
OUTPATH = dirname(__file__)+'/../results'
OWNPATH = '/afs/cern.ch/work/j/joknolle/store'

def PCC():
    """Set common parameters of PCC data sets"""
    options['detector'] = ['pcc', 'PCC']
    options['treename'] = {'fulltrees': 'lumi/tree', 'minitrees': 'pccminitree'}
    options['timename'] = {'fulltrees': 'timeStamp_begin', \
                           'minitrees': 'timeStamp'}
    options['bxname'] = {'fulltrees': 'bunchCrossing', 'minitrees': 'BXid'}
    options['vtxisgood'] = 'vtx_isGood'

def BCM1f():
    """Set common parameters of BCM1f data sets"""
    options['detector'] = ['bcm1f', 'BCM1f']
    options['treename'] = {'hd5files': 'bcm1f'}
    options['timename'] = {'hd5files': 'timestamp'}
    options['bxname'] = {'hd5files': 'bx'}

def PLT():
    """Set common parameters of PLT data sets"""
    options['detector'] = ['plt', 'PLT']
    options['treename'] = {'hd5files': 'plt'}
    options['timename'] = {'hd5files': 'timestamp'}
    options['bxname'] = {'hd5files': 'bx'}

def VdM2015():
    """Set common parameters of 2015 Van der Meer scan program"""
    options['scans'] = ['X1', 'Y1', 'X2']
    options['runs'] = {'X1': 254991, 'Y1': 254991, 'X2': 254992}
    options['fill'] = 4266
    options['lumisections'] = {'X1': [285, 360], 'Y1': [361, 428], \
                               'X2': [200, 257]}
    options['crossings'] = [51, 771, 1631, 2211, 2674]
    options['plotsig'] = '2015 (13 TeV)'

    beginMin = {'X1': [307, 309, 311, 313, 315, 317, 320, 322, 324], \
                'Y1': [333, 335, 337, 339, 341, 343, 345, 347, 349, 351], \
                'X2': [442, 445, 446, 448, 451, 452, 455, 456, 459, 461]}
    beginSec = {'X1': [40, 40, 40, 40, 40, 58, 10, 10, 10], \
                'Y1': [32, 56, 56, 44, 44, 44, 44, 44, 44, 44], \
                'X2': [58, 32, 58, 58, 20, 56, 20, 58, 20, 20]}
    endMin = {'X1': [308, 310, 312, 314, 316, 318, 320, 322, 325], \
              'Y1': [334, 336, 338, 340, 342, 344, 346, 348, 350, 352], \
              'X2': [444, 445, 447, 449, 451, 453, 455, 457, 459, 462]}
    endSec = {'X1': [16, 16, 16, 16, 28, 50, 50, 50, 04], \
              'Y1': [16, 16, 16, 16, 16, 16, 16, 16, 16, 16], \
              'X2': [12, 40, 40, 40, 50, 50, 40, 40, 40, 0]}
    stableBeamsDeclared = 1440450384
    options['begin'] = dict(zip(options['scans'], [[stableBeamsDeclared+a*60+b \
           for a,b in zip(beginMin[scanname], beginSec[scanname])] for \
           scanname in options['scans']]))
    options['end'] = dict(zip(options['scans'], [[stableBeamsDeclared+a*60+b \
           for a,b in zip(endMin[scanname], endSec[scanname])] for scanname in \
           options['scans']]))

    options['LS'] = {'X1': [[303], [308], [313], [318], [324], [330], [335], \
                            [340], [346]], \
                     'Y1': [[370], [375], [380], [385], [390], [395], [401], \
                            [406], [411], [416]], \
                     'X2': [[203], [208], [213], [218], [223], [229], [234], \
                            [239], [244], [249]]}

    posBeam1 = {'X1': [+195, +65, -65, -195, -325, -195, -65, 65, 195], \
                'Y1': [-300, -180, -60, 60, 180, 300, 180, 60, -60, -180], \
                'X2': [325, 195, 65, -65, -195, -325, -195, -65, 65, 195]}
    posBeam2 = {'X1': [+65, -65, -195, -325, -195, -65, 65, 195, 325], \
                'Y1': [-180, -60, 60, 180, 300, 180, 60, -60, -180, -300], \
                'X2': [195, 65, -65, -195, -325, -195, -65, 65, 195, 325]}
    options['nominalPos'] = dict(zip(options['scans'], [[(a+b)/2. for a,b in \
           zip(posBeam1[scanname], posBeam2[scanname])] for scanname in \
           options['scans']]))
    options['nominalDif'] = dict(zip(options['scans'], [[b-a for a,b in \
           zip(posBeam1[scanname], posBeam2[scanname])] for scanname in \
           options['scans']]))

def PCCPromptReco2015():
    """Set parameters of 2015 PCC Prompt Reco"""
    print '<<< Initialize PCC PromptReco 2015'
    VdM2015()
    PCC()

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/0150825/ZeroBias'+str(i) \
                            +'/PCC_ZeroBias'+str(i+1)+'_VdMScans_150825_nVtxFix' \
                            +'/150831_'+str(time)+'/0000' for i, time in \
                            enumerate([134443, 134510, 134550, 134629, 134649, \
                            134708, 134731, 134748], start=1)]
    options['minitrees'] = [s+'_noveto' for s in options['fulltrees']]
    options['dataset'] = ['promptreco15', 'Prompt Reco 2015']

def PCCReRecoOct2015():
    """Set parameters of October 2015 PCC ReReco"""
    print '<<< Initialize PCC ReReco Oct 2015'
    VdM2015()
    PCC()

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/0150825_05Oct2015ReReco' \
                            +'V2/ZeroBias'+str(i)+'/PCC_ZeroBias'+str(i)+'_Re' \
                            +'RecoV2/160104_'+str(time)+'/0000' for i, time in \
                            enumerate([232532, 232550, 232605, 232620, 232635, \
                            232651, 232707, 232722], start=1)]
    options['minitrees'] = [s+'_noveto' for s in options['fulltrees']]
    options['dataset'] = ['rereco_oct15', 'ReReco Oct 2015']

def PCCReRecoDec2015():
    """Set parameters of December 2015 PCC ReReco"""
    print '<<< Initialize PCC ReReco Dec 2015'
    VdM2015()
    PCC()

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/0150825_Dec2015ReReco/' \
                            +'ZeroBias'+str(i)+'/PCC_VdM_ZeroBias'+str(i)+'_' \
                            +'4266_DecRereco_Event/161026_'+str(time)+'/0000' \
                            for i, time in enumerate([153235, 153318, 153418, \
                            153453, 153542, 153807, 153907, 153950], start=1)]
    options['minitrees'] = [s+'_vdmminitrees' for s in options['fulltrees']]
    options['dataset'] = ['rereco_dec15', 'ReReco Dec 2015']

def PCC2015ReRecoJan2017():
    """Set parameters of January 2017 ReReco of 2015 PCC"""
    print '<<< Initialize PCC 2015 ReReco January 2017'
    VdM2015()
    PCC()

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/August2015Scans/ZeroBias' \
                            +str(i)+'/PCC_Run2015C_25ns-19Jan2017-v1_Zero' \
                            +'Bias'+str(i)+'/170123_'+str(time)+'/0000' for i, \
                            time in zip([1, 2, 4, 6, 7, 8], [184427, 184441, \
                            184504, 184518, 184536, 184550])]
    options['minitrees'] = [s+'_noVeto' for s in options['fulltrees']]
    options['dataset'] = ['2015_rereco_jan17_part', \
                          '2015 ReReco Jan 2017 (partial)']

def VdM2016():
    """Set common parameters of 2016 Van der Meer scan program"""
    options['scans'] = ['X1', 'Y1', 'X2', 'Y2']
    options['runs'] = {'X1': 274100, 'Y1': 274100, 'X2': 273591, 'Y2': 273591}
    options['fill'] = 4954
    options['lumisections'] = {'X1': [668, 717], 'Y1': [731, 782], \
                               'X2': [290, 350], 'Y2': [345, 405]}
    options['crossings'] = [41, 281, 872, 1783, 2063]
    options['plotsig'] = '2016 (13 TeV)'

    beginMin = {'X1': [5, 7, 9, 11, 13, 14, 16, 18, 20, 22], \
                'Y1': [30, 32, 34, 36, 37, 39, 41, 43, 45, 46], \
                'X2': [], 'Y2': []}
    beginSec = {'X1': [49, 42, 28, 17, 02, 50, 38, 27, 15, 00], \
                'Y1': [33, 25, 11, 0, 51, 40, 27, 18, 5, 55], \
                'X2': [], 'Y2': []}
    endMin = {'X1': [6, 8, 10, 12, 14, 15, 17, 19, 21, 23], \
              'Y1': [31, 33, 35, 37, 38, 40, 42, 44, 46, 47], \
              'X2': [], 'Y2': []}
    endSec = {'X1': [49, 42, 28, 17, 2, 50, 38, 27, 15, 0], \
              'Y1': [33, 25, 11, 0, 51, 40, 27, 18, 5, 55], \
              'X2': [], 'Y2': []}
    May27ElevenOClock = 1464346800
    options['begin'] = dict(zip(options['scans'], [[May27ElevenOClock+a*60+b \
           for a,b in zip(beginMin[scanname], beginSec[scanname])] for \
           scanname in options['scans']]))
    options['end'] = dict(zip(options['scans'], [[May27ElevenOClock+a*60+b \
           for a,b in zip(endMin[scanname], endSec[scanname])] for scanname in \
           options['scans']]))

    options['LS'] = {'X1': [[671], [676], [681], [685], [690], [694], [699], \
                            [704], [708], [713]], \
                     'Y1': [[735], [740], [744], [749], [754], [758], [763], \
                            [768], [772], [777]], \
                     'X2': [[299], [304], [308], [313], [318], [322], [327], \
                            [332], [336], [341]], \
                     'Y2': [[355], [360], [365], [369], [374], [379], [383], \
                            [388], [393], [397]]}

    posBeam1 = {'X1': [-246.039, -147.623, -49.208, +49.208, +147.623, \
                       +246.039, +147.623, +49.208, -49.208, -147.623], \
                'Y1': [-246.039, -147.623, -49.208, +49.208, +147.623, \
                       +246.039, +147.623, +49.208, -49.208, -147.623], \
                'X2': [-246.039, -147.623, -49.208, +49.208, +147.623, \
                       +246.039, +147.623, +49.208, -49.208, -147.623], \
                'Y2': [-246.039, -147.623, -49.208, +49.208, +147.623, \
                       +246.039, +147.623, +49.208, -49.208, -147.623]}
    posBeam2 = {'X1': [-147.623, -49.208, +49.208, +147.623, +246.039, \
                       +147.623, +49.208, -49.208, -147.623, -246.039], \
                'Y1': [-147.623, -49.208, +49.208, +147.623, +246.039, \
                       +147.623, +49.208, -49.208, -147.623, -246.039], \
                'X2': [-147.623, -49.208, +49.208, +147.623, +246.039, \
                       +147.623, +49.208, -49.208, -147.623, -246.039], \
                'Y2': [-147.623, -49.208, +49.208, +147.623, +246.039, \
                       +147.623, +49.208, -49.208, -147.623, -246.039]}
    options['nominalPos'] = dict(zip(options['scans'], [[(a+b)/2. for a,b in \
           zip(posBeam1[scanname], posBeam2[scanname])] for scanname in \
           options['scans']]))
    options['nominalDif'] = dict(zip(options['scans'], [[b-a for a,b in \
           zip(posBeam1[scanname], posBeam2[scanname])] for scanname in \
           options['scans']]))

def VdM2016DorosPositions():
    """Set beam positions measured by DOROS of 2016 Van der Meer scan program"""
    dorosX1 = [[-232.79, 4.23, -141.917, 2.2625], \
               [-140.787, 5.177, -47.5415, 2.75], \
               [-46.2245, 5.864, 48.4053, 3.1235], \
               [47.7269, 5.7695, 144, 2.7225], \
               [141.538, 6.717, 238.746, 2.9265], \
               [237.043, 6.7575, 141.331, 2.929], \
               [143.814, 6.018, 45.3501, 2.4675], \
               [50.141, 5.558, -49.826, 2.498], \
               [-43.334, 5.62, -144.065, 2.202], \
               [-137.27, 5.296, -240.707, 2.2515]]
    dorosY1 = [[0.5415, -237.129, -3.1365, -143.403], \
               [0.3695, -143.827, -1.629, -48.572], \
               [0.942, -48.957, -1.37, 47.6725], \
               [0.9355, 45.617, -1.7015, 143.037], \
               [0.726, 140.072, -2.0495, 238.757], \
               [1.983, 237.563, -2.4065, 140.93], \
               [1.032, 143.748, -1.308, 45.466], \
               [-0.4285, 49.429, -1.234, -50.3495], \
               [-0.5, -45.5584, -0.755, -146.688], \
               [-1.3935, -139.405, -0.459, -241.569]]
    if 'nominalPos' not in options:
        options['nominalPos'] = {}
    if 'nominalDif' not in options:
        options['nominalDif'] = {}
    def xpos(x, y):
        return copysign((x**2+y**2)**0.5, x)
    def ypos(x, y):
        return copysign((x**2+y**2)**0.5, y)
    options['nominalPos']['X1'] = [xpos((a+c)/2.,(b+d)/2.) for a,b,c,d in dorosX1]
    options['nominalDif']['X1'] = [xpos(a-c,b-d) for a,b,c,d in dorosX1]
    options['nominalPos']['Y1'] = [ypos((a+c)/2.,(b+d)/2.) for a,b,c,d in dorosY1]
    options['nominalDif']['Y1'] = [ypos(a-c,b-d) for a,b,c,d in dorosY1]
    # options['nominalPos']['X1'] = [(a+c)/2. for a,b,c,d in dorosX1]
    # options['nominalDif']['X1'] = [a-c for a,b,c,d in dorosX1]
    # options['nominalPos']['Y1'] = [(b+d)/2. for a,b,c,d in dorosY1]
    # options['nominalDif']['X1'] = [b-d for a,b,c,d in dorosY1]
    # options['nominalPos']['X1y'] = [(b+d)/2. for a,b,c,d in dorosX1]
    # options['nominalDif']['X1y'] = [b-d for a,b,c,d in dorosX1]
    # options['nominalPos']['Y1x'] = [(a+c)/2. for a,b,c,d in dorosY1]
    # options['nominalDif']['Y1x'] = [a-c for a,b,c,d in dorosY1]
    options['nominalTitle'] = 'Position Measured by DOROS [#mum]'

def PCCPromptReco2016():
    """Set parameters of 2016 PCC Prompt Reco"""
    print '<<< Initialize PCC PromptReco 2016'
    VdM2016()
    PCC()

    run274100 = ['/comm_luminosity/PCC/VdM/May272016_274100/ZeroBias'+str(i) \
                 +'/PCC_VdM_ZeroBias'+str(i)+'_274100_ProMay312016_Event' \
                 +'_AlwaysTrue/160531_'+str(time)+'/0000' for i, time in \
                 enumerate([211313, 211331, 211350, 211413, 211430, 211447, \
                 211507, 211529], start=1)]
    run273591 = ['/comm_luminosity/PCC/VdM/May182016_273591/ZeroBias'+str(i) \
                 +'/PCC_VdM_ZeroBias'+str(i)+'_273591_ProMay212016_Event' \
                 +'_AlwaysTrue/16052'+time+'/0000' for i, time in \
                 enumerate(['4_190706', '4_190731', '4_190756', '4_190825', \
                 '4_190850', '1_215614', '4_190916', '4_190945'], start=1)]
    options['fulltrees'] = run273591 + run274100
    options['minitrees'] = [s+'_vdmminitrees' for s in options['fulltrees']]
    options['dataset'] = ['promptreco16', 'Prompt Reco 2016']

def PCC2016ReRecoJan2017():
    """Set parameters of January 2017 ReReco of 2016 PCC"""
    print '<<< Initialize PCC 2016 ReReco January 2017'
    VdM2016()
    PCC()

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/May2016Scans/ZeroBias' \
                            +str(i)+'/PCC_Run2016B-17Jan2017-v'+str(v)+'_' \
                            +'ZeroBias'+str(i)+'/170'+time+'/0000' for i, \
                            v, time in ((1, 1, '130_084827'), (2, 1, \
                            '130_084841'), (3, 1, '130_084855'), (4, 1, \
                            '130_084911'), (5, 4, '213_002332'), (6, 1, \
                            '130_084929'), (7, 3, '213_002401'), (8, 1, \
                            '130_084943'))]
    options['minitrees'] = [s+'_FPix_Feb27' for s in options['fulltrees']]
    # options['dataset'] = ['2016_rereco_jan17', \
    #                       '2016 ReReco Jan 2017']
    options['dataset'] = ['2016_rereco_jan17_part', '2016 ReReco Jan 2017 (partial)']

def HD5Files2016():
    """Set parameters of 2016 data that is stored in HD5 files"""
    options['hd5files'] = ['/comm_luminosity/VdM/scanFill'+a+'/compressed/'+ \
                           'central' for a in ['4954_27May16', '4945_18May16']]
    options['dataset'] = ['2016', '2016']

def BCM1f2016():
    """Set parameters of 2016 BCM1f data"""
    print '<<< Initialize 2016 data of BCM1f'
    VdM2016()
    BCM1f()
    HD5Files2016()

def PLT2016():
    """Set parameters of 2016 PLT data"""
    print '<<< Initialize 2016 data of PLT'
    VdM2016()
    PLT()
    HD5Files2016()

def VdM2017():
    """Set common parameters of 2017 Van der Meer scan program"""
    options['scans'] = ['X1', 'Y1']
    options['runs'] = {'X1': 300050, 'Y1': 300050}
    options['fill'] = 6016
    options['lumisections'] = {'X1': [8, 60], 'Y1': [68, 122]}
    options['crossings'] = [41, 281, 872, 1783, 2063]
    options['plotsig'] = 'Fill 6016 (2017, 13 TeV)'

    options['begin'] = {
        'X1': [1501261174, 1501261289, 1501261406, 1501261521, 1501261636, \
               1501261766, 1501261881, 1501261996, 1501262111, 1501262226], \
        'Y1': [1501262584, 1501262705, 1501262822, 1501262938, 1501263055, \
               1501263188, 1501263306, 1501263422, 1501263539, 1501263657] \
    }
    options['end'] = {
        'X1': [1501261247, 1501261362, 1501261477, 1501261592, 1501261707, \
               1501261837, 1501261952, 1501262067, 1501262182, 1501262297], \
        'Y1': [1501262659, 1501262777, 1501262893, 1501263010, 1501263126, \
               1501263259, 1501263377, 1501263493, 1501263611, 1501263728] \
    }

    options['LS'] = {
        'X1': [[11, 12], [16, 17], [21, 22], [26, 27], [31, 32], \
               [36, 37], [41, 42], [46, 47], [51, 52], [56, 57]], \
        'Y1': [[72, 73], [77, 78], [82, 83], [87, 88], [92, 93], \
               [97, 98], [102, 103], [107, 108], [112, 113], [117, 118]] \
    }

    posBeam1 = [-246.043, -147.626, -49.209, +49.209, +147.626, \
                +285.410, +186.993, +88.576, -9.842, -108.259]
    posBeam2 = [-108.259, -9.842, +88.576, +186.993, +285.410, \
                +147.626, +49.209, -49.209, -147.626, -246.043]
    options['nominalPos'] = dict(zip(options['scans'], [[(a+b)/2. for a,b in \
           zip(posBeam1, posBeam2)] for scanname in options['scans']]))
    options['nominalDif'] = dict(zip(options['scans'], [[b-a for a,b in \
           zip(posBeam1, posBeam2)] for scanname in options['scans']]))

def PCCPromptReco2017():
    """Set parameters of 2017 PCC Prompt Reco"""
    print '<<< Initialize PCC PromptReco 2017'
    VdM2017()
    PCC()

    options['fulltrees'] = [
        '/comm_luminosity/PCC/ForLumiComputation/2017/VdMFills/6016/ZeroBias' \
        +str(i)+'/crab_CMSSW_9_2_6_ZeroBias'+str(i)+'_splitPerBXTrue/' \
        +str(time)+'/0000' for i, time in enumerate(['180328_174419', \
        '180327_173243', '180327_193215', '180327_193232', '170804_183235', \
        '180328_174508', '180327_193252', '180328_174601'], start=1) \
    ]
    options['minitrees'] = [
        '/comm_luminosity/PCC/ForLumiComputation/2017/VdMFills/6016/ZeroBias' \
        +str(i)+'/crab_CMSSW_9_2_6_ZeroBias'+str(i)+'_splitPerBXTrue/17080' \
        +time+'/0000/minituples_v2_NoLayer1WithVetoModules/merged' for i, time \
        in enumerate(['4_183112', '4_183143', '4_183203', '4_183220', '4_183235', \
        '3_140851', '4_183310', '4_183328'], start=1) \
    ]
    options['dataset'] = ['promptreco17', 'Prompt Reco 2017']
