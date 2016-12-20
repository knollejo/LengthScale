from config import options as O
from tools import openRootFileR, plotName

def num(value, error, form='{}'):
    return '\\num{' + form.format(value) + ' \\pm ' + \
           form.format(error) + '}'

def extractPerDirectionBx(options):
    """Extract results from directional fits (per BX)"""
    name = options['scan'] + '_'+ options['name'] + options['fitted'] \
           + '_collected'
    f = openRootFileR(name)
    crossings = O['crossings'][:]
    if options['combine']:
        crossings.append('all')
    average = dict(zip(crossings, [[0, 0] for i in range(len(crossings))]))
    averror = dict(zip(crossings, [[0, 0] for i in range(len(crossings))]))
    def extract(graph):
        func = graph.GetFunction(options['fit'])
        return func.GetParameter(options['parameter']), \
               func.GetParError(options['parameter'])
    for bx in crossings:
        plotname = plotName(name+'_bx'+str(bx), timestamp=False)
        print '<<< Access plot:', plotname
        graphs = f.Get(plotname)
        for j, graph in enumerate(graphs.GetListOfGraphs()):
            average[bx][j], averror[bx][j] = extract(graph)
    return average, averror

def makeTexTablePerDirectionBx(average, averror, options):
    """Output results to LaTeX code"""
    form = options['format']
    s = '\\begin{tabular}{lrrrr}\n'
    s += '\t\\bfseries ' + options['scan'] + ' & \\bfseries forward & ' + \
          '\\bfseries backward & \\bfseries difference \\\\\n'
    s += '\t\\hline\n'
    for bx in O['crossings']:
        difference = abs(average[bx][0] - average[bx][1])
        differror = (averror[bx][0] ** 2 + averror[bx][1] ** 2) ** 0.5
        s += '\t\\bfseries ' + str(bx)
        for i in range(2):
            s += ' & ' + num(average[bx][i], averror[bx][i], form)
        s += ' & ' + num(difference, differror, form) + ' \\\\\n'
    s += '\t\\hline\n'
    av = [sum([average[bx][i] * averror[bx][i] ** -2 for bx in O['crossings']]) \
          / sum([averror[bx][i] ** -2 for bx in O['crossings']]) for i in \
          range(2)]
    er = [sum([averror[bx][i] ** -2 for bx in O['crossings']]) ** -0.5 for i \
          in range(2)]
    s += '\t\\bfseries average & '+ num(av[0], er[0], form) + ' & ' + \
         num(av[1], er[1], form) + ' & \\\\\n'
    if(options['combine']):
        s += '\t\\bfseries inclusive'
        for i in range(2):
            s += ' & ' + num(average['all'][i], averror['all'][i], form)
        s += ' & \\\\\n'
    s += '\\end{tabular}'
    return s

def makeTexTablePerDirectionBxComparison(average1, averror1, average2, averror2, \
                                         options):
    """Output results of two different fits to LaTex code"""
    form = options['format']
    s = '\\begin{tabular}{lrrrr}\n'
    s += '\t\\multirow{2}{*}{\\bfseries ' + options['scan'] + '} & ' + \
         '\\multicolumn{2}{c}{\\bfseries ' + options['title1'] + '} & ' + \
         '\\multicolumn{2}{c}{\\bfseries ' + options['title2'] + '} \\\\\n'
    s += '\t& \\bfseries forward & \\bfseries backward & \\bfseries ' + \
         'forward & \\bfseries backward \\\\\n'
    s += '\t\\hline\n'
    for bx in O['crossings']:
        s += '\t\\bfseries ' + str(bx)
        for average, averror in [(average1, averror1), (average2, averror2)]:
            for i in range(2):
                s += ' & ' + num(average[bx][i], averror[bx][i], form)
        s += ' \\\\\n'
    s += '\t\\hline\n'
    s += '\t\\bfseries average'
    for average, averror in [(average1, averror1), (average2, averror2)]:
        av = [sum([average[bx][i] * averror[bx][i] ** -2 for bx in \
              O['crossings']]) / sum([averror[bx][i] ** -2 for bx in \
              O['crossings']]) for i in range(2)]
        er = [sum([averror[bx][i] ** -2 for bx in O['crossings']]) ** -0.5 for \
              i in range(2)]
        s += ' & ' + num(av[0], er[0], form) + ' & ' + num(av[1], er[1], form)
    s += ' \\\\\n'
    if(options['combine']):
        s += '\t\\bfseries inclusive'
        for average, averror in [(average1, averror1), (average2, averror2)]:
            for i in range(2):
                s += ' & ' + num(average['all'][i], averror['all'][i], form)
        s += ' \\\\\n'
    s += '\\end{tabular}'
    return s

def numberClustersTexTable(scan, fitted='', combined=False):
    options = {'scan': scan, 'name': 'nCluster', 'fitted': fitted, \
               'fit': 'pol1', 'parameter': 1, 'combine': combined, \
               'format': '{:.4f}'}
    average, averror = extractPerDirectionBx(options)
    if fitted:
        options['fitted'] = ''
        options['title1'] = 'without fit'
        options['title2'] = 'fitted'
        averag1, averro1 = extractPerDirectionBx(options)
        return makeTexTablePerDirectionBxComparison(averag1, averro1, average, \
                                                    averror, options)
    else:
        return makeTexTablePerDirectionBx(average, averror, options)

def vertexPositionTexTable(scan, fitted='', combined=False):
    options = {'scan': scan, 'name': 'vtxPos', 'fitted': fitted, 'fit': 'pol1', \
               'parameter': 1, 'combine': combined, 'format': '{:.4f}'}
    average, averror = extractPerDirectionBx(options)
    return makeTexTablePerDirectionBx(average, averror, options)

def epsilonFactorTexTable(scan, combined=False):
    options = {'scan': scan, 'fit': 'pol1', 'format': '{:.4f}', \
               'combine': combined, 'title1': 'Number of Clusters', \
               'title2': 'Number of Vertices'}
    options['name'] = 'nCluster'
    options['parameter'] = 0
    nClusterp0, nClusterp0e = extractPerDirectionBx(options)
    options['parameter'] = 1
    nClusterp1, nClusterp1e = extractPerDirectionBx(options)
    options['name'] = 'nVtx'
    options['parameter'] = 0
    nVtxp0, nVtxp0e = extractPerDirectionBx(options)
    options['parameter'] = 1
    nVtxp1, nVtxp1e = extractPerDirectionBx(options)
    if 'X' in scan:
        s0 = 130.0
    else:
        s0 = 120.0
    sigmaeff = 80.0
    nClustereps = [[-p1/p0*sigmaeff**2/s0 \
                    for p0, p1 in zip(nClusterp0[bx], nClusterp1[bx])] \
                   for bx in nClusterp0]
    nClustererr = [[abs(p1/p0*sigmaeff**2/s0)*((p0e/p0)**2+(p1e/p1)**2)**0.5 \
                    for p0, p0e, p1, p1e in zip(nClusterp0[bx], \
                    nClusterp0e[bx], nClusterp1[bx], nClusterp1e[bx])] \
                   for bx in nClusterp0]
    nVtxeps = [[-p1/p0*sigmaeff**2/s0 \
                    for p0, p1 in zip(nVtxp0[bx], nVtxp1[bx])] \
                   for bx in nVtxp0]
    nVtxerr = [[abs(p1/p0*sigmaeff**2/s0)*((p0e/p0)**2+(p1e/p1)**2)**0.5 \
                    for p0, p0e, p1, p1e in zip(nVtxp0[bx], \
                    nVtxp0e[bx], nVtxp1[bx], nVtxp1e[bx])] \
                   for bx in nVtxp0]
    return makeTexTablePerDirectionBxComparison(nClustereps, nClustererr, \
                                                nVtxeps, nVtxerr, options)
