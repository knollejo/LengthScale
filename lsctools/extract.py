from config import options as O
from tools import openRootFileR, plotName

def si(value, error, form='{}'):
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
    for bx in crossings:
        plotname = plotName(name+'_bx'+str(bx), timestamp=False)
        print '<<< Access plot:', plotname
        graphs = f.Get(plotname)
        for j, graph in enumerate(graphs.GetListOfGraphs()):
            function = graph.GetFunction(options['fit'])
            average[bx][j] = function.GetParameter(options['parameter'])
            averror[bx][j] = function.GetParError(options['parameter'])
    return average, averror

def makeTexTablePerDirectionBx(average, averror, options):
    """Output results to LaTeX code"""
    form = options['format']
    s = '\\begin{tabular}{lccc}\n'
    s += '\t\\bfseries ' + options['scan'] + ' & \\bfseries forward & ' + \
          '\\bfseries backward & \\bfseries difference \\\\\n'
    s += '\t\\hline\n'
    for bx in O['crossings']:
        difference = abs(average[bx][0] - average[bx][1])
        differror = (averror[bx][0] ** 2 + averror[bx][1] ** 2) ** 0.5
        s += '\t\\bfseries ' + str(bx)
        for i in range(2):
            s += ' & ' + si(average[bx][i], averror[bx][i], form)
        s += ' & ' + si(difference, differror, form) + ' \\\\\n'
    s += '\t\\hline\n'
    av = [sum([average[bx][i] * averror[bx][i] ** -2 for bx in O['crossings']]) \
          / sum([averror[bx][i] ** -2 for bx in O['crossings']]) for i in \
          range(2)]
    er = [sum([averror[bx][i] ** -2 for bx in O['crossings']]) ** -0.5 for i \
          in range(2)]
    s += '\t\t average & '+ si(av[0], er[0], form) + ' & ' + \
         si(av[1], er[1], form) + ' & \\\\\n'
    if(options['combine']):
        s += '\t\bfseries inclusive'
        for i in range(2):
            s += ' & ' + si(average['all'][i], averror['all'][i], form)
        s += ' & \\\\\n'
    s += '\\end{tabular}'
    return s

def vertexPositionTexTable(scan, fitted='', combined=False):
    options = {'scan': scan, 'name': 'vtxPos', 'fitted': fitted, 'fit': 'pol1', \
               'parameter': 1, 'combine': combined, 'format': '{:.4f}'}
    average, averror = extractPerDirectionBx(options)
    return makeTexTablePerDirectionBx(average, averror, options)
