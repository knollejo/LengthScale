from config import options as O
from tools import openRootFileR
from numpy import mean

def si(value, error):
    return '\\si{' + str(value) + ' \\pm ' + str(error) + '}'

def extractPerDirectionBx(options):
    """Extract results from directional fits (per BX)"""
    name = options['scan'] + '_'+ options['name'] + options['fitted'] \
           + '_collected'
    f = openRootFileR(name)
    crossings = O['crossings']
    average = dict(zip(crossings, [[0, 0] for i in len(crossings)]))
    averror = dict(zip(crossings, [[0, 0] for i in len(crossings)]))
    for bx in crossings:
        plotname = plotName(name+'_bx'+str(bx), timestamp=False)
        print '<<< Access plot:', plotname
        graphs = f.Get(plotname)
        for j, graph in enumerate(graphs.GetListOfGraphs()):
            function = graph.GetListOfFunctions().FindObject(options['fit'])
            average[bx][j] = function.GetParameter(options['parameter'])
            averror[bx][j] = function.GetParError(options['parameter'])
    return average, averror

def makeTexTablePerDirectionBx(average, averror, options):
    """Output results to LaTeX code"""
    print '\\begin{tabular}{lccc}'
    print '\t\\bfseries', options['scan'], '& \\bfseries forward & ', \
          '\\bfseries backward & \\bfseries difference \\\\'
    print '\t\\hline'
    for bx in O['crossings']:
        difference = abs(average[bx][0] - average[bx][1])
        differror = (averror[bx][0] ** 2 + averror[bx][1] ** 2) ** 0.5
        print '\t\\bfseries', bx
        for i in range(2):
            print '&', si(average[bx][i], averror[bx][i])
        print '&', si(difference, differror), '\\\\'
    print '\t\\hline'
    #print '\t average &'
    if(options['combine']):
        print '\t inclusive'
        for i in range(2):
            print '&', si(average['all'][i], averror['all'][i])
        print '\\\\'
