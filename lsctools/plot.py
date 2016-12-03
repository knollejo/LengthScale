from config import options as O
from tools import openRootFileR, closeRootFile, plotName, plotPath
import ROOT

def plotPerBxStep(options):
    nSteps = len(O['nominalPos'][options['scan']])
    name = options['scan'] + '_' + options['name'] + options['extra']
    f = openRootFileR(name)
    for bx in O['crossings']:
        for step in range(nSteps):
            histname = plotName(options['scan']+'_'+options['name']+\
                                options['extra']+'_bx'+str(bx)+'_step'+\
                                str(step), timestamp=False)
            filename = plotPath(options['scan']+'_'+options['name']+\
                                options['extra']+'_bx'+str(bx)+'_step'+\
                                str(step), timestamp=True)
            print '<<<< Save plot:', filename
            hist = f.Get(histname)
            canvas = ROOT.TCanvas()
            canvas.SetLogx(options['logx'])
            canvas.SetLogy(options['logy'])
            ROOT.gStyle.SetOptStat(options['optstat'])
            ROOT.gStyle.SetOptFit(options['optfit'])
            hist.Draw()
            hist.GetXaxis().SetTitle(options['xtitle'])
            hist.GetXaxis().SetRangeUser(options['xmin'], options['xmax'])
            hist.GetYaxis().SetTitle(options['ytitle'])
            canvas.Print(filename)
            canvas.Close()
    closeRootFile(f, name)

def numberVerticesPerBxStep(scan):
    options = {'name': 'nVtx', 'scan': scan, 'xmin': -0.5, 'xmax': 6.5, 'logx': 0, \
               'logy': 1, 'xtitle': 'Number of Vertices', \
               'ytitle': 'Number of Events', 'optstat': 1110, 'optfit': 0, \
               'extra': ''}
    plotPerBxStep(options)

def vertexPositionPerBxStep(scan, fit=''):
    options = {'name': 'vtxPos', 'scan': scan, 'xmin': -0.1, 'xmax': 0.3, \
               'logx': 0, 'logy': 0, 'xtitle': 'Measured Vertex Position [#mum]', \
               'ytitle': 'Number of Events','optstat': 1110, 'optfit': 101,
               'extra': fit}
    plotPerBxStep(options)

def plotPerDirectionBx(options):
    name = options['scan'] + '_'+ options['name'] + options['fitted'] \
           + '_collected'
    f = openRootFileR(name)
    for bx in O['crossings']:
        plotname = plotName(name+'_bx'+str(bx), timestamp=False)
        filename = plotPath(name+'_bx'+str(bx), timestamp=True)
        print '<<<< Save plot:', filename
        graphs = f.Get(plotname)
        residuals = f.Get(plotname+'_residuals')
        
        ROOT.gStyle.SetOptFit(options['optfit'])
        canvas = ROOT.TCanvas()
        canvas.cd()
        pad1 = ROOT.TPad('pad1', 'pad1', 0, 0.3, 1, 1)
        pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 0.3)
        pad1.Draw()
        pad2.Draw()
        
        pad1.cd()
        ROOT.gPad.SetMargin(0.1, 0.01, 0.0, 0.3)
        graphs.Draw('AP')
        ROOT.gPad.Update()
        for j, graph in enumerate(graphs.GetListOfGraphs()):
            graph.SetMarkerStyle(21)
            graph.SetMarkerColor(2+2*j)
            stats = graph.GetListOfFunctions().FindObject('stats')
            stats.SetTextColor(2+2*j)
            stats.SetX1NDC(0.1+0.5*j)
            stats.SetX2NDC(0.40+0.5*j)
            stats.SetY1NDC(0.72)
            stats.SetY2NDC(0.88)
            graph.GetFunction(options['fit']).SetLineColor(2+2*j)
        graphs.GetYaxis().SetTitle(options['ytitle'])
        
        pad2.cd()
        ROOT.gPad.SetMargin(0.1, 0.01, 0.3, 0.0)
        for j, residual in enumerate(residuals.GetListOfGraphs()):
            residual.SetMarkerStyle(21)
            residual.SetMarkerColor(2+2*j)
        residuals.Draw("AP")
        residuals.GetXaxis().SetTitle('Nominal Position [#mum]')
        residuals.GetYaxis().SetTitle('Residuals')
        residuals.GetXaxis().SetTitleOffset(3)
        residuals.GetXaxis().SetLabelOffset(0.02)
        residuals.GetYaxis().SetNdivisions(305)
        ROOT.gPad.Update()
        line = ROOT.TLine(pad2.GetUxmin(), 0.0, pad2.GetUxmax(), 0.0)
        line.SetLineColor(14)
        line.SetLineStyle(3)
        line.Draw()
        
        for axis in [graphs.GetYaxis(), residuals.GetXaxis(), \
                     residuals.GetYaxis()]:
            axis.SetTitleFont(133)
            axis.SetTitleSize(16)
            axis.SetLabelFont(133)
            axis.SetLabelSize(12)
            axis.CenterTitle()
        
        for pad in [pad1, pad2]:
            pad.Modified()
            pad.Update()
        
        canvas.cd()
        canvas.Print(filename)
        canvas.Close()
    closeRootFile(f, name)

def vertexPositionPerDirectionBx(scan, fitted=''):
    options = {'name': 'vtxPos', 'scan': scan, 'fitted': fitted, 'optfit': 111, \
               'fit': 'pol1', 'ytitle': 'Measured Vertex Position [#mum]'}
    plotPerDirectionBx(options)
