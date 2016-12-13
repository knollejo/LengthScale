from config import options as O, EOSPATH as eos
from os import listdir, stat
from tools import writeFiles
from ROOT import TFile

def loopOverRootFiles(action, fileset):
    """Execute an action on all ROOT files in a fileset"""
    for directory in O[fileset]:
        print '<<< Enter directory', directory
        allfiles = listdir(eos+directory+'/')
        for filename in allfiles:
            if not filename.endswith('.root'):
                continue
            if stat(eos+directory+'/'+filename).st_size <= 0:
                continue
            datafile = TFile.Open(eos+directory+'/'+filename)
            datatree = datafile.Get(O['treename'][fileset])
            action(datatree, directory+'/'+filename)
            datafile.Close()

def findRootFiles(fileset):
    """Check all ROOT files for lumisections belonging to scans"""
    files = dict([(scan, []) for scan in O['scans']])
    def action(tree, filename):
        for scan in O['scans']:
            condition = 'run == ' + str(O['runs'][scan]) + \
                        ' && LS >= ' + str(O['lumisections'][scan][0]) + \
                        ' && LS <= ' + str(O['lumisections'][scan][1])
            if tree.GetEntries(condition) > 0:
                files[scan].append(filename)
                print '<<< Found file:', filename
    loopOverRootFiles(action, fileset)
    return writeFiles(files, fileset)

def findAllRootFiles(fileset):
    """Create a list of all ROOT files belonging to a fileset"""
    files = []
    def action(tree, filename):
        files.append(filename)
        print '<<< Found file:', filename
    loopOverRootFiles(action, fileset)
    return writeFiles(files, fileset+'_all')
