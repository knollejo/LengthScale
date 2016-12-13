options = {}
EOSPATH = '/tmp/joknolle/eos/cms/store/group'
OUTPATH = '/afs/cern.ch/user/j/joknolle/lsc/results'

def VdM2015():
    """Set common parameters of 2015 Van der Meer scan program"""
    options['scans'] = ['X1', 'Y1', 'X2']
    options['runs'] = {'X1': 254991, 'Y1': 254991, 'X2': 254992}
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

def PCC():
    """Set common parameters of PCC data sets"""
    options['detector'] = ['pcc', 'PCC']
    options['treename'] = {'fulltrees': 'lumi/tree', 'minitrees': 'pccminitree'}

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

def VdM2016():
    """Set common parameters of 2016 Van der Meer scan program"""
    options['scans'] = ['X1', 'Y1', 'X2']
    options['runs'] = {'X1': 274100, 'Y1': 274100, 'X2': 274100}
    options['lumisections'] = {'X1': [640, 715], 'Y1': [715, 820], \
                               'X2': [200, 300]}
    options['crossings'] = [41, 281, 872, 1783, 2063]
    
    beginMin = {'X1': [0, 2, 3, 5, 7, 9, 10, 12, 14, 16], \
                'Y1': [24, 26, 28, 30, 34, 35, 37, 39, 41, 43, 45], \
                'X2': [442, 445, 446, 448, 451, 452, 455, 456, 459, 461, 463]}
    beginSec = {'X1': [2, 10, 45, 30, 5, 50, 40, 40, 10, 20], \
                'Y1': [50, 40, 40, 20, 0, 44, 30, 20, 10, 0, 20], \
                'X2': [58, 32, 58, 58, 20, 56, 20, 58, 20, 20, 20]}
    endMin = {'X1': [0, 2, 4, 6, 8, 9, 11, 13, 15, 17], \
              'Y1': [25, 27, 29, 31, 34, 36, 38, 40, 41, 43, 46], \
              'X2': [444, 445, 447, 449, 451, 453, 455, 457, 459, 462, 464]}
    endSec = {'X1': [50, 50, 30, 0, 55, 30, 20, 200, 04, 00], \
              'Y1': [30, 20, 20, 0, 46, 20, 10, 0, 50, 50, 0], \
              'X2': [12, 40, 40, 40, 50, 50, 40, 40, 40, 0, 0]}
    stableBeamsDeclared = 1464347152
    options['begin'] = dict(zip(options['scans'], [[stableBeamsDeclared+a*60+b \
           for a,b in zip(beginMin[scanname], beginSec[scanname])] for \
           scanname in options['scans']]))
    options['end'] = dict(zip(options['scans'], [[stableBeamsDeclared+a*60+b \
           for a,b in zip(endMin[scanname], endSec[scanname])] for scanname in \
           options['scans']]))
    
    posBeam1 = {'X1': [+195, +65, -65, -195, -325, -195, -65, 65, 195, 325], \
                'Y1': [-300, -180, -60, 60, 180, 300, 180, 60, -60, -180, -300], \
                'X2': [325, 195, 65, -65, -195, -325, -195, -65, 65, 195, 325]}
    posBeam2 = {'X1': [+65, -65, -195, -325, -195, -65, 65, 195, 325, 195], \
                'Y1': [-180, -60, 60, 180, 300, 180, 60, -60, -180, -300, -180], \
                'X2': [195, 65, -65, -195, -325, -195, -65, 65, 195, 325, 195]}
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

    options['fulltrees'] = ['/comm_luminosity/PCC/VdM/May182016_274100/Zero' \
                            +'Bias'+str(i)+'/PCC_VdM_ZeroBias'+str(i)+'_' \
                            +'274100_ProMay312016_Event_AlwaysTrue/160531_' \
                            +str(time)+'/0000' for i, time in \
                            enumerate([211313, 211331, 211350, 211413, 211430, \
                            211447, 211507, 211529], start=1)]
    options['minitrees'] = [s+'_vdmminitrees' for s in options['fulltrees']]
    options['dataset'] = ['promptreco16', 'Prompt Reco 2016']
