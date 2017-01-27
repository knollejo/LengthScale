from config import options as O, EOSPATH as eos
from tools import plotName, plotTitle, openRootFileW, openRootFileU, \
                  closeRootFile, loadFiles
from array import array
from ROOT import TChain, TH1I, TH1F, TObject, TProfile

def chain(fileset, scan=''):
    """Create chain of all files belonging to a scan"""
    chain = TChain(O['treename'][fileset])
    if scan:
        files = loadFiles(fileset)[scan]
    else:
        files = loadFiles(fileset+'_all')
    for filename in files:
        chain.Add(eos+filename)
    return chain

def reducedChain(fileset, scan=''):
    """Create chain of 1/8 of the files belonging to a scan"""
    chain = TChain(O['treename'][fileset])
    if scan:
        files = loadFiles(fileset)[scan]
    else:
        files = loadFiles(fileset+'_all')
    for filename in [f for f in files if 'ZeroBias1' in f]:
        chain.Add(eos+filename)
    return chain

def pccPerBxStep(options):
    """Extract PCC data from ROOT files and sort by bunch crossing and step"""
    c = chain(options['fileset'], options['scan'])
    name = options['scan'] + '_' + options['name']
    hists = dict(zip(O['crossings'], [[] for bx in O['crossings']]))
    nSteps = len(O['nominalPos'][options['scan']])
    for bx in O['crossings']:
        for step in range(nSteps):
            histname = plotName(options['scan']+'_'+options['name']+'_bx'+\
                                str(bx)+'_step'+str(step), timestamp=False)
            histtitl = plotTitle(options['scan']+' BX '+str(bx)+', Step '+\
                                str(step))
            hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
            hist.StatOverflows(True)
            hists[bx].append(hist)
    fields = {}
    for f, t, v in options['fields']:
        pointer = array(t, v)
        c.SetBranchAddress(f, pointer)
        fields[f] = pointer
    nEntries = c.GetEntries()
    print '<<< Run over', nEntries, 'events'
    for n in range(nSteps):
        if n % 10000 == 0:
            print '<<< Processing event', n
        c.GetEntry(n)
        for bx in O['crossings']:
            for step in range(nSteps):
                values = options['evaluate'](fields, bx, step)
                if not values:
                    continue
                for v in values:
                    hists[bx][step].Fill(v)
    f = openRootFileW(name)
    for bx in O['crossings']:
        for hist in hists[bx]:
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

def numberClustersPerBxStep(scan, combine=False):
    """Extract number of pixel clusters from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 1000.5, 'bin': 1001, 'histo': TH1I, \
               'name': 'nCluster', 'scan': scan}
    if combine:
        combinePccPerStep(options)
    else:
        def evaluate(event, bx, step, s):
            flag = event.timeStamp >= O['begin'][s][step] and \
                   event.timeStamp <= O['end'][s][step] and event.BXid == bx
            value = [event.nCluster]
            return flag, value
        options['fileset'] = 'minitrees'
        options['evaluate'] = lambda ev, bx, st: evaluate(ev, bx, st, scan)
        pccPerBxStep(options)

def numberVerticesPerBxStep(scan, combine=False):
    """Extract vertex number from ROOT files sorted by BX and step"""
    options = {'min': -0.5, 'max': 9.5, 'bin': 10, 'histo': TH1I, \
               'name': 'nVtx', 'scan': scan}
    if combine:
        combinePccPerStep(options)
    else:
        def evaluate(event, bx, step, s):
            flag = event.timeStamp >= O['begin'][s][step] and \
                   event.timeStamp <= O['end'][s][step] and event.BXid == bx
            value = [event.nVtx]
            return flag, value
        options['fileset'] = 'minitrees'
        options['evaluate'] = lambda ev, bx, st: evaluate(ev, bx, st, scan)
        pccPerBxStep(options)

def vertexPositionPerBxStep(scan, combine=False, alternative=False):
    """Extract vertex position from ROOT files sorted by BX and step"""
    options = {'min': -3e3, 'max': 3e3, 'bin': 500, 'histo': TH1F, \
               'name': 'vtxPos', 'scan': scan}
    if combine:
        combinePccPerStep(options)
    else:
        options['fields'] = [('bunchCrossing', 'l', [0]), \
                            ('nVtx', 'l', [0]), \
                            ('vtx_isGood', 'b', 10*[0])]
        if 'X' in scan:
            options['fields'].append(('vtx_x', 'f', 10*[0.]))
        else:
            options['fields'].append(('vtx_y', 'f', 10*[0.]))
        def evaluate1(fields, bx, step, s):
            if fields['timeStamp_begin'][0] < O['begin'][s][step] or \
               fields['timeStamp_begin'][0] > O['end'][s][step] or \
               fields['bunchCrossing'][0] != bx:
                return []
            if 'X' in s:
                vtx = fields['vtx_x']
            else:
                vtx = fields['vtx_y']
            values = []
            nVtx = min(fields['nVtx'], 10)
            for i in range(nVtx):
                if fields['vtx_isGood'][i]:
                    values.append(vtx[i] * 1e4)
            return values
        def evaluate2(fields, bx, step, s):
            if fields['LS'][0] < O['beginLS'][s][step] or \
               fields['LS'][0] > O['endLS'][s][step] or \
               fields['bunchCrossing'][0] != bx:
                return []
            if 'X' in s:
                vtx = fields['vtx_x']
            else:
                vtx = fields['vtx_y']
            values = []
            nVtx = min(fields['nVtx'], 10)
            for i in range(nVtx):
                if fields['vtx_isGood'][i]:
                    values.append(vtx[i] * 1e4)
            return values
        if alternative:
            options['evaluate'] = lambda fi, bx, st: evaluate2(fi, bx, st, scan)
            options['name'] += 'LS'
            options['fields'].append(('LS', 'l', [0]))
        else:
            options['evaluate'] = lambda fi, bx, st: evaluate1(fi, bx, st, scan)
            options['fields'].append(('timeStamp_begin', 'L', [0]))
        options['fileset'] = 'fulltrees'
        pccPerBxStep(options)

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
