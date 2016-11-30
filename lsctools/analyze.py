from config import options as O, EOSPATH as eos
from tools import plotName, plotTitle, dataDir, dataName, loadFiles
from os import listdir
import ROOT

def chain(filelist, scan, tree):
    """Create chain of all files belonging to a scan"""
    files = loadFiles(filelist)
    chain = ROOT.TChain(tree)
    for filename in files[scan]:
        chain.Add(eos+'/'+filename)
    return chain

def miniCondition(scan, bx, step):
    return 'timeStamp >= ' + str(O['begin'][scan][step]) + \
           ' && timeStamp <= ' + str(O['end'][scan][step]) + \
           ' && BXid == ' + str(bx)

def doPerBxStep(options):
    c = chain(options['filelist'], options['scan'], options['tree'])
    nSteps = len(O['nominalPos'][options['scan']])
    nCross = len(O['crossings'])
    fname = dataDir() + '/' + dataName(options['scan']+'_'+options['name']) \
            + '.root'
    print '<<<< Open file:', fname
    f = ROOT.TFile(fname, 'RECREATE')
    for i, bx in enumerate(O['crossings']):
        for step in range(nSteps):
            print '<<<< Analyze:', options['scan'], bx, 'step', step
            histname = plotName(options['scan']+'_'+options['name']+'_bx'+\
                                str(bx)+'_step'+str(step))
            histtitl = plotTitle(options['scan']+' BX '+str(bx)+', Step '+\
                                str(step))
            hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
            hist.StatOverflows(True)
            c.Draw(options['field'](options['scan'])+'>>'+histname, \
                   options['condition'](options['scan'], bx, step), 'goff')
            hist.Write()
    print '<<<< Close file:', fname
    f.Close()
    return fname

def numberClusters(scan, filelist):
    def field(s):
        return 'nCluster'
    options = {'min': 0, 'max': 1000, 'bin': 1000, 'histo': ROOT.TH1I, \
               'tree': 'pccminitree', 'name': 'nCluster', 'field': field, \
               'condition': miniCondition, 'scan': scan, \
               'filelist': filelist}
    return doPerBxStep(options)

def numberVertices(scan, filelist):
    def field(s):
        return 'nVtx'
    options = {'min': 0, 'max': 10, 'bin': 10, 'histo': ROOT.TH1I, \
               'tree': 'pccminitree', 'name': 'nVtx', 'field': field, \
               'condition': miniCondition, 'scan': scan, 'filelist': filelist}
    return doPerBxStep(options)

def vertexPosition(scan, filelist):
    def field(s):
        if 'X' in scan:
            return 'vtx_x'
        else:
            return 'vtx_y'
    def condition(s, bx, step):
        return 'timeStamp_begin >= ' + str(O['begin'][s][step]) + \
               ' && timeStamp_begin <= ' + str(O['end'][s][step]) + \
               ' && vtx_isGood && bunchCrossing == ' + str(bx)
    options = {'min': -0.3, 'max': 0.3, 'bin': 500, 'histo': ROOT.TH1F, \
               'tree': 'lumi/tree', 'name': 'vtxPos', 'field': field, \
               'condition': condition, 'scan': scan, 'filelist': filelist}
    return doPerBxStep(options)
