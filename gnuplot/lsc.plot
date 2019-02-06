set terminal pdfcairo font "Helvetica, 12pt" size 3in,2.5in notransparent

set lmargin at screen 0.15
set rmargin at screen 0.95
set tmargin at screen 0.935
set bmargin at screen 0.155

set xtics 100 font ',12pt' offset 0,0.5
set xlabel 'nominal position [µm]' font ',16pt' offset 0,1
set ytics 5 font ',12pt' offset 0.5,0
set ylabel 'vertex – nominal position [µm]' font ',16pt' offset 1.5,0
set bars large

unset key
set label 1 '{/:Bold CMS}' at screen 0.15,0.935 left font ',16pt' front offset 0,character 0.6
set label 3 '' at screen 0.28,0.935 left font ',12pt' front offset 0,character 0.5
set label 2 '2016 (13 TeV)' at screen 0.95,0.935 right font ',12pt' front offset 0,character 0.6

set label 12 '' at screen 0.2,0.86 left font 'Helvetica Bold,10pt' front
set label 4 'forward direction' at screen 0.2,0.86 left font ',10pt' front tc lt 1 offset character 1,character -0.7
set label 5 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -1.4
set label 6 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -2.1
set label 7 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -2.8
set label 8 'backward direction' at screen 0.6,0.86 left font ',10pt' front tc lt 2 offset character 1,character -0.7
set label 9 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -1.4
set label 10 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -2.1
set label 11 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -2.8
set label 13 at screen 0.205,0.815 point pt 7 ps 0.22 lc 0
set label 14 at screen 0.605,0.815 point pt 5 ps 0.22 lc 0

set xrange [-250:250]
set yrange [648:673]
set label 12 'horizontal scan'
set label 5 'p0 = 652.5 ± 0.2'
set label 6 'p1 = −0.0093 ± 0.0010'
set label 7 'χ²/d.o.f. = 6.9 / 3'
set label 9 'p0 = 660.5 ± 0.2'
set label 10 'p1 = −0.0105 ± 0.0010'
set label 11 'χ²/d.o.f. = 22.1 / 3'
filename = 'pcc_2016_rereco_jan17_X1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:(-$2-$1+1305) with lines lc 1, \
                  '' index 3 using 1:(-$2-$1+1321) with lines lc 2, \
                  '' index 0 using 1:(-$2-$1+1305):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:(-$2-$1+1321):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set xrange [-250:250]
set yrange [942:967]
set label 12 'vertical scan'
set label 5 'p0 = 952.4 ± 0.2'
set label 6 'p1 = −0.0073 ± 0.0010'
set label 7 'χ²/d.o.f. = 16.6 / 3'
set label 9 'p0 = 947.0 ± 0.2'
set label 10 'p1 = −0.0020 ± 0.0010'
set label 11 'χ²/d.o.f. = 5.1 / 3'
filename = 'pcc_2016_rereco_jan17_Y1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set label 2 '2015 (13 TeV)'
set xrange [-300:300]
set yrange [721:746]
set label 12 'first horizontal scan'
set label 5 'p0 = 724.5 ± 0.2'
set label 6 'p1 = −0.0034 ± 0.0010'
set label 7 'χ²/d.o.f. = 3.4 / 2'
set label 9 'p0 = 733.2 ± 0.2'
set label 10 'p1 = −0.0038 ± 0.0008'
set label 11 'χ²/d.o.f. = 1.8 / 3'
filename = 'pcc_2015_rereco_jan17_X1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set xrange [-300:300]
set yrange [956:981]
set label 12 'vertical scan'
set label 5 'p0 = 967.5 ± 0.2'
set label 6 'p1 = −0.0020 ± 0.0008'
set label 7 'χ²/d.o.f. = 6.0 / 3'
set label 9 'p0 = 961.1 ± 0.2'
set label 10 'p1 = −0.0029 ± 0.0008'
set label 11 'χ²/d.o.f. = 6.7 / 3'
filename = 'pcc_2015_rereco_jan17_Y1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set xrange [-300:300]
set yrange [712:737]
set label 12 'second horizontal scan'
set label 5 'p0 = 716.0 ± 0.2'
set label 6 'p1 = −0.0038 ± 0.0007'
set label 7 'χ²/d.o.f. = 16.7 / 3'
set label 9 'p0 = 725.4 ± 0.2'
set label 10 'p1 = −0.0021 ± 0.0008'
set label 11 'χ²/d.o.f. = 5.0 / 3'
filename = 'pcc_2015_rereco_jan17_X2_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set label 3 '{/:Italic Internal}'
set label 2 '2016, PromptReco (13 TeV)'
set xrange [-250:250]
set yrange [645:670]
set label 12 'horizontal scan'
set label 5 'p0 = 648.9 ± 0.2'
set label 6 'p1 = −0.0081 ± 0.0009'
set label 7 'χ²/d.o.f. = 16.2 / 3'
set label 9 'p0 = 656.9 ± 0.2'
set label 10 'p1 = −0.0101 ± 0.0009'
set label 11 'χ²/d.o.f. = 17.4 / 3'
filename = 'pcc_promptreco16_X1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:(-$2-$1+1298) with lines lc 1, \
                  '' index 3 using 1:(-$2-$1+1314) with lines lc 2, \
                  '' index 0 using 1:(-$2-$1+1298):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:(-$2-$1+1314):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set xrange [-250:250]
set yrange [949:974]
set label 12 'vertical scan'
set label 5 'p0 = 958.9 ± 0.2'
set label 6 'p1 = −0.0072 ± 0.0009'
set label 7 'χ²/d.o.f. = 38.2 / 3'
set label 9 'p0 = 953.8 ± 0.2'
set label 10 'p1 = −0.0020 ± 0.009'
set label 11 'χ²/d.o.f. = 10.8 / 3'
filename = 'pcc_promptreco16_Y1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set label 2 '2015, PromptReco (13 TeV)'
set xrange [-300:300]
set yrange [733:758]
set label 12 'first horizontal scan'
set label 5 'p0 = 736.7 ± 0.2'
set label 6 'p1 = −0.0028 ± 0.0009'
set label 7 'χ²/d.o.f. = 3.2 / 2'
set label 9 'p0 = 745.6 ± 0.2'
set label 10 'p1 = −0.0025 ± 0.0007'
set label 11 'χ²/d.o.f. = 9.2 / 3'
filename = 'pcc_promptreco15_X1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set ylabel offset 2.5,0
set xrange [-300:300]
set yrange [981:1006]
set label 12 'vertical scan'
set label 5 'p0 = 993.0 ± 0.2'
set label 6 'p1 = −0.0022 ± 0.0007'
set label 7 'χ²/d.o.f. = 6.1 / 3'
set label 9 'p0 = 986.7 ± 0.2'
set label 10 'p1 = −0.0026 ± 0.0007'
set label 11 'χ²/d.o.f. = 10.0 / 3'
filename = 'pcc_promptreco15_Y1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output

set ylabel offset 1.5,0
set xrange [-300:300]
set yrange [724:749]
set label 12 'second horizontal scan'
set label 5 'p0 = 728.3 ± 0.2'
set label 6 'p1 = −0.0034 ± 0.0006'
set label 7 'χ²/d.o.f. = 19.4 / 3'
set label 9 'p0 = 737.7 ± 0.2'
set label 10 'p1 = −0.0008 ± 0.0007'
set label 11 'χ²/d.o.f. = 1.8 / 3'
filename = 'pcc_promptreco15_X2_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output
