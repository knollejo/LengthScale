from config import options as O
from tools import plotTitle, plotName, plotDir, loadResults
from array import array
import ROOT

def plotFitPerDirectionPerBx(results, options, x, y, e, save=False):
    average, averror = loadResults(results)
    scan = options['scan']
    nSteps = len(O['nominalPos'][scan])
    bxid = O['crossings'][options['bxno']]
    for i in range(nSteps):
        if O['nominalPos'][scan][i+1] == O['nominalPos'][scan][i]:
            break
    plotname = plotName(scan + '_' + options['name'] + '_fit_bx' + str(bxid))
    plottitl = plotTitle(scan + ' BX ' + str(bxid))
    print '<<<< Create plot:', plotname
    ROOT.gStyle.SetOptFit(111)
    
    graph1 = ROOT.TGraphErrors(i+1, 
             array('d', [x(a) for a in O['nominalPos'][scan][:i+1]]), \
             array('d', [y(a) for a in average[bxid][:i+1]]), \
             array('d', [0]*(i+1)), \
             array('d', [e(a) for a in averror[bxid][:i+1]]))
    graph2 = ROOT.TGraphErrors(nSteps-i-1, \
             array('d', [x(a) for a in O['nominalPos'][scan][i+1:]]), \
             array('d', [y(a) for a in average[bxid][i+1:]]), \
             array('d', [0]*(nSteps-i-1)), \
             array('d', [e(a) for a in averror[bxid][i+1:]]))
    graphs = ROOT.TMultiGraph(plotname+'_graphs', plottitl)
    for graph in [graph1, graph2]:
        graph.Fit(options['fit'])
        graphs.Add(graph)
    
    res1 = [y(a) - graph1.GetFunction(options['fit']).Eval(x(b)) for a, b in \
            zip(average[bxid][:i+1], O['nominalPos'][scan][:i+1])]
    res2 = [y(a) - graph2.GetFunction(options['fit']).Eval(x(b)) for a, b in \
            zip(average[bxid][i+1:], O['nominalPos'][scan][i+1:])]
    residual1 = ROOT.TGraphErrors(i+1, \
                array('d', [x(a) for a in O['nominalPos'][scan][:i+1]]), \
                array('d', res1), array('d', [0]*(i+1)), \
                array('d', [e(a) for a in averror[bxid][:i+1]]))
    residual2 = ROOT.TGraphErrors(nSteps-i-1, \
                array('d', [x(a) for a in O['nominalPos'][scan][i+1:]]), \
                array('d', res2), array('d', [0]*(nSteps-i-1)), \
                array('d', [e(a) for a in averror[bxid][i+1:]]))
    residuals = ROOT.TMultiGraph(plotname+'_residuals', '')
    for residual in [residual1, residual2]:
        residuals.Add(residual)
    
    canvas = ROOT.TCanvas(plotname)
    canvas.cd()
    pad1 = ROOT.TPad('pad1', 'pad1', 0, 0.3, 1, 1)
    pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 0.3)
    pad1.Draw()
    pad2.Draw()
    
    pad1.cd()
    ROOT.gPad.SetMargin(0.1, 0.01, 0.0, 0.3)
    graphs.Draw("AP")
    ROOT.gPad.Update()
    for j, graph in enumerate([graph1, graph2]):
        graph.SetMarkerStyle(21)
        graph.SetMarkerColor(2+2*j)
        stats = graph.GetListOfFunctions().FindObject('stats')
        stats.SetTextColor(2+2*j)
        stats.SetX1NDC(0.1+0.5*j)
        stats.SetX2NDC(0.49+0.5*j)
        stats.SetY1NDC(0.72)
        stats.SetY2NDC(0.88)
        graph.GetFunction(options['fit']).SetLineColor(2+2*j)
    graphs.GetYaxis().SetTitle(options['ytitle'])
    
    pad2.cd()
    ROOT.gPad.SetMargin(0.1, 0.01, 0.3, 0.0)
    for j, residual in enumerate([residual1, residual2]):
        residual.SetMarkerStyle(21)
        residual.SetMarkerColor(2+2*j)
    residuals.Draw("AP")
    residuals.GetXaxis().SetTitle('Nominal Position [#mum]')
    residuals.GetYaxis().SetTitle('Residuals')
    residuals.GetXaxis().SetTitleOffset(3)
    residuals.GetXaxis().SetLabelOffset(0.02)
    residuals.GetYaxis().SetNdivisions(305)
    pad2.Update()
    line = ROOT.TLine(pad2.GetUxmin(), 0.0, pad2.GetUxmax(), 0.0)
    line.SetLineColor(14)
    line.SetLineStyle(3)
    line.Draw()
    
    for axis in [graphs.GetYaxis(), residuals.GetXaxis(), residuals.GetYaxis()]:
        axis.SetTitleFont(133)
        axis.SetTitleSize(16)
        axis.SetLabelFont(133)
        axis.SetLabelSize(12)
        axis.CenterTitle()
    
    for pad in [pad1, pad2]:
        pad.Modified()
        pad.Update()
    
    canvas.cd()
    if save:
        outputfile = plotDir() + '/' + plotname + '.pdf'
        print '<<<< Save plot:', outputfile
        canvas.Print(outputfile)
        canvas.Close()
    return canvas, [graphs, residuals, line]

def numberClusterPerBx(scan, bxno, results, name, save=False):
    options = {'scan': scan, 'bxno': bxno, 'name': 'nCluster_'+name, \
               'fit': 'pol1', 'ytitle': 'Average Number of Pixel Clusters'}
    def x(a):
        return a
    return plotFitPerDirectionPerBx(results, options, x, x, x, save)

def vertexPositionPerBx(scan, bxno, results, name, save=False):
    options = {'scan': scan, 'bxno': bxno, 'name': 'vtxPos_'+name, \
               'fit': 'pol1', 'ytitle': 'Measured Vertex Position [#mum]'}
    def x(a):
        return a
    def y(a):
        return 1e4 * a
    return plotFitPerDirectionPerBx(results, options, x, y, y, save)

def numberVerticesPerBx(scan, bxno, results, name, save=False):
    options = {'scan': scan, 'bxno': bxno, 'name': 'nVtx_'+name, \
               'fit': 'pol1', 'ytitle': 'Average Number of Vertices'}
    def x(a):
        return a
    return plotFitPerDirectionPerBx(results, options, x, x, x, save)
