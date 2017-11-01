from config import options as O
from tools import plotName, openRootFileU, openRootFileW, closeRootFile
from ROOT import TObject

def fitPerBxStep(options):
    """Fit histograms (per BX and step) with a function"""
    oldname = options['scan']+'_'+options['name']
    newname = oldname + options['extra']
    if 'method' in options:
        oldname += '_' + options['method']
        newname += '_' + options['method']
    f = openRootFileU(oldname)
    g = openRootFileW(newname)
    for bx in options['crossings']:
        for step in range(len(O['nominalPos'][options['scan']])):
            print '<<< Fit:', options['scan'], bx, 'step', step
            histname = plotName(oldname+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=False)
            histnew = plotName(newname+'_bx'+str(bx)+'_step'+str(step), \
                               timestamp=False)
            hist = f.Get(histname)
            hist.SetName(histnew)
            if options['range']:
                mini, maxi = options['range'](hist)
                hist.Fit(options['fit'], options['fitopt'], '', mini, maxi)
            else:
                hist.Fit(options['fit'], options['fitopt'])
            hist.Write('', TObject.kOverwrite)
    closeRootFile(g, newname)
    closeRootFile(f, oldname)

def numberClusters(scan, fitmethod='F', combine=False, alternative=False, \
                   all=False):
    """Fit number of clusters with a Gaussian in a range"""
    def getRange(hist):
        hist.GetXaxis().SetRange(1, 30)
        mini = hist.GetXaxis().GetBinCenter(hist.GetMinimumBin())
        hist.GetXaxis().SetRange(int(mini), 1000)
        maxi = hist.GetXaxis().GetBinCenter(hist.GetMaximumBin())
        return mini, 2 * maxi - mini
    options = {'name': 'nCluster', 'scan': scan, 'fit': 'gaus', 'extra': 'F', \
               'fitopt': '', 'range': getRange}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if alternative:
        options['method'] = 'LS'
    fitPerBxStep(options)

def vertexPosition(scan, fitmethod='F', combine=False, alternative=False, \
                   all=False):
    """Fit vertex position with a Gaussian (standard or log-likelihood)"""
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'gaus'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if fitmethod.startswith('L'):
        options['fitopt'] = 'L'
        options['extra'] = 'L'
    else:
        options['fitopt'] = ''
        options['extra'] = 'F'
    if fitmethod.endswith('R'):
        def getRange(hist):
            mean = hist.GetMean()
            rms = hist.GetRMS()
            return mean - 2 * rms, mean + 2 * rms
        options['range'] = getRange
        options['extra'] += 'R'
    else:
        options['range'] = False
    if alternative:
        options['method'] = 'LS'
    fitPerBxStep(options)
