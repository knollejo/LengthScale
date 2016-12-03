from config import options as O
from config import OUTPATH as outpath
from os import mkdir
from os.path import exists
from time import strftime
import pickle
import ROOT

def dataDir(check=True):
    """Give directory for data files and check if it exists"""
    dirname = outpath + '/' + O['detector'][0] + '_' + O['dataset'][0]
    if check and not exists(dirname):
        mkdir(dirname)
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

def writeFiles(files, name):
    """Write list of files to a pickle-file"""
    outputfile = picklePath(name)
    print '<<<< Write selected files:', outputfile
    with open(outputfile, 'wb') as pkl:
        pickle.dump(files, pkl)
    return outputfile

def loadFiles(name):
    """Load list of files from a pickle-file"""
    print '<<<< Load selected files:', picklePath(name)
    with open(picklePath(name), 'rb') as pkl:
        files = pickle.load(pkl)
    return files

def openRootFileW(name):
    """Open a ROOT file"""
    outputfile = rootPath(name)
    print '<<<< Write to file:', outputfile
    return ROOT.TFile(outputfile, 'RECREATE')

def openRootFileU(name):
    """Open a ROOT file"""
    outputfile = rootPath(name)
    print '<<<< Open file to update:', outputfile
    return ROOT.TFile(outputfile, 'UPDATE')

def openRootFileR(name):
    """Open a ROOT file"""
    outputfile = rootPath(name)
    print '<<<< Read from file:', outputfile
    return ROOT.TFile(outputfile, 'READ')

def closeRootFile(f, name):
    """Close a ROOT file"""
    print '<<<< Close file:', rootPath(name)
    f.Close()

def plotDir(check=True):
    """Give directory for plot files and check if it exists"""
    dirname = outpath + '/' + O['detector'][0] + '_' + O['dataset'][0] + '/out'
    if check and not exists(dirname):
        mkdir(dirname)
    return dirname

def plotName(title, timestamp=True):
    """Give name for plot file"""
    filename = O['detector'][0] + '_' + O['dataset'][0] + '_' + title
    if timestamp:
        filename = filename + '_' + strftime('%y%m%d_%H%M%S')
    return filename

def plotPath(title, check=True, timestamp=True):
    """Give path to plot file"""
    return plotDir(check) + '/' + plotName(title) + '.pdf'

def plotTitle(title):
    """Give title for a plot"""
    titlename = O['detector'][1] + ' ' + O['dataset'][1] + ' ' + title
    return titlename
