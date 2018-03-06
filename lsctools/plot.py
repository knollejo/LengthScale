from config import options as O
from tools import openRootFileR, closeRootFile, plotName, plotPath, \
                  drawSignature
from ROOT import TCanvas, gStyle, TPad, gPad, TLine, TLatex, TLegend

def plotPerBxStep(options):
    """Save histograms (per BX and step) to PDF files"""
    name = options['scan'] + '_' + options['name'] + options['extra']
    if 'method' in options:
        name += '_' + options['method']
    f = openRootFileR(name)
    for bx in options['crossings']:
        for step in range(len(O['nominalPos'][options['scan']])):
            histname = plotName(name+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=False)
            filename = plotName(name+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=True)
            filepath = plotPath(name+'_bx'+str(bx)+'_step'+str(step), \
                                timestamp=True)
            print '<<< Save plot:', filepath
            hist = f.Get(histname)
            canvas = TCanvas()
            canvas.SetLogx(options['logx'])
            canvas.SetLogy(options['logy'])
            gStyle.SetOptStat(options['optstat'])
            gStyle.SetOptFit(options['optfit'])
            hist.Draw()
            gPad.Update()
            hist.GetXaxis().SetTitle(options['xtitle'])
            hist.GetXaxis().SetRangeUser(options['xmin'], options['xmax'])
            hist.GetYaxis().SetTitle(options['ytitle'])
            hist.GetYaxis().SetTitleOffset(1.2)
            for axis in [hist.GetXaxis(), hist.GetYaxis()]:
                axis.SetTitleFont(133)
                axis.SetTitleSize(16)
                axis.SetLabelFont(133)
                axis.SetLabelSize(12)
                axis.CenterTitle()
            stats = hist.FindObject('stats')
            stats.SetTextFont(133)
            stats.SetTextSize(16)
            drawSignature(filename)
            gPad.Modified()
            gPad.Update()
            if 'custom' in options:
                extragraphs = options['custom'](hist)
            canvas.Print(filepath)
            canvas.Close()
    closeRootFile(f, name)

def numberClustersPerBxStep(scan, fit='', combine=False, alternative=False, \
                            all=False):
    """Save cluster number histograms to PDF files"""
    def plotZoom(hist):
        pad = TPad('pad', '', 0.2, 0.55, 0.6, 0.89)
        pad.Draw()
        pad.cd()
        hist2 = hist.Clone()
        hist2.SetTitle('')
        hist2.Draw()
        hist2.GetXaxis().SetRangeUser(10, 100)
        for axis in [hist2.GetXaxis(), hist2.GetYaxis()]:
            axis.SetTitle('')
            axis.SetNdivisions(505)
            axis.SetLabelOffset(0.02)
        hist2.SetStats(False)
        return pad, hist2
    options = {'name': 'nCluster', 'scan': scan, 'xmin': -0.5, 'xmax': 5000.5, \
               'logx': 0, 'logy': 1, 'xtitle': 'Number of Pixel Clusters (per event)', \
               'ytitle': 'Number of Events', 'optstat': 101110, 'optfit': 111, \
               'extra': fit, 'custom': plotZoom}
    if alternative:
        options['method'] = 'LS'
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    plotPerBxStep(options)

def numberVerticesPerBxStep(scan, combine=False, all=False):
    """Save vertex number histograms to PDF files"""
    options = {'name': 'nVtx', 'scan': scan, 'xmin': -0.5, 'xmax': 6.5, 'logx': 0, \
               'logy': 1, 'xtitle': 'Number of Vertices (per event)', \
               'ytitle': 'Number of Events', 'optstat': 1110, 'optfit': 0, \
               'extra': ''}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    plotPerBxStep(options)

def vertexPositionPerBxStep(scan, fit='', combine=False, alternative=False, \
                            all=False):
    """Save vertex position histograms to PDF files"""
    options = {'name': 'vtxPos', 'scan': scan, 'xmin': -1e3, 'xmax':3e3, \
               'logx': 0, 'logy': 0, 'xtitle': 'Measured Vertex Position [#mum]', \
               'ytitle': 'Number of Events','optstat': 1110, 'optfit': 111,
               'extra': fit}
    if alternative:
        options['method'] = 'LS'
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    plotPerBxStep(options)

def countsPerBxStep(scan, fit='', combine=False, all=False):
    """Save counts histograms to PDF files"""
    options = {'name': 'counts', 'scan': scan, 'xmin': -0.5, 'xmax': 599.5, \
               'logx': 0, 'logy': 0, 'xtitle': 'Counts', 'ytitle': 'Number of'+ \
               ' events', 'optstat': 1110, 'optfit': 0, 'extra': ''}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    plotPerBxStep(options)

def plotPerDirectionBx(options):
    """Save directional fit plots (per BX) to PDF files"""
    name = options['scan'] + '_'+ options['name'] + options['fitted']
    if 'method' in options:
        name += '_' + options['method']
    name += '_collected'
    f = openRootFileR(name)
    for bx in options['crossings']:
        plotname = plotName(name+'_bx'+str(bx), timestamp=False)
        filename = plotName(name+'_bx'+str(bx), timestamp=True)
        filepath = plotPath(name+'_bx'+str(bx), timestamp=True)
        print '<<< Save plot:', filepath
        graphs = f.Get(plotname)
        residuals = f.Get(plotname+'_residuals')
        if 'final' in options:
            graphs.SetTitle('')
            residuals.SetTitle('')

        gStyle.SetOptFit(options['optfit'])
        canvas = TCanvas(plotname+'_canvas', '', 700, 600)

        canvas.cd()
        canvas.SetMargin(0.13, 0.03, 0.33, 0.05)

        graphs.Draw('AP')
        gPad.Update()
        text = TLatex()
        text.SetNDC()
        for j, graph in enumerate(graphs.GetListOfGraphs()):
            graph.SetMarkerStyle(21)
            graph.SetMarkerColor(2+2*j)
            graph.GetFunction(options['fit']).SetLineColor(2+2*j)
            stats = graph.GetListOfFunctions().FindObject('stats')
            stats.SetTextColor(2+2*j)
            stats.SetBorderSize(0)
            stats.SetTextSize(0.04)
            inverted = graph.GetFunction(options['fit']).GetParameter('p1')<0.0
            text.SetTextFont(42)
            text.SetTextSize(0.04)
            text.SetTextColor(2+2*j)
            if inverted and j==0:
                text.DrawLatex(0.18,0.54,options['scan']+' scan forward')
                stats.SetX1NDC(0.16)
                stats.SetX2NDC(0.53)
                stats.SetY1NDC(0.38)
                stats.SetY2NDC(0.53)
            elif inverted and j==1:
                text.DrawLatex(0.61,0.9,options['scan']+' scan backward')
                stats.SetX1NDC(0.59)
                stats.SetX2NDC(0.96)
                stats.SetY1NDC(0.74)
                stats.SetY2NDC(0.89)
            elif j==0:
                text.DrawLatex(0.18,0.9,options['scan']+' scan forward')
                stats.SetX1NDC(0.16)
                stats.SetX2NDC(0.53)
                stats.SetY1NDC(0.74)
                stats.SetY2NDC(0.89)
            else:
                text.DrawLatex(0.61,0.54,options['scan']+' scan backward')
                stats.SetX1NDC(0.59)
                stats.SetX2NDC(0.96)
                stats.SetY1NDC(0.38)
                stats.SetY2NDC(0.53)
        graphs.GetXaxis().SetTitle('Nominal Position [#mum]')
        graphs.GetYaxis().SetTitle(options['ytitle'])
        graphs.GetYaxis().SetTitleOffset(1.3)
        if('final' in options):
            text.SetTextColor(1)
            text.SetTextFont(42)
            text.SetTextSize(0.04)
            text.SetTextAlign(31)
            text.DrawLatex(0.97,0.96,O['plotsig'])
            text.SetTextAlign(11)
            if options['final'] == 'wip':
                text.SetTextFont(52)
                text.SetTextSize(0.04)
                text.DrawLatex(0.13,0.96,'Work in Progress')
            else:
                text.SetTextFont(62)
                text.SetTextSize(0.05)
                text.DrawLatex(0.13,0.96,'CMS')
                text.SetTextFont(52)
                text.SetTextSize(0.04)
                text.DrawLatex(0.22,0.96,'Preliminary')
        for axis in [graphs.GetYaxis(), graphs.GetXaxis()]:
            axis.SetTitleSize(0.05)
            axis.SetLabelSize(0.04)
            axis.SetLabelOffset(0.01)
            axis.CenterTitle()

        pad = TPad('pad', 'pad', 0, 0, 1, 0.2)
        pad.Draw()
        pad.cd()
        pad.SetMargin(0.13, 0.03, 0.01, 0.01)
        for j, residual in enumerate(residuals.GetListOfGraphs()):
            residual.SetMarkerStyle(21)
            residual.SetMarkerColor(2+2*j)
        residuals.Draw("AP")
        residuals.GetXaxis().SetLabelSize(0.0)
        residuals.GetXaxis().SetTickSize(0.151)
        residuals.GetYaxis().SetTitle('')
        residuals.GetYaxis().SetNdivisions(305)
        residuals.GetYaxis().SetRangeUser(-0.9,0.9)
        residuals.GetYaxis().SetTickSize(0.019)
        residuals.GetYaxis().SetLabelSize(0.2)
        residuals.GetYaxis().SetLabelOffset(0.01)
        pad.Update()
        line = TLine(pad.GetUxmin(), 0.0, pad.GetUxmax(), 0.0)
        line.SetLineColor(14)
        line.SetLineStyle(3)
        line.Draw()

        canvas.cd()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextAngle(90.0)
        text.DrawLatex(0.035,0.0,'Residuals '+options['restitle'])

        if not 'final' in options:
            drawSignature(filename)
        # canvas.Modified()
        # canvas.Update()
        canvas.Print(filepath)
        canvas.Close()
    closeRootFile(f, name)

def numberClustersPerDirectionBx(scan, fitted='', combine=False, \
                                 alternative=False, all=False, final=False):
    """Save number of clusters directional plots to PDF files"""
    options = {'name': 'nCluster', 'scan': scan, 'fitted': fitted, \
               'optfit': 111, 'fit': 'pol1', 'restitle': '[abs.]', \
               'ytitle': 'Number of Pixel Clusters (per event)'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if alternative:
        options['method'] = 'LS'
    if final:
        options['final'] = final
    plotPerDirectionBx(options)

def numberVerticesPerDirectionBx(scan, fitted='', combine=False, all=False, \
                                 final=False):
    """Save number of vertices directional plots to PDF files"""
    options = {'name': 'nVtx', 'scan': scan, 'fitted': fitted, \
               'optfit': 111, 'fit': 'pol1', 'restitle': '[abs.]', \
               'ytitle': 'Number of Vertices (per event)'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if final:
        options['final'] = final
    plotPerDirectionBx(options)

def vertexPositionPerDirectionBx(scan, fitted='', combine=False, \
                                 alternative=False, all=False, final=False):
    """Save vertex position directional plots to PDF files"""
    options = {'name': 'vtxPos', 'scan': scan, 'fitted': fitted, 'optfit': 111, \
               'fit': 'pol1', 'ytitle': 'Measured Vertex Position [#mum]', \
               'restitle': '[#mum]'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if alternative:
        options['method'] = 'LS'
    if final:
        options['final'] = final
    plotPerDirectionBx(options)

def vertexPositionSigmaPerDirectionBx(scan, fitted='F', combine=False, \
                                      all=False, final=False):
    """Save sigma of vertex position directional plots to PDF files"""
    options = {'name': 'vtxPosSig', 'scan': scan, 'fitted': fitted, \
               'optfit': 111, 'fit': 'pol1', 'restitle': '[#mum]', \
               'ytitle': '#sigma(Measured Vertex Position) [#mum]'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if final:
        options['final'] = final
    plotPerDirectionBx(options)

def countsPerDirectionBx(scan, fitted='', combine=False, all=False, final=False):
    """Save counts directional plots to PDF files"""
    options = {'name': 'counts', 'scan': scan, 'fitted': fitted, 'optfit': 111, \
               'fit': 'pol1', 'restitle': '[abs.]', 'ytitle': 'Counts'}
    if all:
        options['crossings'] = ['all']
    else:
        options['crossings'] = O['crossings'][:]
        if combine:
            options['crossings'].append('all')
    if final:
        options['final'] = final
    plotPerDirectionBx(options)

def plotPerLumiSection(options):
    """Save profile histograms per lumisection to PDF files"""
    name = options['name'] + '_perLS'
    f = openRootFileR(name)
    histname = plotName(options['title']+'_perLS', timestamp=False)
    filename = plotName(options['title']+'_perLS', timestamp=True)
    filepath = plotPath(options['title']+'_perLS', timestamp=True)
    print '<<< Save plot:', filepath
    hist = f.Get(histname)
    canvas = TCanvas()
    canvas.SetLogy(options['logy'])
    gStyle.SetOptStat(options['optstat'])
    hist.Draw()
    gPad.Update()
    hist.GetXaxis().SetTitle('Lumisection')
    hist.GetYaxis().SetTitle(options['ytitle'])
    hist.GetYaxis().SetTitleOffset(1.2)
    for axis in [hist.GetXaxis(), hist.GetYaxis()]:
        axis.SetTitleFont(133)
        axis.SetTitleSize(16)
        axis.SetLabelFont(133)
        axis.SetLabelSize(12)
        axis.CenterTitle()
    drawSignature(filename)
    gPad.Modified()
    gPad.Update()
    #canvas.Print(filepath)
    #canvas.Close()
    #closeRootFile(f, name)
    return [canvas, hist, f]

def vertexPositionPerLumiSection(coordinate):
    """Save vertex position per LS profiles to PDF files"""
    options = {'name': 'vtxPos', 'logy': 0, 'optstat': 0, \
               'title': 'vtxPos'+coordinate, \
               'ytitle': 'Measured Vertex Position in '+coordinate}
    return plotPerLumiSection(options)

def plotPerTimeStamp(options):
    """Save profile histograms per timestamp to PDF files"""
    name = options['name'] + '_' + options['scan'] + '_perTime'
    if options['extra']:
        name += '_' + options['extra']
    f = openRootFileR(options['name']+'_perTime')
    histname = plotName(name, timestamp=False)
    filename = plotName(name, timestamp=True)
    filepath = plotPath(name, timestamp=True)
    print '<<< Save plot:', filepath
    hist = f.Get(histname)
    hist.SetErrorOption(options['error'])
    if options['big']:
        canvas = TCanvas('c', '', 8000, 1200)
    else:
        canvas = TCanvas('c', '', 1400, 500)
    canvas.SetLogy(options['logy'])
    gStyle.SetOptStat(options['optstat'])
    hist.Draw()
    gPad.Update()
    hist.GetXaxis().SetTimeDisplay(1)
    hist.GetXaxis().SetTimeFormat('#splitline{%d.%m.%y}{%H:%M:%S}%F1969-12-31' \
                                  +' 22:00:00')
    hist.GetXaxis().SetLabelOffset(0.03)
    hist.GetXaxis().SetTitle('')
    if 'xmin' in options and 'xmax' in options:
        hist.GetXaxis().SetRangeUser(options['xmin'], options['xmax'])
    hist.GetYaxis().SetTitle(options['ytitle'])
    hist.GetYaxis().SetTitleOffset(1.2)
    for axis in [hist.GetXaxis(), hist.GetYaxis()]:
        axis.SetTitleFont(133)
        axis.SetTitleSize(16)
        axis.SetLabelFont(133)
        axis.SetLabelSize(12)
        axis.CenterTitle()
        if options['big']:
            axis.SetTickLength(0.01)
    if options['big']:
        hist.GetYaxis().SetTitleOffset(0.25)
    drawSignature(filename)
    gPad.Modified()
    gPad.Update()
    if options['retrn']:
        return [canvas, hist, f]
    else:
        canvas.Print(filepath)
        canvas.Close()
        closeRootFile(f, options['name']+'_perTime')

def vertexPositionPerTimeStamp(scan, tmin=-1, tmax=-1, extra='', big=False, \
                               retrn=False):
    """Save vertex position per timestamp profiles to PDF files"""
    options = {'name': 'vtxPos', 'logy': 0, 'optstat': 0, 'name': 'vtxPos', \
               'scan': scan, 'ytitle': 'Measured Vertex Position', \
               'error': '', 'extra': extra, 'big': big, 'retrn': retrn}
    if tmin > 0 and tmax > 0:
        options['xmin'] = tmin
        options['xmax'] = tmax
    return plotPerTimeStamp(options)
