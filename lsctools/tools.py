from config import options as O
from config import OUTPATH as outpath
from config import STOPATH as storage
from os import mkdir
from os.path import exists
from time import strftime
import pickle

def dataDir(check = True):
    """Give directory for data files and check if it exists"""
    dirname = outpath + '/' + O['detector'][0] + '_' + O['dataset'][0]
    if check and not exists(dirname):
        mkdir(dirname)
    return dirname

def dataName(title):
    """Give name for data file"""
    filename = O['detector'][0] + '_' + O['dataset'][0] + '_' + title
    return filename

def dataPath(title, check = True):
    """Give path to data file"""
    return dataDir(check) + '/' + dataName(title) + '.pkl'

def plotDir(check = True):
    """Give directory for plot files and check if it exists"""
    dirname = outpath + '/' + O['detector'][0] + '_' + O['dataset'][0] + '/out'
    if check and not exists(dirname):
        mkdir(dirname)
    return dirname

def plotName(title):
    """Give name for plot file"""
    filename = O['detector'][0] + '_' + O['dataset'][0] + '_' + title + '_' + \
               strftime('%y%m%d_%H%M%S')
    return filename

def plotPath(title, check = True):
    """Give path to plot file"""
    return plotDir(check) + '/' + plotName(title) + '.pdf'

def plotTitle(title):
    """Give title for a plot"""
    titlename = O['detector'][1] + ' ' + O['dataset'][1] + ' ' + title
    return titlename

def storDir(check = True):
    """Give directory for temporary storage and check if it exists"""
    dirname = storage + '/storage_' + O['detector'][0] + '_' + O['dataset'][0]
    if check and not exists(dirname):
        mkdir(dirname)
    return dirname

def storName(title):
    """Give name for temporary storage file"""
    filename = O['detector'][0] + '_' + O['dataset'][0] + '_' + title
    return filename

def storPath(title, check = True):
    """Give path to temporary storage file"""
    return storDir(check) + '/' + storName(title) + '.root'

def writeResults(average, averror, name):
    """Write results in a pickle-file"""
    outputfile = dataPath(name)
    print '<<<< Write results:', outputfile
    with open(outputfile, 'wb') as pkl:
        pickle.dump(average, pkl)
        pickle.dump(averror, pkl)
    return outputfile

def loadResults(path):
    """Load results from a pickle-file"""
    print '<<<< Load results:', path
    with open(path, 'rb') as pkl:
        average = pickle.load(pkl)
        averror = pickle.load(pkl)
    return (average, averror)

def writeFiles(files, name):
    """Write list of files to a pickle-file"""
    outputfile = dataPath(name)
    print '<<<< Write selected files:', outputfile
    with open(outputfile, 'wb') as pkl:
        pickle.dump(files, pkl)
    return outputfile

def loadFiles(path):
    """Load list of files from a pickle-file"""
    print '<<<< Load selected files:', path
    with open(path, 'rb') as pkl:
        files = pickle.load(pkl)
    return files

def addToPickle(key, value, path):
    """Add an entry to a dictionary stored in a pickle-file"""
    print '<<<< Add to file:', path
    if exists(path):
        with open(path, 'rb') as pkl:
            collection = pickle.load(pkl)
    else:
        collection = {}
    collection[key+strftime('%y%m%d_%H%M%S')] = value
    with open(path, 'wb') as pkl:
        pickle.dump(collection, pkl)
