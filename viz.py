#Author: Daniel de C. A. valente, 2020

import numpy as np

# This python3 script is part of the CS-NPSA package, distributed under the GNU General Public License, version 3 (2007), being provided "as is" and without warranties of any kind. For more details, see <https://www.gnu.org/licenses/>.

# INSTRUCTIONS

# This script reads a cosmo/cpcm output file created by Turbomole or Orca ("arqinp") and, for the latter software, associated output file ("arqinp2"), and creates a visualization script ("outjmol") which should be read by Jmol software. A second output is printed directly to a text file ("arqtxt"): a list of polar and total surface areas for each atom. The total area, total polar area and their difference (equal to NPSA) for the molecule are printed to screen.

# "treshdensity" is the threshold for segments charge density absolute value. Higher than this, and the segment is considered polar. Otherwise, it is considered nonpolar. 

# "tresharea" is the threshold over area for an atom. If (atom polar area)/(atom total area) is higher than this, the atom is considered polar, and will be colored red. Otherwise, it is treated as nonpolar and will be colored blue. Atoms with no segments (internal) are colored yellow.

# user input ###############################################
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
        arqinp=str(input('Enter '+fim+' filename.\n'))
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
        treshdensity=input('Enter treshold for segment charge density (e/Angstrom^2). \n')
        try: 
                treshdensity=float(treshdensity)
                if treshdensity <= 0.0:
                   print("Treshold must be a positive decimal number.")
                   test=True
                else:
                   test=False
        except:
                print("Treshold must be a positive decimal number.")

test=True
while test == True:   # defining area treshold
        tresharea=input('Enter treshold for atom area, from 0 to 1. \n')
        try:
                tresharea=float(tresharea)
                test=False
                if tresharea > 1.0 or tresharea < 0.0:
                      print("Treshold must be between 0 and 1")
                      test=True
        except:
                print("Treshold must be a decimal number.")

outjmol=arqinp+'.spt'
arqxyz=arqinp+'.xyz'
arqtxt=arqinp+'.area.txt'
# end of user input  ###################################################

# program related information ##########################################
if nome == 'tur':
  string='n   atom              position (X, Y, Z)'  
  stringxyz='$coord_rad'
  stringxyz2='$coord_car' 
  arqinp2=arqinp
  aind=1  # atom column in data
  aare=6  # area column
  aden=7  # charge density column

if nome == 'orc':
  string='SURFACE POINTS (A.U.)' 
  stringxyz='CARTESIAN COORDINATES (ANGSTROEM)'
  stringxyz2='CARTESIAN COORDINATES (A.U.)'
  aind=6  # atom column in data
  aare=3  # area column
  aden=7  # charge density column

# create xyz file ######################################################
toang=1.0/1.889716  # conversion of bohr to angstrom
geom=False
geo=[]
with open(arqinp2,'r') as f:
  for line in f:
    if stringxyz in line:
      geom=True
      continue
    if stringxyz2 in line:
      geom=False
      continue
    if geom:
      geo.append(line)

arq=open(arqxyz,'w')

if nome == 'tur':
  print(len(geo[1:]),file=arq)
  print('',file=arq)
  for line in geo[1:]: 
    line2=line.split()
    print(line2[4].upper(),float(line2[1])*toang,float(line2[2])*toang,float(line2[3])*toang,file=arq,sep=" ")
elif nome == 'orc':
  print(len(geo[1:-2]),file=arq)
  print('',file=arq)
  for line in geo[1:-2]:
    print(line.strip(),file=arq,sep=" ")

arq.close()   

# read data ############################################################
with open(arqinp,'r') as f:
  for line in f:
    if string in line:
      data=np.loadtxt(f,skiprows=2)

f.close()

if nome == 'orc': 
  data[:,aare]=data[:,aare]*toang*toang # convert areas from bohr to angs
  data=np.c_[ data, np.divide(data[:,5],data[:,aare]) ] # calculate charge density for orca and add to data
  data[:,aind]=data[:,aind]+1 # orca atom numbers begin with 0. jmol starts with 1.

# begin jmol script. ##################################################
# assign all atoms as internal (yellow) and then correct for nonpolar or polar.
arqout=open(outjmol,"w")
print('load '+arqxyz+' ;\n frame last; \n color background white \n select all; \n color yellow;',file=arqout)

###############################################################
# reassign all atoms that have segments as nonpolar (blue). 
atoms=data[:,aind] # column with atoms index
atoms3=np.unique(atoms)  # list of atoms that actually have segments
string='select '
for a in atoms3:
        string=string+'atomno = '+str(a)+', '
string=string[:-2]+' ; '  # removing last comma 
print(string+'\n color blue\n',file=arqout)

###############################################################
# calculate total area for each atom
areaatom=np.zeros(atoms3.shape)
contador=0
for a in atoms3:
        area=data[data[:,aind]==a]
        area2=area[:,aare]
        area3=np.sum(area2)
        areaatom[contador]=areaatom[contador]+area3
        contador=contador+1

# eliminate nonpolar segments
data2=data[abs(data[:,aden])>treshdensity] 

# calculate polar surface for each atom
polarareaatom=np.zeros(atoms3.shape)
contador=0
arqarea=open(arqtxt,'w')
print('polar and total surface areas for each atom (Angstrom^2)',file=arqarea)
areatotal=0.0
polartotal=0.0
for a in atoms3:
	polararea=data2[data2[:,aind]==a]
	polararea2=polararea[:,aare]
	polararea3=np.sum(polararea2)
	polarareaatom[contador]=polarareaatom[contador]+polararea3
	print('atom ',a,' = ',polarareaatom[contador],' ',areaatom[contador],file=arqarea)
	areatotal=areatotal+areaatom[contador]
	polartotal=polartotal+polarareaatom[contador]
	contador=contador+1
arqarea.close()

print('In Angstrom^2')
print('Total area = ',areatotal)
print('Total polar area = ',polartotal)
print('NPSA = ',areatotal-polartotal)

# dividing polar/total area
div=np.zeros((len(atoms3),2))
div[:,1]=np.divide(polarareaatom,areaatom)
div[:,0]=atoms3

# applying area treshold. Atoms considered nonpolar are discarded.
div2=div[div[:,1]>tresharea]

# reassigning atoms as polar (red), if polar area is large enough
string='select '
for a in div2[:,0]:
        string=string+'atomno = '+str(a)+', '
string=string[:-2]+' ; '  # remove last comma
print(string+'\n color red;\n',file=arqout)
arqout.close()

# End of script ###############################################
###############################################################
