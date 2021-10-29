#!/bin/bash

# Written by Daniel Valente, 2020.

# READ THE $out FILE IN COSMOVIEW, TO VISALUZE THE ALTERED SURFACE BASED ON SEGMENT CHARGE DENSITY. CONTRIBUTING SEGMENTS ARE GREEN, AND POLAR ONES ARE BLUE
inp=out.cosmo
tresh=0.01  # Charge-density
out=${inp/.cosmo/.viz.cosmo}

echo "$inp $out"

cat /dev/null > $out

linha=$(awk '/n/ && /atom/ && /charge/ && /area/ && /charge\/area/ && /potential/ {print NR}' $inp)
let linha=$linha+3

# Alterando cor de segmentos
cat $inp > $out
awk -i inplace -v linha=$linha -v tresh=$tresh -v printv=-0.02 '
NR < linha {print} 
NR >= linha {if ( $(NF-1) <= tresh && $(NF-1) >= -tresh ) {$(NF-1)=0.00 ; $7=1.0 ; $6=0.00 ; print} else {$(NF-1)=printv ; $7=1.0 ;  $6=printv ; print} }' $out # FOR CHARGE-DENSITY BASED SURFACE

echo Acabou
