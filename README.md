# Automate-steered-MD-simulation
This script generate a pipeline of steered MD simulation and pull the ligand in the axis user give with the force which also user give to it.
# INSTALL requirements with conda
*conda create -n autosmd python==3.7.3
*conda install NetworkX==2.3
*conda activate autosmd
*pip install numpy
*pip install Mechanize
## Run the script
python Automate_sMD.py --axis (X,Y or Z) --rotate [rotation degree of your protein] --center [to put your structure at the end of the box] --box [box size] --kj [the fore you want to apply]
## Some important points you need to focus on them ##
1) try to use your ligand pdb file as a simple name and protein pdb files same name as your ligand file name + _protein
exmp/ your ligand name -> ligand1.pdb and your protein file name -> ligand1_protein.pdb
2) You need to put ligands pdb files only in pdb_files diectory
3) You need to put protein pdb files (only protein) in protein_pdb directory
4) First check your complex box and choose the box size and if need rotation for protein select the rotation 
   degrees for X,Y,Z coordinates. After you be sure about you box and complex center (Your complex should be completely inside the box) you can run script.
** Inside a folder open 3 folder 1.pdb_files 2.protein_pdb 3.sMD_need **
pdb_files => Your ligand.pdb files
protein_pdb => Your ligandname_protein.pdb files
sMD_need => All .mdp files you need for run pulling
#
Go to cGenFF website and open an acount -> get username and password https://cgenff.silcsbio.com/
Then in cGenFF_scraper/ folder open cGenFF_scraper.py script and change {user = input('Please insert your cGenFF username or enter Q to quit: ')} with user= 'your username'
and also remove print('Please input your password now: ') and change {psw = getpass()} with psw= 'your password'
### *** NOW YOU CAN START THE SCRIPT FOR STEERED MD RUNNING *** ###

**Cite**

Please cite our publication: https://doi.org/10.1002/cbic.202400008
