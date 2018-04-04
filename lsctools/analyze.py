from config import options as O
from tools import openRootFileR, openRootFileW, closeRootFile, plotName, \
                  plotTitle
from array import array
from ROOT import TMultiGraph, TGraphErrors, TObject

def scale(s=1.0):
    """Generate a function that multiplies the argument with a constant"""
    return lambda a: s*a

def collectPerDirectionBx(options):
    """Fit data in both directions of a scan"""
    nSteps = len(O['nominalPos'][options['scan']])
    for i in range(nSteps-1):
        if O['nominalPos'][options['scan']][i+1] == \
           O['nominalPos'][options['scan']][i]:
            break
    else:
        for i in range(nSteps-1):
            if abs(O['nominalPos'][options['scan']][i+1] - \
                   O['nominalPos'][options['scan']][i]) < 10.0:
                break
        else:
            raise RuntimeError('Could not find change of direction.')
    if 'nominalPos' in options:
        nominalPos = options['nominalPos']
    else:
        nominalPos = O['nominalPos'][options['scan']]
    oldname = options['scan'] + '_' + options['name'] + options['fitted']
    if 'newname' in options:
        newname = options['scan'] + '_' + options['newname'] + \
                  options['fitted']
    else:
        newname = oldname
    if 'method' in options:
        oldname += '_' + options['method']
        newname += '_' + options['method']
    newname += '_collected'
    f = openRootFileR(oldname)
    g = openRootFileW(newname)
    for bx in options['crossings']:
        average = [0 for j in range(nSteps)]
        averror = [0 for j in range(nSteps)]
        for step in range(nSteps):
            print '<<< Access data from:', options['scan'], bx, 'step', step
            histname = plotName(oldname+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=False)
            hist = f.Get(histname)
            if options['custom']:
                average[step], averror[step] = options['custom'](hist)
            else:
                average[step] = hist.GetMean()
                averror[step] = hist.GetMeanError()
        plotname = plotName(newname+'_bx'+str(bx), timestamp=False)
        plottitl = plotTitle(options['scan']+' BX '+str(bx))
        print '<<< Create plot:', plotname
        graphs = TMultiGraph(plotname, plottitl)
        residuals = TMultiGraph(plotname+'_residuals', '')
        for n, rnge in zip([i+1, nSteps-i-1], [lambda l: l[:i+1], \
                                               lambda l: l[i+1:]]):
            graph = TGraphErrors(n, \
                    array('d', [options['x'](a) for a in rnge(nominalPos)]), \
                    array('d', [options['y'](a) for a in rnge(average)]), \
                    array('d', [0]*n), \
                    array('d', [options['e'](a) for a in rnge(averror)]))
            graph.Fit(options['fit'])
            residual = TGraphErrors(n, \
                       array('d', [options['x'](a) for a in rnge(nominalPos)]), \
                       array('d', [options['y'](a) - graph.GetFunction( \
                             options['fit']).Eval(options['x'](b)) for a, b \
                             in zip(rnge(average), rnge(nominalPos))]),
                       array('d', [0]*n), \
                       array('d', [options['e'](a) for a in rnge(averror)]))
            graphs.Add(graph)
            residuals.Add(residual)
        graphs.Write('', TObject.kOverwrite)
        residuals.Write('', TObject.kOverwrite)
    closeRootFile(g, newname)
    closeRootFile(f, oldname)

def numberClusters(scan, fitted='', truncated=False, combine=False, \
                   alternative=False, all=False):
    """Fit pixel cluster number in both directions of a scan"""
    options = {'name': 'nCluster', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': fitted}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if truncated:
        def custom(hist):
            hist.GetXaxis().SetRange(1, 30)
            mini = hist.GetXaxis().GetBinCenter(hist.GetMinimumBin())
            hist.GetXaxis().SetRange(int(mini), 100)
            average = hist.GetMean()
            averror = hist.GetMeanError()
            return average, averror
        options['custom'] = custom
        options['newname'] = 'nClusterT'
        options['fitted'] = ''
    elif fitted:
        def custom(hist):
            average = hist.GetFunction('gaus').GetParameter(1)
            averror = hist.GetFunction('gaus').GetParError(1)
            return average, averror
        options['custom'] = custom
    else:
        options['custom'] = False
    if alternative:
        options['method'] = 'LS'
    collectPerDirectionBx(options)

def numberVertices(scan, combine=False, all=False):
    """Fit vertex number in both directions of a scan"""
    options = {'name': 'nVtx', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': '', 'custom': False}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    collectPerDirectionBx(options)

def vertexTemplate(scan, name, fitted='', combine=False, alternative=False, \
                   all=False, nominalPos=None):
    """Template for fit of vertex positions in both directions of a scan"""
    options = {'name': name, 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': fitted}
    if nominalPos is not None:
        options['nominalPos'] = nominalPos
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if fitted and not 'LS' in fitted:
        def custom(hist):
            average = hist.GetFunction('gaus').GetParameter(1)
            averror = hist.GetFunction('gaus').GetParError(1)
            return average, averror
        options['custom'] = custom
    else:
        options['custom'] = False
    if alternative:
        options['method'] = 'LS'
    collectPerDirectionBx(options)

def vertexPosition(scan, fitted='', combine=False, alternative=False, \
                   all=False):
    """Fit vertex positions in both directions of a scan"""
    vertexTemplate(scan, 'vtxPos', fitted, combine, alternative, all)

def vertexPositionTr(scan, fitted='', combine=False, alternative=False, \
                   all=False):
    """Fit transverse vertex positions in both directions of a scan"""
    if 'X' in scan:
        nominalPos = O['nominalPos'][scan+'y']
    else:
        nominalPos = O['nominalPos'][scan+'x']
    vertexTemplate(scan, 'vtxPosTr', fitted, combine, alternative, all, \
                   nominalPos=nominalPos)

def vertexDistance(scan, fitted='', combine=False, alternative=False, \
                   all=False):
    """Fit vertex distances in both directions of a scan"""
    vertexTemplate(scan, 'vtxDist', fitted, combine, alternative, all)

def vertexPositionSigma(scan, fitted='F', combine=False, all=False):
    """Fit sigma of vertex positions in both directions of a scan"""
    def custom(hist):
        average = hist.GetFunction('gaus').GetParameter(2)
        averror = hist.GetFunction('gaus').GetParError(2)
        return average, averror
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': fitted, \
               'custom': custom, 'newname': 'vtxPosSig'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    collectPerDirectionBx(options)

def counts(scan, combine=False, alternative=False, all=False):
    """Fit counts in both directions of a scan"""
    options = {'name': 'counts', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'custom': False, 'fitted': ''}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] + O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    collectPerDirectionBx(options)
