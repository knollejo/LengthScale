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

def convertHD5FilesToRoot(options):
    """Convert all HD5 files to ROOT tree files and list them"""
    files = dict([(scan, []) for scan in O['scans']])
    allfiles = []
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
            rootfile['tree'] = TTree(O['treename']['hd5files'], \
                                     O['detector'][1]+' data')
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
                allfiles.append(rootfile['name'])
                if rootfile['tree'].GetEntries(condition) > 0:
                    files[scan].append(rootfile['name'])
                    print '<<< File contains scan', scan
            print '<<< Save ROOT file:', rootfile['name']
            rootfile['file'].Write()
            rootfile['file'].Close()
            return rootfile['number'] + 1
        print '<<< Read from file:', filename
        hd5 = getattr(table.root, options['table'])
        first = True
        lasttimestamp = 0
        thisfilenumber = 0
        for i, row in enumerate(hd5.iterrows()):
            if not options['condition'](row):
                continue
            nowtimestamp = int(row['timestampsec'])
            if first:
                rootfile = newRootFile(filenumber)
                rootfile['time'][0] = nowtimestamp
                first = False
            if nowtimestamp > rootfile['time'][0]:
                for j in range(nBX):
                    rootfile['data'][0] = rootfile['datas'][j]
                    rootfile['bx'][0] = rootfile['bxs'][j]
                    rootfile['tree'].Fill()
                if i / 100000 > thisfilenumber:
                    rootfile = newRootFile(closeRootFile(rootfile))
                    thisfilenumber += 1
                for j in range(nBX):
                    rootfile['datas'][j] = 0.0
                rootfile['time'][0] = nowtimestamp
            rootfile['fill'][0] = int(row['fillnum'])
            rootfile['run'][0] = int(row['runnum'])
            rootfile['ls'][0] = int(row['lsnum'])
            for i, bx in enumerate(O['crossings']):
                rootfile['datas'][i] += int(row['data'][bx-1])
        return closeRootFile(rootfile)
    loopOverHD5Files(action, options['fileset'])
    writeFiles(allfiles, options['fileset']+'_all', eos=False)
    return writeFiles(files, options['fileset'], eos=False)

def convertBCM1f(fileset):
    """Extract BCM1f data from HD5 files"""
    options = {'fileset': fileset, 'table': 'bcm1fagghist'}
    def condition(row):
        algoid = int(row['algoid'])
        channelid = int(row['channelid'])
        return algoid == 2 and channelid < 48
    options['condition'] = 'condition'
    convertHD5FilesToRoot(options)

def convertPLT(fileset):
    """Extract PLT data from HD5 files"""
    options = {'fileset': fileset, 'table': 'pltaggzero'}
    options['condition'] = lambda row: True
    convertHD5FilesToRoot(options)
