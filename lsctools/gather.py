from config import options as O, EOSPATH as eos
from tools import plotName, plotTitle, openRootFileW, openRootFileU, \
                  closeRootFile, loadFiles
from ROOT import TChain, TH1I, TH1F, TObject, TProfile

def chain(fileset, scan=''):
    """Create chain of all files belonging to a scan"""
    chain = TChain(O['treename'][fileset])
    if scan:
        files = loadFiles(fileset)[scan]
    else:
        files = loadFiles(fileset+'_all')
    for filename in files:
        chain.Add(filename)
    return chain

def reducedChain(fileset, scan=''):
    """Create chain of 1/8 of the files belonging to a scan"""
    chain = TChain(O['treename'][fileset])
    if scan:
        files = loadFiles(fileset)[scan]
    else:
        files = loadFiles(fileset+'_all')
    for filename in [f for f in files if 'ZeroBias1' in f]:
        chain.Add(filename)
    return chain

def miniCondition(scan, bx, step, all=False):
    """Create condition that event in a minitree belongs to step and BX"""
    cond = 'timeStamp >= ' + str(O['begin'][scan][step]) + \
           ' && timeStamp <= ' + str(O['end'][scan][step])
    if all:
        return cond
    else:
        return cond + ' && BXid == ' + str(bx)

def doPerBxStep(options):
    """Extract data from ROOT files and sort by bunch crossing and step"""
    c = chain(options['fileset'], options['scan'])
    name = options['scan'] + '_' + options['name']
    if 'method' in options:
        name += '_' + options['method']
    f = openRootFileU(name)
    for bx in O['crossings']:
        for step in range(len(O['nominalPos'][options['scan']])):
            print '<<< Analyze:', options['scan'], bx, 'step', step
            histname = plotName(name+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=False)
            histtitl = plotTitle(options['scan']+' BX '+str(bx)+', Step '+\
                                str(step))
            hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
            hist.StatOverflows(True)
            c.Draw(options['field'](options['scan'])+'>>'+histname, \
                   options['condition'](options['scan'], bx, step), 'goff')
            hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

def doPerStep(options):
    """Extract data from ROOT files and sort by step"""
    c = chain(options['fileset'], options['scan'])
    name = options['scan'] + '_' + options['name']
    if 'method' in options:
        name += '_' + options['method']
    if len(O['crossings']):
        cond = O['bxname'][options['fileset']] + ' == ' + str(O['crossings'][0])
        if O['crossings'][1:]:
            cond = '(' + cond
            for bx in O['crossings']:
                cond += ' || ' + O['bxname'][options['fileset']] + ' == ' + str(bx)
            cond += ')'
        cond = ' && ' + cond
    else:
        cond = ''
    f = openRootFileU(name)
    for step in range(len(O['nominalPos'][options['scan']])):
        print '<<< Analyze:', options['scan'], 'step', step
        histname = plotName(name+'_bxall_step'+str(step), timestamp=False)
        histtitl = plotTitle(options['scan']+' BX all, Step '+str(step))
        hist = options['histo'](histname, histtitl, options['bin'], \
                                options['min'], options['max'])
        hist.StatOverflows(True)
        c.Draw(options['field'](options['scan'])+'>>'+histname, \
               options['condition'](options['scan'], step)+cond, 'goff')
        hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

def combinePerStep(options):
    """Combine data from all bunch crossings into a single histogram"""
    name = options['scan'] + '_' + options['name']
    if 'method' in options:
        name += '_' + options['method']
    f = openRootFileU(name)
    for step in range(len(O['nominalPos'][options['scan']])):
        histname = plotName(name+'_bxall_step'+str(step), timestamp=False)
        histtitl = plotTitle(options['scan']+', Step '+str(step)+' (all BX)')
        hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
        hist.StatOverflows(True)
        print '<<< Combine histograms:', histname
        for bx in O['crossings']:
            bxname = plotName(name+'_bx'+str(bx)+'_step'+str(step), \
                              timestamp=False)
            bxhist = f.Get(bxname)
            hist.Add(bxhist)
        hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

def numberClustersPerBxStep(scan, combine=False, alternative=False, all=False):
    """Extract number of pixel clusters from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 1000.5, 'bin': 1001, 'histo': TH1I, \
               'name': 'nCluster', 'scan': scan}
    if combine:
        if alternative:
            options['method'] = 'LS'
        combinePerStep(options)
    else:
        options['fileset'] = 'minitrees'
        options['field'] = lambda s: 'nCluster'
        def condition2(s, bx, step, all=False):
            cond = '(LS == ' + str(O['LS'][s][step][0])
            for ls in O['LS'][s][step][1:]:
                cond += ' || LS == ' + str(ls)
            cond += ')'
            if all:
                return cond
            else:
                return cond + ' && BXid == ' + str(bx)
        if alternative:
            condition = condition2
            options['method'] = 'LS'
        else:
            condition = miniCondition
        if all:
            options['condition'] = lambda s, step: condition(s, None, step, \
                                                             all=True)
            doPerStep(options)
        else:
            options['condition'] = condition
            doPerBxStep(options)

def numberVerticesPerBxStep(scan, combine=False, alternative=False, all=False):
    """Extract vertex number from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 9.5, 'bin': 10, 'histo': TH1I, \
               'name': 'nVtx', 'scan': scan}
    if combine:
        if alternative:
            options['method'] = 'LS'
        combinePerStep(options)
    else:
        options['fileset'] = 'minitrees'
        options['field'] = lambda s: 'nVtx'
        def condition2(s, bx, step, all=False):
            cond = '(LS == ' + str(O['LS'][s][step][0])
            for ls in O['LS'][s][step][1:]:
                cond += ' || LS == ' + str(ls)
            cond += ')'
            if all:
                return cond
            else:
                return cond + ' && BXid == ' + str(bx)
        if alternative:
            condition = condition2
            options['method'] = 'LS'
        else:
            condition = miniCondition
        if all:
            options['condition'] = lambda s, step: condition(s, None, step, \
                                                             all=True)
            doPerStep(options)
        else:
            options['condition'] = condition
            doPerBxStep(options)

def vertexTemplatePerBxStep(options, combine=False, alternative=False, \
                            all=False, field=None):
    """Template for extraction of vertex data from ROOT files by BX and step"""
    if combine:
        if alternative:
            options['method'] = 'LS'
        combinePerStep(options)
    else:
        options['fileset'] = 'fulltrees'
        options['field'] = field
        if all:
            def condition1(s, step):
                return 'timeStamp_begin >= ' + str(O['begin'][s][step]) + \
                       ' && timeStamp_begin <= ' + str(O['end'][s][step]) + \
                       ' && ' + O['vtxisgood']
            def condition2(s, step):
                cond = '(LS == ' + str(O['LS'][s][step][0])
                for ls in O['LS'][s][step][1:]:
                    cond += ' || LS == ' + str(ls)
                cond += ')'
                return cond + ' && ' + O['vtxisgood']
            if alternative:
                options['condition'] = condition2
                options['method'] = 'LS'
            else:
                options['condition'] = condition1
            doPerStep(options)
        else:
            def condition1(s, bx, step):
                return 'timeStamp_begin >= ' + str(O['begin'][s][step]) + \
                       ' && timeStamp_begin <= ' + str(O['end'][s][step]) + \
                       ' && ' + O['vtxisgood'] + ' && bunchCrossing == ' + str(bx)
            def condition2(s, bx, step):
                cond = '(LS == ' + str(O['LS'][s][step][0])
                for ls in O['LS'][s][step][1:]:
                    cond += ' || LS == ' + str(ls)
                cond += ')'
                return cond + ' && ' + O['vtxisgood'] + ' && bunchCrossing == ' + str(bx)
            if alternative:
                options['condition'] = condition2
                options['method'] = 'LS'
            else:
                options['condition'] = condition1
            doPerBxStep(options)

def vertexPositionPerBxStep(scan, combine=False, alternative=False, all=False):
    """Extract vertex position from ROOT files sorted by BX and step"""
    options = {'min': -1e3, 'max': 3e3, 'bin': 250, 'histo': TH1F, \
               'name': 'vtxPos', 'scan': scan}
    if combine:
        field = None
    else:
        def field(s):
            if 'X' in s:
                return 'vtx_x*1e4'
            else:
                return 'vtx_y*1e4'
    vertexTemplatePerBxStep(options, combine, alternative, all, field)

def vertexPositionTrPerBxStep(scan, combine=False, alternative=False, all=False):
    """Extract transverse vertex position from ROOT files sorted by BX and step"""
    options = {'min': -1e3, 'max': 3e3, 'bin': 250, 'histo': TH1F, \
               'name': 'vtxPosTr', 'scan': scan}
    if combine:
        field = None
    else:
        def field(s):
            if 'X' in s:
                return 'vtx_y*1e4'
            else:
                return 'vtx_x*1e4'
    vertexTemplatePerBxStep(options, combine, alternative, all, field)

def vertexDistancePerBxStep(scan, combine=False, alternative=False, all=False):
    """Extract vertex distance from ROOT files sorted by BX and step"""
    options = {'min': -1e3, 'max': 3e3, 'bin': 250, 'histo': TH1F, \
               'name': 'vtxDist', 'scan': scan}
    if combine:
        field = None
    else:
        def field(s):
            if 'X' in s:
                return 'TMath::Sign(sqrt(vtx_x^2+vtx_y^2)*1e4,vtx_x)'
            else:
                return 'TMath::Sign(sqrt(vtx_x^2+vtx_y^2)*1e4,vtx_y)'
    vertexTemplatePerBxStep(options, combine, alternative, all, field)

def countsPerBxStep(scan, combine=False, alternative=False, all=False):
    """Extract BCM1f counts from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 599.5, 'bin': 600, 'histo': TH1I, \
               'name': 'counts', 'scan': scan}
    if combine:
        if alternative:
            options['method'] = 'LS'
        combinePerStep(options)
    else:
        options['fileset'] = 'hd5files'
        options['field'] = lambda s: 'data'
        def condition1(s, step):
            return 'timestamp >= ' + str(O['begin'][s][step]) + \
                   ' && timestamp <= ' + str(O['end'][s][step])
        def condition2(s, step):
            cond = 'ls == ' + str(O['LS'][s][step][0])
            for ls in O['LS'][s][step][1:]:
                cond += ' || ls == ' + str(ls)
            return cond
        if all:
            if alternative:
                options['condition'] = condition2
                options['method'] = 'LS'
            else:
                options['condition'] = condition1
            doPerStep(options)
        else:
            if alternative:
                options['condition'] = lambda sc, bx, st: '('+condition2(sc,st) \
                                       +') && bx == '+str(bx)
                options['method'] = 'LS'
            else:
                options['condition'] = lambda sc, bx, st: condition1(sc,st) \
                                       +' && bx == '+str(bx)
            doPerBxStep(options)

def pccPerLumiSection(options):
    """Extract PCC data from ROOT files and sort by lumisection"""
    c = chain(options['fileset'], options['scan'])
    rc = reducedChain(options['fileset'], options['scan'])
    name = options['name'] + '_perLS'
    f = openRootFileU(name)
    print '<<< Analyze', options['title']
    histname = plotName(options['title']+'_perLS', timestamp=False)
    histtitl = plotTitle()
    print '<<< Get Minimum'
    mini = int(rc.GetMinimum('LS'))
    print '<<< Get Maximum'
    maxi = int(rc.GetMaximum('LS'))
    print '<<< Fill Profile Histogram', histname
    hist = TProfile(histname, histtitl, maxi-mini+1, mini-0.5, maxi+0.5)
    c.Draw(options['field']+':LS>>'+histname, '', 'goff')
    hist.Write('', TObject.kOverwrite)
    closeRootFile(f, name)

def numberClusterPerLumiSection(scan):
    """Extract cluster number from ROOT files sorted by lumisection"""
    options = {'fileset': 'fulltrees', 'name': 'nCluster', \
               'scan': scan, 'title': 'nCluster'+scan, \
               'field': 'nCluster'}
    pccPerLumiSection(options)

def vertexPositionPerLumiSection(scan):
    """Extract vertex position from ROOT files sorted by lumisection"""
    options = {'fileset': 'fulltrees', 'name': 'vtxPos', \
               'scan': scan, 'title': 'vtxPos'+scan, \
               'field': 'vtx_'+scan[0].lower()+'*1e4'}
    pccPerLumiSection(options)

def pccPerTimeStamp(options):
    """Extract PCC data from ROOT files and sort by timestamps"""
    c = chain(options['fileset'], options['scan'])
    rc = chain(options['fileset'], options['scan'])
    name = options['name'] + '_' + options['scan'] + '_perTime'
    f = openRootFileU(options['name']+'_perTime')
    print '<<< Analyze', options['scan'], options['name']
    histname = plotName(name, timestamp=False)
    histtitl = plotTitle(options['scan'])
    print '<<< Get Minimum'
    mini = int(rc.GetMinimum(O['timename'][options['fileset']]))
    print '<<< Get Maximum'
    maxi = int(rc.GetMaximum(O['timename'][options['fileset']]))
    print '<<< Fill Profile Histogram', histname
    hist = TProfile(histname, histtitl, maxi-mini+1, mini-0.5, maxi+0.5)
    c.Draw(options['field']+':'+O['timename'][options['fileset']]+'>>'+ \
           histname, '', 'goff')
    hist.Write('', TObject.kOverwrite)
    closeRootFile(f, options['name']+'_perTime')

def vertexPositionPerTimeStamp(scan):
    """Extract vertex position from ROOT files sorted by timestamps"""
    options = {'fileset': 'fulltrees', 'name': 'vtxPos', 'scan': scan, \
               'field': 'vtx_'+scan[0].lower()+'*1e4'}
    pccPerTimeStamp(options)
