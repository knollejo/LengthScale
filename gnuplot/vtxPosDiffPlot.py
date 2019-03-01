import ROOT
import csv
csv.register_dialect('gnuplot', delimiter=' ', doublequote=False, lineterminator='\n')

def extract(inputfile, outputfile):
    tfile = ROOT.TFile.Open(inputfile)
    multi = filter(lambda key: not key.GetName().endswith('_residuals'), tfile.GetListOfKeys())[0].ReadObj()
    forw, backw = multi.GetListOfGraphs()[0:2]
    f1 = forw.GetListOfFunctions()[0]
    f2 = backw.GetListOfFunctions()[0]
    x, y = ROOT.Double(), ROOT.Double()
    forw_x, forw_y, forw_e = [], [], []
    backw_x, backw_y, backw_e = [], [], []
    for i in range(forw.GetN()):
        forw.GetPoint(i, x, y)
        forw_x.append(1.0*x)
        forw_y.append(1.0*y)
        forw_e.append(forw.GetErrorY(i))
    for i in range(backw.GetN()):
        backw.GetPoint(i, x, y)
        backw_x.append(1.0*x)
        backw_y.append(1.0*y)
        backw_e.append(backw.GetErrorY(i))
    forw_fx, backw_fx = [], []
    forw_fx.append(forw_x[0]-0.5*(forw_x[1]-forw_x[0]))
    forw_fx.extend(forw_x)
    forw_fx.append(forw_x[-1]+0.5*(forw_x[-1]-forw_x[-2]))
    backw_fx.append(backw_x[0]-0.5*(backw_x[1]-backw_x[0]))
    backw_fx.extend(backw_x)
    backw_fx.append(backw_x[-1]+0.5*(backw_x[-1]-backw_x[-2]))
    forw_fy = map(f1.Eval, forw_fx)
    backw_fy = map(f2.Eval, backw_fx)
    pars_forw = (
        f1.GetParameter(0), f1.GetParError(0),
        f1.GetParameter(1), f1.GetParError(1),
        f1.GetChisquare(), f1.GetNDF()
    )
    pars_backw = (
        f2.GetParameter(0), f2.GetParError(0),
        f2.GetParameter(1), f2.GetParError(1),
        f2.GetChisquare(), f2.GetNDF()
    )
    tfile.Close()
    with open(outputfile, 'w') as f:
        writer = csv.writer(f, dialect='gnuplot')
        f.write('# forward scan (x, y, e)\n')
        writer.writerows(zip(forw_x, forw_y, forw_e))
        f.write('\n\n# backward scan (x, y, e)\n')
        writer.writerows(zip(backw_x, backw_y, backw_e))
        f.write('\n\n# forward fit (x, y)\n')
        writer.writerows(zip(forw_fx, forw_fy))
        f.write('\n\n# backward fit (x, y)\n')
        writer.writerows(zip(backw_fx, backw_fy))
        f.write('\n\n# forward fit parameters:\n')
        f.write('# p0: {0}\n# p0 err: {1}\n'.format(pars_forw[0], pars_forw[1]))
        f.write('# p1: {0}\n# p1 err: {1}\n'.format(pars_forw[2], pars_forw[3]))
        f.write('# chisq/dof: {0} / {1}\n'.format(pars_forw[4], pars_forw[5]))
        f.write('\n\n# backw fit parameters:\n')
        f.write('# p0: {0}\n# p0 err: {1}\n'.format(pars_backw[0], pars_backw[1]))
        f.write('# p1: {0}\n# p1 err: {1}\n'.format(pars_backw[2], pars_backw[3]))
        f.write('# chisq/dof: {0} / {1}\n'.format(pars_backw[4], pars_backw[5]))

for inputfile, outputfile in (
    # ('results/pcc_2016_rereco_jan17_part/pcc_2016_rereco_jan17_part_X1_vtxPosF_LS_collected.root',
    #  'pcc_2016_rereco_jan17_X1_vtxPosF_LS.dat'),
    # ('results/pcc_2016_rereco_jan17_part/pcc_2016_rereco_jan17_part_Y1_vtxPosF_LS_collected.root',
    #  'pcc_2016_rereco_jan17_Y1_vtxPosF_LS.dat'),
    # ('results/pcc_2015_rereco_jan17_part/pcc_2015_rereco_jan17_part_X1_vtxPosF_LS_collected.root',
    #  'pcc_2015_rereco_jan17_X1_vtxPosF_LS.dat'),
    # ('results/pcc_2015_rereco_jan17_part/pcc_2015_rereco_jan17_part_X2_vtxPosF_LS_collected.root',
    #  'pcc_2015_rereco_jan17_X2_vtxPosF_LS.dat'),
    # ('results/pcc_2015_rereco_jan17_part/pcc_2015_rereco_jan17_part_Y1_vtxPosF_LS_collected.root',
    #  'pcc_2015_rereco_jan17_Y1_vtxPosF_LS.dat'),
    # ('results/pcc_promptreco16/pcc_promptreco16_X1_vtxPosF_LS_collected.root',
    #  'pcc_promptreco16_X1_vtxPosF_LS.dat'),
    # ('results/pcc_promptreco16/pcc_promptreco16_Y1_vtxPosF_LS_collected.root',
    #  'pcc_promptreco16_Y1_vtxPosF_LS.dat'),
    # ('results/pcc_promptreco15/pcc_promptreco15_X1_vtxPosF_LS_collected.root',
    #  'pcc_promptreco15_X1_vtxPosF_LS.dat'),
    # ('results/pcc_promptreco15/pcc_promptreco15_X2_vtxPosF_LS_collected.root',
    #  'pcc_promptreco15_X2_vtxPosF_LS.dat'),
    # ('results/pcc_promptreco15/pcc_promptreco15_Y1_vtxPosF_LS_collected.root',
    #  'pcc_promptreco15_Y1_vtxPosF_LS.dat'),
    ('results/pcc_rereco18/pcc_rereco18_X1_vtxPosL_collected.root',
     'pcc_rereco18_X1_vtxPosL.dat'),
    ('results/pcc_rereco18/pcc_rereco18_Y1_vtxPosL_collected.root',
     'pcc_rereco18_Y1_vtxPosL.dat'),
):
    extract(inputfile, outputfile)
