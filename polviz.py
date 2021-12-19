#!/bin/bash

# This python3 script is part of the CS-NPSA package, distributed under the GNU General Public License, version 3 (2007), being provided "as is" and without warranties of any kind. For more details, see <https://www.gnu.org/licenses/>.

# INSTRUCTIONS

#  This script requires as input the cosmo/cpcm ouput file (with charges, areas, etc, of each segment) created by Turbomole or Orca ("arqinp"), and, for the latter software, associated output file ("arqinp2"). It alters the charges, areas and charge densities in the file, generating the "out" file. 

# Areas are reset to 1. If the original absolute value of the segment charge density (CD) is larger (smaller) than "tresh" variable, both its CD and charge are reset to "printv" variable (0.0). 

# The output file can be visualized with COSMOview, providing estimates for the polar (blue) and nonpolar (green) surfaces.

import numpy as np

# user input ##########################################################################

test=True
while test == True:   # defining program
        nome=str(input('Enter program name. tur (Turbomole) or orc (Orca).\n'))
        if nome == 'tur':
                test=False
                fim='.cosmo'
        elif nome == 'orc':
                test=False
                fim='.cpcm'
        else:
                print("Select tur (Turbomole) or orc (Orca).")

test=True
while test == True:   # defining cosmo/cpcm file
        base=str(input('Enter '+fim+' filename, but without the '+fim+' extension.\n'))
        arqinp=base+fim
        test=False
        try:
                f=open(arqinp,'r')
        except:
                print("Can not open file.")
                test=True
f.close()

if nome == 'orc':
  test=True
  while test == True:
    arqinp2=str(input('For Orca, also enter the name of the output file.\n'))
    test=False
    try:
      f=open(arqinp2,'r')
    except:
      print("Can not open file.")
      test=True
f.close()

test=True
while test == True:   # defining density treshold
        tresh=input('Enter treshold for segment charge density (e/Angstrom^2). \n')
        try: 
                tresh=float(tresh)
                if tresh <= 0.0:
                   print("Treshold must be a positive decimal number.")
                   test=True
                else:
                   test=False
        except:
                print("Treshold must be a positive decimal number.")

out=base+'.polviz.cosmo' # output file. 
printv=-0.02             # charge density new value, in case original is higher than tresh.
# End of input ##########################################################################

# program related information ##########################################
acharg=5  # atom column in data
aare=6  # area column
aden=7  # charge density column

arqout=open(out,"w")
if nome == 'tur':
  string='n   atom              position (X, Y, Z)'  
  arqinp2=arqinp

if nome == 'orc': # for Orca, it is necessary to read the geometry from both output and cpcm files.
  string='SURFACE POINTS (A.U.)' 
  stringxyz='CARTESIAN COORDINATES (ANGSTROEM)'
  stringxyz2='CARTESIAN COORDINATES (A.U.)'

  # create xyz fragment for orca 
  tobohr=1.889716  # conversion of angstrom to bohr
  toang=1.0/tobohr # conversion of bohr to angstrom

  geom=False
  geo=[]

  with open(arqinp2,'r') as f: # reading geometry from output file to get element list
    for line in f:
      if stringxyz in line:
        geom=True
        continue
      if stringxyz2 in line:
        geom=False
        continue
      if geom:
        geo.append(line)
  stringxyz='CARTESIAN COORDINATES (A.U.) + RADII (A.U.)'
  geom=False
  radius=[]

  with open(arqinp,'r') as f: # reading geometry from cpcm file to get radius list
    for line in f:
      if stringxyz in line:
        geom=True
        continue
      if string in line:
        geom=False
        continue
      if geom:
        radius.append(line)
  print('$coord_rad',file=arqout)
  cont=0

  for line in geo[1:-2]:
    cont=cont+1
    radius2=radius[cont].split()
    line2=line.split()
    line3=[cont,float(line2[1])*tobohr,float(line2[2])*tobohr,float(line2[3])*tobohr,line2[0].lower(),float(radius2[-1])/tobohr]  # adjust columns and convert to apropriate units
    line2=" ".join(map(str,line3))
    print(line2,file=arqout,sep=" ")

  print('$coord_car',file=arqout)
  print('!BIOSYM archive 3\n!DATE',file=arqout)
  cont=0

  for line in geo[1:-2]:
    cont=cont+1
    line2=line.split()
    line3=[line2[0],float(line2[1]),float(line2[2]),float(line2[3]),'COSM 1',line2[0].lower(),line2[0],'0.000']  # adjust columns 
    line2=" ".join(map(str,line3))
    print(line2,file=arqout,sep=" ")

  print('end\nend\n$segment_information',file=arqout)
  del geo 
  del radius 

# read segment data ############################################################
with open(arqinp,'r') as f:
  for line in f:
    if string in line:
      data=np.loadtxt(f,skiprows=2) 
      print(line,file=arqout,end='')
      break
    else:
      if nome == 'tur':
        print(line,file=arqout,end='')  
      else:
        continue 

if nome == 'orc':                   # several adjustments are required for Orca
  data[:,3]=data[:,3]*toang*toang   # convert areas from bohr to angs
  data[:,6]=data[:,6]+1             # orca atom numbers begin with 0, instead of 1.
  row,column=np.shape(data)
  data=np.c_[ np.linspace(1,row,num=row).reshape(row,1), data, np.divide(data[:,5],data[:,3]) ] # add column with segment number and column with charge density
  data2=data[:,[0,7,1,2,3,6,4,8,5]]  # reorganizing columns
  del data
  data=data2  # updating data matrix for next steps
  del data2 

# altering the segment data ######################################################

mask=(data[:,7]>tresh) | (data[:,7]<-tresh) # selecting polar segments
data[:,7]=0.0 				    # altering charge density of all segments to zero
data[mask,7]=printv 			    # altering charge density of polar segments to desired value. 

# altering areas. Set them equal to 1
data[:,6]=1.0

# altering charges. Set them equal to charge density
data[:,5]=data[:,7]  

# printing data
np.savetxt(arqout,data,fmt='%i %i %.9f %.9f %.9f %.2f %i %.2f %.9f',delimiter='\t')
arqout.close()
