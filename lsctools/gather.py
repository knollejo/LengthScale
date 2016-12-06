from config import options as O, EOSPATH as eos
from tools import plotName, plotTitle, openRootFileW, closeRootFile, loadFiles
from ROOT import TChain, TH1I, TH1F

def chain(fileset, scan):
    """Create chain of all files belonging to a scan"""
    files = loadFiles(fileset)
    chain = TChain(O['treename'][fileset])
    for filename in files[scan]:
        chain.Add(eos+'/'+filename)
    return chain

def miniCondition(scan, bx, step):
    """Create condition that event in a minitree belongs to step and BX"""
    return 'timeStamp >= ' + str(O['begin'][scan][step]) + \
           ' && timeStamp <= ' + str(O['end'][scan][step]) + \
           ' && BXid == ' + str(bx)

def pccPerBxStep(options):
    """Extract PCC data from ROOT files and sort by bunch crossing and step"""
    c = chain(options['fileset'], options['scan'])
    name = options['scan'] + '_' + options['name']
    f = openRootFileW(name)
    for bx in O['crossings']:
        for step in range(len(O['nominalPos'][options['scan']])):
            print '<<< Analyze:', options['scan'], bx, 'step', step
            histname = plotName(options['scan']+'_'+options['name']+'_bx'+\
                                str(bx)+'_step'+str(step), timestamp=False)
            histtitl = plotTitle(options['scan']+' BX '+str(bx)+', Step '+\
                                str(step))
            hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
            hist.StatOverflows(True)
            c.Draw(options['field'](options['scan'])+'>>'+histname, \
                   options['condition'](options['scan'], bx, step), 'goff')
            hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

def combinePccPerStep(options):
    """Combine PCC data from all bunch crossings into a single histogram"""
    name = options['scan'] + '_' + options['name']
    f = openRootFileU(name)
    for step in range(len(O['nominalPos'][options['scan']])):
        histname = plotName(options['scan']+'_'+options['name']+'_bxall_step'+ \
                            str(step), timestamp=False)
        histtitl = plotTitle(options['scan']+', Step '+str(step)+' (all BX)')
        hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
        hist.StatOverflows(True)
        print '<<< Combine histograms:', histname
        for bx in O['crossings']:
            bxname = plotName(options['scan']+'_'+options['name']+'_bx'+ \
                              str(bx)+'_step'+str(step), timestamp=False)
            bxhist = f.Get(bxname)
            hist.Add(bxhist)
        hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

def numberClusters(scan, combine=False):
    """Extract number of pixel clusters from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 1000.5, 'bin': 1001, 'histo': TH1I, \
               'name': 'nCluster', 'scan': scan}
    if combine:
        combinePccPerStep(options)
    else:
        options['condition'] = miniCondition
        options['fileset'] = 'minitrees'
        options['field'] = lambda s: 'nCluster'
        pccPerBxStep(options)

def numberVertices(scan, combine=False):
    """Extract vertex number from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 9.5, 'bin': 10, 'histo': TH1I, \
               'name': 'nVtx', 'scan': scan}
    if combine:
        combinePccPerStep(options)
    else:
        options['condition'] = miniCondition
        options['fileset'] = 'minitrees'
        options['field'] = lambda s: 'nVtx'
        pccPerBxStep(options)

def vertexPosition(scan, combine=False):
    """Extract vertex position from ROOT files sorted by BX and step"""
    options = {'min': -3e3, 'max': 3e3, 'bin': 500, 'histo': TH1F, \
               'name': 'vtxPos', 'scan': scan}
    if combine:
        combinePccPerStep(options)
    else:
        def field(s):
            if 'X' in scan:
                return 'vtx_x*1e4'
            else:
                return 'vtx_y*1e4'
        def condition(s, bx, step):
            return 'timeStamp_begin >= ' + str(O['begin'][s][step]) + \
                   ' && timeStamp_begin <= ' + str(O['end'][s][step]) + \
                   ' && vtx_isGood && bunchCrossing == ' + str(bx)
        options['condition'] = condition
        options['fileset'] = 'fulltrees'
        options['field'] = field
        pccPerBxStep(options)
