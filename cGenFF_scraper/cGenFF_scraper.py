import os
from getpass import getpass

import cgenFFscraper_lib.structure_processer
import cgenFFscraper_lib.cGenFF_handler
import cgenFFscraper_lib.str_Cleaner


def main():
    pdbList = [pdb for pdb in os.listdir('.') if pdb.endswith('.pdb')]
    user = 'ehsansyh'
    #user = input('Please insert your cGenFF username or enter Q to quit: ')
    if user.lower() == 'q':
        exit()
    #print('Please input your password now: ')
    #psw = getpass()
    psw = 'Es@1373813s'
    os.makedirs('pdbUnique', exist_ok=True)
    resname = None
    for pdb in pdbList:
        resname = cgenFFscraper_lib.structure_processer.operatePDB(pdb)
    os.system(f"mv *_unique.pdb pdbUnique")
    del pdbList

    pdbUniques = [pdbUnique for pdbUnique in os.listdir('./pdbUnique')]
    os.makedirs('mol2Files', exist_ok=True)
    for unique in pdbUniques:
        try:
            cgenFFscraper_lib.structure_processer.operateMOL2(unique)
            _FILEPATH = ["./mol2Files/" + uniqueMol2 for uniqueMol2 in os.listdir('./mol2Files')][0]
            cgenFFscraper_lib.cGenFF_handler.cGenFF_handler(user, psw, _FILEPATH)
            cgenFFscraper_lib.str_Cleaner.StrClearer(resname)
        except RuntimeError:
            print("Molecule :", unique, "failed. Check if obabel produced a valid .mol2 file")


if __name__ == "__main__":
    main()
