from config import options as O
from tools import plotName, openRootFileU, openRootFileW, closeRootFile
from ROOT import TObject

def fitPerBxStep(options):
    """Fit histograms (per BX and step) with a function"""
    name = options['scan']+'_'+options['name']
    if options['fitopt']:
        extra = options['fitopt']
    else:
        extra = 'F'
    if options['range']:
        extra = extra + 'R'
    f = openRootFileU(name)
    g = openRootFileW(name+extra)
    crossings = O['crossings'][:]
    if options['combine']:
        crossings.append('all')
    for bx in crossings:
        for step in range(len(O['nominalPos'][options['scan']])):
            print '<<< Fit:', options['scan'], bx, 'step', step
            histname = plotName(options['scan']+'_'+options['name']+'_bx'+\
                                str(bx)+'_step'+str(step), timestamp=False)
            newname = plotName(options['scan']+'_'+options['name']+extra+'_bx'+\
                               str(bx)+'_step'+str(step), timestamp=False)
            hist = f.Get(histname)
            hist.SetName(newname)
            if options['range']:
                hist.Fit(options['fit'], options['fitopt'], '', \
                         options['rangemin'](hist), options['rangemax'](hist))
            else:
                hist.Fit(options['fit'], options['fitopt'])
            hist.Write('', TObject.kOverwrite)
    closeRootFile(g, name+extra)
    closeRootFile(f, name)

def vertexPosition(scan, fitmethod='F', combine=False):
    """Fit vertex position with a Gaussian (standard or log-likelihood)"""
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'gaus', \
               'combine': combine}
    if fitmethod.startswith('L'):
        options['fitopt'] = 'L'
    else:
        options['fitopt'] = ''
    if fitmethod.endswith('R'):
        options['range'] = True
        options['rangemin'] = lambda hist: hist.GetMean()-2*hist.GetRMS()
        options['rangemax'] = lambda hist: hist.GetMean()+2*hist.GetRMS()
    else:
        options['fit'] = 'gaus'
        options['range'] = False
    fitPerBxStep(options)
