from config import options as O, OUTPATH as outpath, EOSPATH as eospath
from os import mkdir
from os.path import exists
from time import strftime
from pickle import load as pklload, dump as pkldump
from ROOT import TFile, TText

def timeStamp():
    return strftime('%y%m%d_%H%M%S')

def checkDir(dirname):
    if not exists(dirname):
        mkdir(dirname)

def dataDir(check=True):
    """Give directory for data files and check if it exists"""
    dirname = outpath + '/' + O['detector'][0] + '_' + O['dataset'][0]
    if check:
        checkDir(dirname)
    return dirname

def dataName(title):
    """Give name for data file"""
    filename = O['detector'][0] + '_' + O['dataset'][0] + '_' + title
    return filename

def picklePath(title, check=True):
    """Give path to a pickle file"""
    return dataDir(check) + '/' + dataName(title) + '.pkl'

def rootPath(title, check=True):
    """Give path to a ROOT file"""
    return dataDir(check) + '/' + dataName(title) + '.root'

def writeFiles(files, name, eos=True):
    """Write list of files to a pickle-file"""
    outputfile = picklePath(name)
    print '<<< Write selected files:', outputfile
    with open(outputfile, 'wb') as pkl:
        pkldump(files, pkl)
        pkldump(eos, pkl)
    return outputfile

def loadFiles(name):
    """Load list of files from a pickle-file"""
    print '<<< Load selected files:', picklePath(name)
    with open(picklePath(name), 'rb') as pkl:
        files = pklload(pkl)
        try:
            eos = pklload(pkl)
        except EOFError:
            eos = True
    if eos and type(files) is dict:
        returnfiles = {}
        for scan in files:
            returnfiles[scan] = [eospath+filename for filename in files[scan]]
        return returnfiles
    elif eos and type(files) is list:
        return [eospath+filename for filename in files]
    else:
        return files

def openRootFileW(name):
    """Open a ROOT file (overwrite mode)"""
    outputfile = rootPath(name)
    print '<<< Write to file:', outputfile
    return TFile(outputfile, 'RECREATE')

def openRootFileU(name):
    """Open a ROOT file (update mode)"""
    outputfile = rootPath(name)
    print '<<< Open file to update:', outputfile
    return TFile(outputfile, 'UPDATE')

def openRootFileR(name):
    """Open a ROOT file (read-only mode)"""
    outputfile = rootPath(name)
    print '<<< Read from file:', outputfile
    return TFile(outputfile, 'READ')

def closeRootFile(f, name):
    """Close a ROOT file"""
    print '<<< Close file:', rootPath(name)
    f.Close()

def plotDir(check=True):
    """Give directory for plot files and check if it exists"""
    dirname = outpath + '/' + O['detector'][0] + '_' + O['dataset'][0] + '/out'
    if check:
        checkDir(dirname)
    return dirname

def plotName(title, timestamp=True):
    """Give name for plot file"""
    filename = O['detector'][0] + '_' + O['dataset'][0] + '_' + title
    if timestamp:
        filename = filename + '_' + timeStamp()
    return filename

def plotPath(title, check=True, timestamp=True):
    """Give path to plot file"""
    return plotDir(check) + '/' + plotName(title) + '.C'

def plotTitle(title=''):
    """Give title for a plot"""
    titlename = O['detector'][1] + ' ' + O['dataset'][1] + ' ' + title
    return titlename

def drawSignature(signature):
    """Write an unique identifier in the lower left canvas corner"""
    l = TText()
    l.SetTextAlign(11)
    l.SetTextSize(0.02)
    l.SetTextFont(82)
    l.DrawTextNDC(0.01, 0.01, signature)
