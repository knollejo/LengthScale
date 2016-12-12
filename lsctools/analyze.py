from config import options as O
from tools import openRootFileR, openRootFileW, closeRootFile, plotName, \
                  plotTitle
from array import array
from ROOT import TMultiGraph, TGraphErrors, TObject

def scale(s=1.0):
    """Generate a function that multiplies the argument with a constant"""
    return lambda a: s*a

def collectPerDirectionBx(options):
    """Fit PCC data in both directions of a scan"""
    nSteps = len(O['nominalPos'][options['scan']])
    for i in range(nSteps):
        if O['nominalPos'][options['scan']][i+1] == \
           O['nominalPos'][options['scan']][i]:
            break
    oldname = options['scan'] + '_' + options['name'] + options['fitted']
    if 'newname' in options:
        newname = options['scan'] + '_' + options['newname'] + \
                  options['fitted'] + '_collected'
    else:
        newname = oldname + '_collected'
    f = openRootFileR(oldname)
    g = openRootFileW(newname)
    crossings = O['crossings'][:]
    if options['combine']:
        crossings.append('all')
    for bx in crossings:
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
                    array('d', [options['x'](a) for a in \
                          rnge(O['nominalPos'][options['scan']])]), \
                    array('d', [options['y'](a) for a in rnge(average)]), \
                    array('d', [0]*n), \
                    array('d', [options['e'](a) for a in rnge(averror)]))
            graph.Fit(options['fit'])
            residual = TGraphErrors(n, \
                       array('d', [options['x'](a) for a in \
                             rnge(O['nominalPos'][options['scan']])]), \
                       array('d', [options['y'](a) - graph.GetFunction( \
                             options['fit']).Eval(options['x'](b)) for a, b \
                             in zip(rnge(average), \
                             rnge(O['nominalPos'][options['scan']]))]),
                       array('d', [0]*n), \
                       array('d', [options['e'](a) for a in rnge(averror)]))
            graphs.Add(graph)
            residuals.Add(residual)
        graphs.Write('', TObject.kOverwrite)
        residuals.Write('', TObject.kOverwrite)
    closeRootFile(g, newname)
    closeRootFile(f, oldname)

def numberCluster(scan, combine=False):
    """Fit pixel cluster number in both directions of a scan"""
    options = {'name': nCluster, 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': '', 'custom': False, \
               'combine': combine}
    collectPerDirectionBx(options)

def numberVertices(scan, combine=False):
    """Fit vertex number in both directions of a scan"""
    options = {'name': nVtx, 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': '', 'custom': False, \
               'combine': combine}
    collectPerDirectionBx(options)

def vertexPosition(scan, fitted='', combine=False):
    """Fit vertex positions in both directions of a scan"""
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': fitted, \
               'combine': combine}
    if fitted:
        def custom(hist):
            average = hist.GetFunction('gaus').GetParameter(1)
            averror = hist.GetFunction('gaus').GetParError(1)
            return average, averror
        options['custom'] = custom
    else:
        options['custom'] = False
    collectPerDirectionBx(options)

def vertexPositionSigma(scan, fitted='F', combine=False):
    """Fit sigma of vertex positions in both directions of a scan"""
    def custom(hist):
        average = hist.GetFunction('gaus').GetParameter(2)
        averror = hist.GetFunction('gaus').GetParError(2)
        return average, averror
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(), 'e': scale(), 'fitted': fitted, \
               'combine': combine, 'custom': custom, 'newname': 'vtxPosSig'}
    collectPerDirectionBx(options)
