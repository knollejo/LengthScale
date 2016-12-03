from config import options as O, EOSPATH as eos
from os import listdir, stat
from tools import writeFiles
import ROOT

def findRootFiles(fileset):
    """Check all ROOT files for relevant lumisections in tree"""
    files = dict([(scan, []) for scan in O['scans']])
    for directory in O[fileset]:
        print '<<<< Enter directory', directory
        allfiles = listdir(eos+directory+'/')
        for filename in allfiles:
            if not filename.endswith('.root'):
                continue
            if stat(eos+directory+'/'+filename).st_size <= 0:
                continue
            datafile = ROOT.TFile.Open(eos+directory+'/'+filename)
            datatree = datafile.Get(O['treename'][fileset])
            for scan in O['scans']:
                condition = 'run == ' + str(O['runs'][scan]) + \
                            ' && LS >= ' + str(O['lumisections'][scan][0]) + \
                            ' && LS <= ' + str(O['lumisections'][scan][1])
                if datatree.GetEntries(condition) > 0:
                    files[scan].append(directory+'/'+filename)
                    print '<<<< Found file:', directory+'/'+filename
            datafile.Close()
    return writeFiles(files, fileset)
