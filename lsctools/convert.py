from config import options as O, OWNPATH as path, EOSPATH as eos
from tools import checkDir, writeFiles
from tables import open_file as tablesOpen
from array import array
from os import listdir, stat
from ROOT import TFile, TTree

def loopOverHD5Files(action, fileset):
    """Execute an action on all HD5 files in a fileset"""
    filenumber = 0
    for directory in O[fileset]:
        print '<<< Enter directory', directory
        allfiles = listdir(eos+directory+'/')
        for filename in allfiles:
            if not filename.endswith('.hd5'):
                continue
            if stat(eos+directory+'/'+filename).st_size <= 0:
                continue
            table = tablesOpen(eos+directory+'/'+filename)
            filenumber = action(table, directory+'/'+filename, filenumber)

def convertBCM1f(fileset):
    """Convert all BMC1f HD5 files to ROOT tree files and list them"""
    files = dict([(scan, []) for scan in O['scans']])
    def action(table, filename, filenumber):
        nBX = len(O['crossings'])
        checkDir(path + '/' + O['detector'][0] + '_' + O['dataset'][0])
        def newRootFile(filenumber):
            rootfile = {'number': filenumber}
            rootfile['name'] = path + '/' + O['detector'][0] + '_' + \
                               O['dataset'][0] + '/' + O['detector'][0] + '_' \
                               + O['dataset'][0] + '_' + str(filenumber) + \
                               '.root'
            print '<<< Create ROOT file:', rootfile['name']
            rootfile['file'] = TFile(rootfile['name'], 'RECREATE')
            for inttype in ['b', 'h', 'i', 'l']:
                if array(inttype, [0]).itemsize == 4:
                    break
            rootfile['time'] = array(inttype, [0])
            rootfile['data'] = array('f', [0.0])
            rootfile['datas'] = nBX * [0.0]
            rootfile['bx'] = array(inttype, [0])
            rootfile['bxs'] = [bx for bx in O['crossings']]
            rootfile['fill'] = array(inttype, [0])
            rootfile['run'] = array(inttype, [0])
            rootfile['ls'] = array(inttype, [0])
            rootfile['tree'] = TTree(O['treename']['hd5files'], 'BCM1f data')
            rootfile['tree'].Branch(O['timename']['hd5files'], \
                                    rootfile['time'], 'timestamp/I')
            rootfile['tree'].Branch('data', rootfile['data'], 'data/F')
            rootfile['tree'].Branch('bx', rootfile['bx'], 'bx/I')
            rootfile['tree'].Branch('fill', rootfile['fill'], 'fill/I')
            rootfile['tree'].Branch('run', rootfile['run'], 'run/I')
            rootfile['tree'].Branch('ls', rootfile['ls'], 'ls/I')
            return rootfile
        def closeRootFile(rootfile):
            for scan in O['scans']:
                condition = 'run == ' + str(O['runs'][scan]) + ' && ls >= ' + \
                            str(O['lumisections'][scan][0]) + ' && ls <= ' + \
                            str(O['lumisections'][scan][1])
                if rootfile['tree'].GetEntries(condition) > 0:
                    files[scan].append(rootfile['name'])
                    print '<<< File contains scan', scan
            print '<<< Save ROOT file:', rootfile['name']
            rootfile['file'].Write()
            rootfile['file'].Close()
            return rootfile['number'] + 1
        rootfile = newRootFile(filenumber)
        print '<<< Read from file:', filename
        bcm1f = table.root.bcm1fagghist
        beam = table.root.beam
        first = True
        lasttimestamp = 0
        thisfilenumber = 0
        for i, row in enumerate(bcm1f.iterrows()):
            if not int(row['algoid']) == 2:
                continue
            channelid = int(row['channelid']) - 1
            if channelid >= 48:
                continue
            nowtimestamp = int(row['timestampsec'])
            if first:
                rootfile['time'][0] = nowtimestamp
                first = False
            if nowtimestamp > rootfile['time'][0]:
                for i in range(nBX):
                    rootfile['data'][0] = rootfile['datas'][i]
                    rootfile['bx'][0] = rootfile['bxs'][i]
                    rootfile['tree'].Fill()
                if i / 100000 > thisfilenumber:
                    rootfile = newRootFile(closeRootFile(rootfile))
                    thisfilenumber += 1
                for i in range(nBX):
                    rootfile['datas'][i] = 0.0
                rootfile['time'][0] = nowtimestamp
            rootfile['fill'][0] = int(row['fillnum'])
            rootfile['run'][0] = int(row['runnum'])
            rootfile['ls'][0] = int(row['lsnum'])
            for i, bx in enumerate(O['crossings']):
                rootfile['datas'][i] += int(row['data'][bx-1])
        return closeRootFile(rootfile)
    loopOverHD5Files(action, fileset)
    return writeFiles(files, fileset+'_all')
