import sys
import collections


def renumPDB(pdbFile):
    prev_res = None
    element_idx = None

    for line_idx, line in enumerate(pdbFile):
        if line.startswith('HETATM'):
            element = line[76:78].strip()
            if not element:
                emsg = 'ERROR!! No element found in line {}'.format(line_idx)
                sys.stderr.write(emsg)
                sys.exit(1)
            resuid = line[17:27]
            if prev_res != resuid:
                prev_res = resuid
                element_idx = collections.defaultdict(lambda: 1)  # i.e. a counter
            spacer = ' ' if len(element) == 1 else ''
            name = (spacer + element + str(element_idx[element])).ljust(4)
            line = line[:12] + name + line[16:]
            element_idx[element] += 1

        yield line
