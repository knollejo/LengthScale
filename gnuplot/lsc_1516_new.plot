set terminal pdfcairo font "Helvetica, 12pt" size 3in,2.5in notransparent

set lmargin at screen 0.15
set rmargin at screen 0.95
set tmargin at screen 0.935
set bmargin at screen 0.155

set xtics 100 font ',12pt' offset 0,0.5
set xlabel 'Nominal position [µm]' font ',16pt' offset 0,1
set ytics 5 font ',12pt' offset 0.5,0
set ylabel 'Vertex – nominal position [µm]' font ',16pt' offset 1.5,0
set bars large

unset key
set label 1 '{/:Bold CMS}' at screen 0.15,0.935 left font ',16pt' front offset 0,character 0.6
set label 3 '{/:Italic Preliminary}' at screen 0.28,0.935 left font ',12pt' front offset 0,character 0.5
set label 2 '2016 (13 TeV)' at screen 0.95,0.935 right font ',12pt' front offset 0,character 0.6

set label 12 '' at screen 0.2,0.86 left font 'Helvetica Bold,10pt' front
set label 4 'Low-to-high' at screen 0.2,0.86 left font ',10pt' front tc lt 1 offset character 1,character -0.7
set label 5 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -1.4
set label 6 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -2.1
set label 7 '' at screen 0.2,0.86 left font ',10pt' front offset 0,character -2.8
set label 8 'High-to-low' at screen 0.6,0.86 left font ',10pt' front tc lt 2 offset character 1,character -0.7
set label 9 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -1.4
set label 10 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -2.1
set label 11 '' at screen 0.6,0.86 left font ',10pt' front offset 0,character -2.8
set label 13 at screen 0.205,0.815 point pt 7 ps 0.22 lc 0
set label 14 at screen 0.605,0.815 point pt 5 ps 0.22 lc 0

set xrange [-250:250]
set yrange [942:967]
set label 12 'Vertical scan'
set label 5 'p0 = 952.4 ± 0.2'
set label 6 'p1 = −0.007 ± 0.001'
set label 7 'χ²/dof = 16.6 / 3'
set label 9 'p0 = 947.0 ± 0.2'
set label 10 'p1 = −0.002 ± 0.001'
set label 11 'χ²/dof = 5.1 / 3'
filename = 'pcc_2016_rereco_jan17_Y1_vtxPosF_LS'
set output filename.'.pdf'
plot filename.'.dat' index 2 using 1:($2-$1) with lines lc 1, \
                  '' index 3 using 1:($2-$1) with lines lc 2, \
                  '' index 0 using 1:($2-$1):3 with yerrorbars pt 7 ps 0.22 lc 0, \
                  '' index 1 using 1:($2-$1):3 with yerrorbars pt 5 ps 0.22 lc 0
set output
