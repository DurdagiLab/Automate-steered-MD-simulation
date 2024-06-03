import os


class StrClearer:
    def __init__(self, resname):
        self.resname = resname
        os.makedirs('strFiles', exist_ok=True)
        for file in os.listdir(os.getcwd()):
            if file.endswith('.str'):
                with open(f'{file.replace(".str", "")}_clean.str', 'w') as destination:
                    with open(file, 'r') as f:
                        for line in f.readlines():
                            if "RESI" in line:
                                split_line = line.split()
                                new_line = split_line[0] + f" {self.resname} " + " ".join(split_line[2:])
                                destination.write(new_line + "\n")
                            else:
                                destination.write(line)
                os.system(f'mv {file.replace(".str", "")}_clean.str {file}')
                os.system(f'mv {file} strFiles')
