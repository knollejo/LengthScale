from config import options as O
from tools import plotName, openRootFileU, openRootFileW, closeRootFile, \
                  loadFiles
import ROOT

def fitPerBxStep(options):
    nSteps = len(O['nominalPos'][options['scan']])
    name = options['scan']+'_'+options['name']
    if options['fitopt']:
        extra = options['fitopt']
    else:
        extra = 'F'
    f = openRootFileU(name)
    g = openRootFileW(name+extra)
    for bx in O['crossings']:
        for step in range(nSteps):
            print '<<<< Fit:', options['scan'], bx, 'step', step
            histname = plotName(options['scan']+'_'+options['name']+'_bx'+\
                                str(bx)+'_step'+str(step), timestamp=False)
            newname = plotName(options['scan']+'_'+options['name']+extra+'_bx'+\
                               str(bx)+'_step'+str(step), timestamp=False)
            hist = f.Get(histname)
            hist.SetName(newname)
            hist.Fit(options['fit'], options['fitopt'])
            hist.Write('', ROOT.TObject.kOverwrite)
    closeRootFile(g, name+extra)
    closeRootFile(f, name)

def vertexPosition(scan, fitmethod='F'):
    options = {'name': 'vtxPos', 'scan': scan, 'fit': 'gaus'}
    if fitmethod == 'L':
        options['fitopt'] = 'L'
    else:
        options['fitopt'] = ''
    fitPerBxStep(options)
