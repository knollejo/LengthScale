set terminal pdfcairo font "Helvetica, 12pt" size 3in,2.5in notransparent

set lmargin at screen 0.15
set rmargin at screen 0.95
set tmargin at screen 0.935
set bmargin at screen 0.155

set xtics 100 font ',12pt' offset 0,0.5
set xlabel 'nominal position [µm]' font ',16pt' offset 0,1
set ytics 2 font ',12pt' offset 0.5,0
set ylabel 'vertex – nominal position [µm]' font ',16pt' offset 1.5,0
set bars large

unset key
set label 1 '{/:Bold CMS}' at screen 0.15,0.935 left font ',16pt' front offset 0,character 0.6
set label 3 'Preliminary' at screen 0.28,0.935 left font ',12pt' front offset 0,character 0.5
set label 2 '2018 (13 TeV)' at screen 0.95,0.935 right font ',12pt' front offset 0,character 0.6

set label 12 '' at screen 0.2,0.86 left font 'Helvetica Bold,10pt' front
set label 4 'forward direction' at screen 0.2,0.86 left font ',10pt' front tc lt 1 offset character 1,character -0.7
set label 5 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -1.4
set label 6 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -2.1
set label 8 'backward direction' at screen 0.6,0.86 left font ',10pt' front tc lt 2 offset character 1,character -0.7
set label 9 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -1.4
set label 10 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -2.1
set label 13 at screen 0.205,0.815 point pt 7 ps 0.22 lc 1
set label 14 at screen 0.605,0.815 point pt 5 ps 0.22 lc 2

set xrange [-225:260]
set yrange [-2:5]
set label 12 'horizontal scan'
set label 5 'slope: −0.0083 ± 0.0005'
set label 6 'χ²/d.o.f. = 49.2 / 3'
set label 9 'slope: −0.0050 ± 0.0005'
set label 10 'χ²/d.o.f. = 3.1 / 3'
filename = 'pcc_rereco18_X1_vtxPosL'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:(-$2-$1+944.0) with lines lc 1, \
                  '' index 3 using 1:(-$2-$1+953.4) with lines lc 2, \
                  '' index 0 using 1:(-$2-$1+944.0):3 with yerrorbars ps 0 lc 0, \
                  '' index 1 using 1:(-$2-$1+953.4):3 with yerrorbars ps 0 lc 0, \
                  '' index 0 using 1:(-$2-$1+944.0) pt 7 ps 0.22 lc 1, \
                  '' index 1 using 1:(-$2-$1+953.4) pt 5 ps 0.22 lc 2
set output

set xrange [-225:260]
set yrange [-2:5]
set label 12 'vertical scan'
set label 5 'slope: −0.0028 ± 0.0005'
set label 6 'χ²/d.o.f. = 61.7 / 3'
set label 9 'slope: −0.0023 ± 0.0005'
set label 10 'χ²/d.o.f. = 6.5 / 3'
filename = 'pcc_rereco18_Y1_vtxPosL'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1+587.8) with lines lc 1, \
                  '' index 3 using 1:($2-$1+591.0) with lines lc 2, \
                  '' index 0 using 1:($2-$1+587.8):3 with yerrorbars ps 0 lc 0, \
                  '' index 1 using 1:($2-$1+591.0):3 with yerrorbars ps 0 lc 0, \
                  '' index 0 using 1:($2-$1+587.8) pt 7 ps 0.22 lc 1, \
                  '' index 1 using 1:($2-$1+591.0) pt 5 ps 0.22 lc 2
set output
