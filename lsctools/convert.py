from config import options as O, OWNPATH as path
from tools import checkDir
from tables import open_file as tablesOpen
from array import array
from os import listdir, stat
from ROOT import TFile, TTree

def loopOverHD5Files(action, fileset):
    """Execute an action on all HD5 files in a fileset"""
    for directory in O[fileset]:
        print '<<< Enter directory', directory
        allfiles = listdir(eos+directory+'/')
        for filename in allfiles:
            if not filename.endswith('.hd5'):
                continue
            if stat(eos+directory+'/'+filename).st_size <= 0:
                continue
            table = tablesOpen(eos+directory+'/'+filename)
            action(table, directory+'/'+filename)

def convertBCM1f(fileset):
    """Convert all BMC1f HD5 files to ROOT tree files and list them"""
    files = dict([(scan, []) for scan in O['scans']])
    def action(table, filename):
        nBX = len(O['crossings'])
        pos = [filename.find('Fill')]
        pos.append(filename.find('_', pos[0]))
        pos.append(filename.rfind('_')+1)
        pos.append(filename.find('.', pos[2]))
        newpath = path + '/' + O['detector'][0] + '_' + O['dataset'][0]
        newname = O['detector'][0] + '_' + O['dataset'][0] + '_' + \
                  filename[pos[0]:pos[1]] + '_' + filename[pos[2]:pos[3]]
        checkDir(newpath)
        print '<<< Create new ROOT file:', newpath+'/'+newfile
        rootfile = TFile(newpath+'/'+newfile, 'RECREATE')
        mytime = array('l', [0])
        mydata = array('f', nBX*[0.0])
        mybx = array('l', [bx for bx in O['crossings']])
        myfill = array('l', [0])
        myrun = array('l', [0])
        myls = array('l', [0])
        tree = TTree(O['treename']['owntrees'], 'BCM1f data')
        tree.Branch(O['timename']['owntrees'], mytime, 'timestamp/I')
        tree.Branch('data', mydata, 'data['+str(nBX)+'/F]')
        tree.Branch('bx', mybx, 'bx['+str(nBX)+'/I]')
        tree.Branch('fill', myfill, 'fill/I')
        tree.Branch('run', myrun, 'run/I')
        tree.Branch('ls', myls, 'ls/I')
        print '<<< Read from file:', filename
        bcm1f = table.root.bcm1fagghist
        beam = table.root.beam
        first = True
        lasttimestamp = 0
        for i, row in enumerate(bcm1f.iterrows()):
            if not int(row['algoid']) == 2:
                continue
            channelid = int(row['channelid']) - 1
            if channelid >= 48:
                continue
            nowtimestamp = int(row['timestampsec'])
            if first:
                mytime[0] = nowtimestamp
                first = False
            if nowtimestamp > mytime[0]:
                tree.Fill()
                for i in nBX:
                    mydata[i] = 0.0
                mytime[0] = nowtimestamp
            myfill = int(row['fillnum'])
            myrun = int(row['runnum'])
            myls = int(row['lsnum'])
            for i, bx in enumerate(O['crossings']):
                mydata[i] += int(row['data'][bx-1])
        print '<<< Save new ROOT file:', newpath+'/'+newfile
        rootfile.Write()
        rootfile.Close()
        for scan in O['scans']:
            condition = 'run == ' + str(O['runs'][scan]) + ' && ls >= ' + \
                        str(O['lumisections'][scan][0]) + ' && ls <= ' + \
                        str(O['lumisections'][scan][1])
            if tree.GetEntries(condition) > 0:
                files[scan].append(filename)
                print '<<< File contains scan', scan
    loopOverHD5Files(action, fileset)
    return writeFiles(files, fileset+'_all')
