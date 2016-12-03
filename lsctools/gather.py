from config import options as O, EOSPATH as eos
from tools import plotName, plotTitle, openRootFileW, closeRootFile, loadFiles
from os import listdir, stat
import ROOT

def chain(fileset, scan):
    """Create chain of all files belonging to a scan"""
    files = loadFiles(fileset)
    chain = ROOT.TChain(O['treename'][fileset])
    for filename in files[scan]:
        chain.Add(eos+'/'+filename)
    return chain

def miniCondition(scan, bx, step):
    """Create condition that event in a minitree belongs to a step and BX"""
    return 'timeStamp >= ' + str(O['begin'][scan][step]) + \
           ' && timeStamp <= ' + str(O['end'][scan][step]) + \
           ' && BXid == ' + str(bx)

def pccPerBxStep(options):
    c = chain(options['fileset'], options['scan'])
    nSteps = len(O['nominalPos'][options['scan']])
    nCross = len(O['crossings'])
    name = options['scan']+'_'+options['name']
    f = openRootFileW(name)
    for i, bx in enumerate(O['crossings']):
        for step in range(nSteps):
            print '<<<< Analyze:', options['scan'], bx, 'step', step
            histname = plotName(options['scan']+'_'+options['name']+'_bx'+\
                                str(bx)+'_step'+str(step), timestamp=False)
            histtitl = plotTitle(options['scan']+' BX '+str(bx)+', Step '+\
                                str(step))
            hist = options['histo'](histname, histtitl, options['bin'], \
                                    options['min'], options['max'])
            hist.StatOverflows(True)
            c.Draw(options['field'](options['scan'])+'>>'+histname, \
                   options['condition'](options['scan'], bx, step), 'goff')
            hist.Write()
    closeRootFile(f, name)

def numberClusters(scan):
    def field(s):
        return 'nCluster'
    options = {'min': 0, 'max': 1000, 'bin': 1000, 'histo': ROOT.TH1I, \
               'name': 'nCluster', 'field': field, 'condition': miniCondition, \
               'scan': scan, 'fileset': 'minitrees'}
    pccPerBxStep(options)

def numberVertices(scan):
    def field(s):
        return 'nVtx'
    options = {'min': -0.5, 'max': 9.5, 'bin': 10, 'histo': ROOT.TH1I, \
               'name': 'nVtx', 'field': field, 'condition': miniCondition, \
               'scan': scan, 'fileset': 'minitrees'}
    pccPerBxStep(options)

def vertexPosition(scan):
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
               'name': 'vtxPos', 'field': field, 'condition': condition, \
               'scan': scan, 'fileset': 'fulltrees'}
    pccPerBxStep(options)
