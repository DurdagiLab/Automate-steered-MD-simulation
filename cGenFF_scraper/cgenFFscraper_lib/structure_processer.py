import subprocess
from .pdb_unique import *
from .mol2_unique import *


def operatePDB(pdb):
    open_pdb = renumPDB(open(pdb, 'r'))
    new_pdb = open(str(pdb).replace(".pdb", "_unique.pdb"), 'w')
    resname = None
    try:
        _buffer = []
        _buffer_size = 5000  # write N lines at a time
        for line in open_pdb:
            if len(line) > 3:
                resname = line.split()[3]
                break
        for lineno, line in enumerate(open_pdb):
            if not (lineno % _buffer_size):
                _buffer = []
            _buffer.append(line)

        new_pdb.write(''.join(_buffer))
        new_pdb.close()
        open_pdb.close()
    except IOError:
        pass
    return resname


def operateMOL2(unique):
    subprocess.check_output(f'obabel ./pdbUnique/{unique} -o mol2 -O ./mol2Files/{unique.replace(".pdb", ".mol2")} ', shell=True)
    _FILEPATH = "mol2Files/" + str(unique.replace(".pdb", ".mol2"))
    mol2Renum = MOL2Reader()
    mol2Renum.CreateAtomCounters()
    mol2Renum.ChangeAtomsInMOL2()
    os.remove(_FILEPATH)
    os.system(f"mv *_renumbered.mol2 mol2Files")
    _RENUMBERED = "mol2Files/" + str(unique.replace(".pdb", "") + "_renumbered.mol2")
