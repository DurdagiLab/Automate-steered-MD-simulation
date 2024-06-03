#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan.Sayyah
٬٬@author mail: Ehsan.sayyah73@gmail.com
Supervisor: Prof.Dr.Serdar Durdağı
"""

import os
import argparse
import glob
import shutil
import time
import subprocess


# Please replace the PATH for cGenFF.
cGenFF = '/media/arma/DATA/S-Ehsan/sMD_project/cGenFF_scraper/'
# Please replace the PATH for ligand pdb files.
autosMD= '/media/arma/DATA/S-Ehsan/Automate_sMD/RET_100_active/sMD/pdb_files/'
# Please replace the PATH for charmm36-jull2022.ff file.
charmm= '/media/arma/DATA/S-Ehsan/Automate_sMD/RET_100_active/sMD/pdb_files/charmm36-jul2022.ff/'
# Please replace the PATH for cgenff_charmm2gmx_py3_nx2.py.
charmm2gmx = '/media/arma/DATA/S-Ehsan/Automate_sMD/RET_100_active/sMD/pdb_files/cgenff_charmm2gmx_py3_nx2.py'
# Please replace the PATH for protein pdb files.
protein_pdb = '/media/arma/DATA/S-Ehsan/Automate_sMD/RET_100_active/sMD/protein_pdb/'
# Please replace the PATH for .mdp files you need for pulling.
sMD_need = '/media/arma/DATA/S-Ehsan/Automate_sMD/RET_100_active/sMD/sMD_need/'

## Some important points you need to focus on them ##
# 1) try to use your ligand pdb file as a simple name and protein pdb files same name as your ligand file name + _protein
# exmp/ your ligand name -> ligand1.pdb and your protein file name -> ligand1_protein.pdb
# 2) You need to put ligands pdb files only in pdb_files diectory
# 3) You need to put protein pdb files (only protein) in protein_pdb directory
# 4) First check your complex box and choose the box size and if need rotation for protein select the rotation 
#    degrees for X,Y,Z coordinates. After you be sure about you box and complex center (Your complex should be completely inside the box) you can run script.
# ** Inside a folder open 3 folder 1.pdb_files 2.protein_pdb 3.sMD_need **
# pdb_files => Your ligand.pdb files
# protein_pdb => Your ligandname_protein.pdb files
# sMD_need => All .mdp files you need for run pulling
#
# Go to cGenFF website and open an acount -> get username and password https://cgenff.silcsbio.com/
# Then in cGenFF_scraper/ folder open cGenFF_scraper.py script and change {user = input('Please insert your cGenFF username or enter Q to quit: ')} with user= 'your username'
# and also remove print('Please input your password now: ') and change {psw = getpass()} with psw= 'your password'
### *** NOW YOU CAN START THE SCRIPT FOR STEERED MD RUNNING *** ###

parser = argparse.ArgumentParser(description='Automate sMD code, for molecular Pulling')
parser.add_argument('--axis', action="store", type=str, help=' The axis you want to pull ligand (X or Y or Z)')
parser.add_argument('--rotate', action="store", nargs='+', type=str, default=None, help=' Rotate your protein inside the box')
parser.add_argument('--center', action="store",nargs='+', type=str, default='3.5', help='Change the center of protein based on your center coordinates defult = 3.5')
parser.add_argument('--box', action="store",nargs='+', type=str, default='6.5 12 6.5', help='Box size defules = 6.5 12 6.5')
parser.add_argument('--kj', metavar= '(kJ mol^-1 nm^-2)' ,action="store", type=int, default=100, help='Force you want to apply')

args = parser.parse_args()
if args.rotate != None:
    rotate= ' '.join(args.rotate)
else:
    rotate= args.rotate
if args.center == '3.5':
    center= args.center
else:
    center= ' '.join(args.center)
if args.box == '6.5 12 6.5':
    box= args.box
else:
    box= ' '.join(args.box)

os.chdir(autosMD)
# os.system(rf'mkdir pdb_files')
# Put all your ligand pdb files that you want to create .str file in pdb_files directory 
## Put your protein pdb file (only protein) in folder name protein_pdb near pdb_files(exmple: ligandname_protein.pdb)

extension = 'pdb'
pdb_files=glob.glob('*.{}'.format(extension))
protein_pdb = glob.glob('*.{}'.format(extension))
for n in pdb_files:
    name= n.split('.')[0]
    os.system('mkdir {}_str_files'.format(name))
    dst= os.getcwd() + "/{}_str_files/cGenFF/".format(name)
    charmmdst= os.getcwd() + "/{}_str_files/charmm36-jul2022.ff/".format(name)
    chrmm2gmxdst= os.getcwd() + "/{}_str_files/cgenff_charmm2gmx_py3_nx2.py".format(name)
    shutil.copytree(cGenFF, dst)
    shutil.copytree(charmm, charmmdst)
    shutil.copy(charmm2gmx, chrmm2gmxdst)
    shutil.copy(autosMD+n, dst)
    os.system(f"cp {sMD_need}/* {name}_str_files")
    os.system("cp /media/arma/DATA/S-Ehsan/Automate_sMD/RET_100_active/sMD/protein_pdb/{}_protein.pdb {}_str_files".format(name, name))
    os.chdir(dst)
    os.system(rf'python3 cGenFF_scraper.py')
    shutil.copyfile(dst+'strFiles/{}_unique_renumbered.str'.format(name), autosMD+"{}_str_files/{}_unique_renumbered.str".format(name, name))
    shutil.copyfile(dst+'mol2Files/{}_unique_renumbered.mol2'.format(name), autosMD+"{}_str_files/{}.mol2".format(name, name))    
    shutil.rmtree(autosMD + "/{}_str_files/cGenFF/".format(name))
    os.chdir(autosMD+"{}_str_files/".format(name))
    with open ('{}_unique_renumbered.str'.format(name),'r') as lig_name:
        lines=lig_name.read()
        resid= lines.split('\n')[16].split(' ')[1]
        lines= lines.replace(resid, 'UNK')
        liness= lines.split('\n')
        lines = [line for line in liness if "LP" not in line]
        lines= '\n'.join(lines) 
    with open ('{}.str'.format(name),'w') as new_lig:
        new_lig.write(lines)
    with open ('{}.mol2'.format(name),'r') as mol2:
        molline=mol2.read()
        molres= molline.split('\n')[1]
        molline= molline.replace(molres, 'UNK')
    os.system('rm {}.mol2'.format(name))
    with open ('{}.mol2'.format(name),'w') as new_mol:
        new_mol.write(molline)
    os.system("python cgenff_charmm2gmx_py3_nx2.py UNK {}.mol2 {}.str charmm36-jul2022.ff".format(name, name, name))
    os.system(f"gmx editconf -f unk_ini.pdb -o UNK.gro")
    os.system("gmx editconf -f {}_protein.pdb -resnr 1 -o {}_protein_new.pdb".format(name, name))
    command = "gmx pdb2gmx -f {}_protein_new.pdb -o {}_protein.gro -ignh".format(name,name)
    forcefield = '1' ## 1 for charmm all-atom force field 
    tip3p= '1' ## 1 for TIP3P CHARMM-modified TIP3P water model (recommended over original TIP3P)
    process = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(input=f'{forcefield}\n{tip3p}\n'.encode())
    if process.returncode != 0:
        print(f"Error: {error.decode()}")
    
    os.chdir(autosMD+"{}_str_files/".format(name))
    os.system("sed '$d' {}_protein.gro > complex.gro".format(name))
    os.system(f"grep UNK UNK.gro >> complex.gro")
    os.system("tail -n 1 {}_protein.gro >> complex.gro".format(name))
    with open ('complex.gro', 'r') as cmp:
        totallines = cmp.readlines()
        totalnum = len(totallines)
    totallines[1] = str(totalnum-3)+'\n'
    new_lines= ''.join(totallines)
    with open ('complex_new.gro', 'w') as duragam:
        duragam.write(new_lines)
    with open ('topol.top', 'r') as topol:
        topolline = topol.readlines()
    ligparam = topolline.index('#include "./charmm36-jul2022.ff/forcefield.itp"\n' )
    ligtopol = topolline.index('; Include water topology\n')
    new_topolline = topolline.copy()
    new_topolline.insert(ligparam+1, '\n; Include ligand parameters\n#include "unk.prm"\n')
    new_topolline.insert(ligtopol, '\n; Include ligand topology\n#include "unk.itp"\n')
    new_topolline.append('UNK                 1\n')
    new_topolline.append('')
    # os.system(f"rm topol.top")
    newtop= ' '.join(new_topolline)
    
    with open ('topol_new.top', 'w') as top:
        top.write(newtop)
    with open ('md_pull.mdp', 'r') as pull:
        pullline= pull.readlines()
    new_pullline= pullline.copy()
    last_element_list = new_pullline[-1].split()
    last_element_list[2] = str(args.kj)
    new_pullline[-1] = ' '.join(last_element_list)
    if args.axis == 'X':
        pull_dim = new_pullline[-5].split('=')
        pull_dim[1] =' Y N N\n'
        new_pullline[-5] = '='.join(pull_dim)
        pull_vec = new_pullline[-4].split('=')
        pull_vec[1] =' -1.0 0.0 0.0\n'
        new_pullline[-4] = '='.join(pull_vec)
    if args.axis == 'Y':
        pull_dim = new_pullline[-5].split('=')
        pull_dim[1] =' N Y N\n'
        new_pullline[-5] = '='.join(pull_dim)
        pull_vec = new_pullline[-4].split('=')
        pull_vec[1] =' 0.0 -1.0 0.0\n'
        new_pullline[-4] = '='.join(pull_vec)
    if args.axis == 'Z':
        pull_dim = new_pullline[-5].split('=')
        pull_dim[1] =' N N Y\n'
        new_pullline[-5] = '='.join(pull_dim)
        pull_vec = new_pullline[-4].split('=')
        pull_vec[1] =' 0.0 0.0 -1.0\n'
        new_pullline[-4] = '='.join(pull_vec)
    new_pullsave = ' '.join(new_pullline)
    with open ('md_pull_new.mdp' , 'w') as pullnew:
        pullnew.write(new_pullsave)
    if args.rotate is None :
        os.system(f"gmx editconf -f complex_new.gro -o newbox.gro -center {center}  -box {box}")
    else:
        os.system(f"gmx editconf -f complex_new.gro -o newbox.gro -rotate {rotate} -center {center}  -box {box}")
    os.system(f"gmx solvate -cp newbox.gro -cs spc216.gro -o solv.gro -p topol_new.top")
    os.system(f"gmx grompp -f ions.mdp -c solv.gro -p topol_new.top -o ions.tpr -maxwarn 1")
    command = "gmx genion -s ions.tpr -o solv_ions.gro -p topol_new.top -pname SOD -nname CLA -neutral -conc 0.1"
    solvent= '15'
    process = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(input=f'{solvent}\n'.encode())
    if process.returncode != 0:
        print(f"Error: {error.decode()}")

    os.chdir(autosMD+"{}_str_files/".format(name))
    os.system(f"gmx grompp -f em.mdp -c solv_ions.gro -p topol_new.top -r solv_ions.gro  -o em.tpr -maxwarn 2")
    os.system(f"gmx mdrun -v -deffnm em")
    os.system(f"gmx grompp -f npt.mdp -c em.gro -p topol_new.top -r em.gro -o npt.tpr -maxwarn 3")
    os.system(f"gmx mdrun -deffnm npt")
    command = "gmx make_ndx -f npt.gro"
    prot= '1'
    changeprot= 'name 19 Pro'
    lig= '13'
    changelig= 'name 20 Lig'
    quitee= 'q'
    process = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(input=f'{prot}\n{changeprot}\n{lig}\n{changelig}\n{quitee}\n'.encode())
    if process.returncode != 0:
        print(f"Error: {error.decode()}")
    os.chdir(autosMD+"{}_str_files/".format(name))
    os.system(f"gmx grompp -f md_pull_new.mdp -c npt.gro -p topol_new.top -r npt.gro -n index.ndx -t npt.cpt -o pull.tpr -maxwarn 2")
    os.system(f"gmx mdrun -deffnm pull -pf pullf.xvg -px pullx.xvg -v -nb gpu")
    os.chdir(autosMD)

