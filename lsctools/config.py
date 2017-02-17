options = {}
EOSPATH = '/eos/cms/store/group'
OUTPATH = '/afs/cern.ch/user/j/joknolle/LengthScale/results'
OWNPATH = '/afs/cern.ch/work/j/joknolle/store'

def PCC():
    """Set common parameters of PCC data sets"""
    options['detector'] = ['pcc', 'PCC']
    options['treename'] = {'fulltrees': 'lumi/tree', 'minitrees': 'pccminitree'}
    options['timename'] = {'fulltrees': 'timeStamp_begin', \
                           'minitrees': 'timeStamp'}
    options['bxname'] = {'fulltrees': 'bunchCrossing', 'minitrees': 'BXid'}

def BCM1f():
    """Set common parameters of BCM1f data sets"""
    options['detector'] = ['bcm1f', 'BCM1f']
    options['treename'] = {'owntrees': 'bcm1f'}
    options['timename'] = {'owntrees': 'timestamp'}
    options['bxname'] = {'owntrees': 'bx'}

def VdM2015():
    """Set common parameters of 2015 Van der Meer scan program"""
    options['scans'] = ['X1', 'Y1', 'X2']
    options['runs'] = {'X1': 254991, 'Y1': 254991, 'X2': 254992}
    options['fill'] = 4266
    options['lumisections'] = {'X1': [285, 360], 'Y1': [361, 428], \
                               'X2': [200, 257]}
    options['crossings'] = [51, 771, 1631, 2211, 2674]

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
    options.clear()
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
    options.clear()
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
    options.clear()
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
    options.clear()
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

def PCCPromptReco2016():
    """Set parameters of 2016 PCC Prompt Reco"""
    print '<<< Initialize PCC PromptReco 2016'
    options.clear()
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
    options.clear()
    VdM2016()
    PCC()

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/May2016Scans/ZeroBias' \
                            +str(i)+'/PCC_Run2016B-17Jan2017-v1_ZeroBias' \
                            +str(i)+'/170130_0'+str(time)+'/0000' for i, time \
                            in zip([1, 2, 3, 4, 6, 8], [84827, 84841, 84855, \
                            84911, 84929, 84943])]
    options['minitrees'] = []
    options['dataset'] = ['2016_rereco_jan17_part', \
                          '2016 ReReco Jan 2017 (partial)']

def BCM1f2016():
    """Set parameters of 2016 BCM1f data"""
    print '<<< Initialize 2016 data of BCM1f'
    options.clear()
    VdM2016()
    BCM1f()

    options['hd5files'] = ['/comm_luminosity/VdM/scanFill'+a+'/central' for a \
                           in ['4954_27May16', '4945_18May16']]
    options['dataset'] = ['2016', '2016']
