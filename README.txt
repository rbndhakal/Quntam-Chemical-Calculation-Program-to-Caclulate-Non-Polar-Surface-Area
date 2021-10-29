List of Contents in Files Directory:

In Folder 'README':

1. 'User Guide NPSA' for the NPSA Python Program. 
   It contains all the information needed to install and use in the system of users. 
   Moreover, it contains a sample test documentation. 

2. 'User Guide Visualization' for Visualization Script  
   It contains the information required to install and use the scripts. 
   Moreover, it contains sample test documentation. 

In Folder 'NPSA Program':

1. NPSA.py
   Python3 program to calculate the non polar surface area (NPSA) using a given cosmo file and user-defined threshold value of charge per area.
   input: out.cosmo
   output: npsa.txt   

2. viz.py
   Python3 script to create a Jmol script (*.spt file) that distinguishes nonpolar, polar and non-surface (internal) atoms. Also produces a list of polar and total areas for each atom (*.area.txt file).
   input: out.cosmo
   output: out.cosmo.spt and out.cosmo.area.txt

3. polviz.py
   Python3 script to produce the altered *.cosmo file for TmoleX. Estimates of the polar and the nonpolar surfaces will appear as blue and green, respectively.
   input: out.cosmo 
   output: out.polviz.cosmo

In Folder 'Example':
   
1. out.cosmo
   Output from Turbomole calculation and input for the programs and scripts in the folder 'NPSA Program' 

2. out.polviz.cosmo
   Sample output from the 'polviz.py' script, using out.cosmo as input. 

3. out.cosmo.spt and out.cosmo.area.txt
   Sample jmol script and list of polar and total areas produced by 'viz.py' script, using out.cosmo as input.  

4. npsa.txt 
   Sample output from the 'NPSA.py' python program, using out.cosmo as input. 

Visualization using TmoleX and Jmol: 
   
The visualization of the COSMO polarization charge density and the CS-NPSA has been 
performed by means of TmoleX available at: 
https://www.3ds.com/products-services/biovia/products/molecular-modeling-simulation/solvation-chemistry/turbomoler/. 

Jmol: an open-source Java viewer for chemical structures in 3D, 
http://www.jmol.org/, has been used for 3D visualization of molecular structures.
