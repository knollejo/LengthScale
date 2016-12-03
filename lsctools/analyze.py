from config import options as O
from tools import openRootFileR, openRootFileW, closeRootFile, plotName, \
                  plotTitle
from array import array

import ROOT

def scale(s=1.0):
    return lambda a: s*a

def collectPerDirectionBx(options):
    nSteps = len(O['nominalPos'][options['scan']])
    for i in range(nSteps):
        if O['nominalPos'][options['scan']][i+1] == \
           O['nominalPos'][options['scan']][i]:
            break
    name = options['scan']+'_'+options['name']+options['fitted']
    f = openRootFileR(name)
    g = openRootFileW(name+'_collected')
    for bx in O['crossings']:
        average = [0 for j in range(nSteps)]
        averror = [0 for j in range(nSteps)]
        for step in range(nSteps):
            print 'Access:', options['scan'], bx, 'step', step
            histname = plotName(name+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=False)
            hist = f.Get(histname)
            if options['custom']:
                average[step], averror[step] = options['custom'](hist)
            else:
                average[step] = hist.GetMean()
                averror[step] = hist.GetMeanError()
        plotname = plotName(name+'_collected_bx'+str(bx), timestamp=False)
        plottitl = plotTitle(options['scan']+' BX '+str(bx))
        print '<<<< Create plot:', plotname
        graphs = ROOT.TMultiGraph(plotname, plottitl)
        residuals = ROOT.TMultiGraph(plotname+'_residuals', '')
        def range1(l):
            return l[:i+1]
        def range2(l):
            return l[i+1:]
        for n, rnge in zip([i+1, nSteps-i-1], [range1, range2]):
            graph = ROOT.TGraphErrors(n, \
                    array('d', [options['x'](a) for a in \
                          rnge(O['nominalPos'][options['scan']])]), \
                    array('d', [options['y'](a) for a in rnge(average)]), \
                    array('d', [0]*n), \
                    array('d', [options['e'](a) for a in rnge(averror)]))
            graph.Fit(options['fit'])
            residual = ROOT.TGraphErrors(n, \
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
        graphs.Write('', ROOT.TObject.kOverwrite)
        residuals.Write('', ROOT.TObject.kOverwrite)
    closeRootFile(g, name+'collected')
    closeRootFile(f, name)

def vertexPosition(scan, fitted=''):
    def custom(hist):
        average = hist.GetFunction('gaus').GetParameter(1)
        averror = hist.GetFunction('gaus').GetParError(1)
        return average, averror
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'pol1', 'x': scale(), \
               'y': scale(1e4), 'e': scale(1e4), 'fitted': fitted}
    if fitted:
        options['custom'] = custom
    else:
        options['custom'] = False
    collectPerDirectionBx(options)
