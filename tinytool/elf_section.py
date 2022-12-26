import sys
import json
from elftools.elf.elffile import ELFFile
from collections import OrderedDict

class CodeSizeAnalyser:
    Prefix = ".text"
    def __init__ (self, filename):
        self.elffile = None
        self.f = open(filename, 'rb')
        self.text_sections = OrderedDict()

        assert self.f is not None
        self.elffile = ELFFile(self.f)

        assert self.elffile is not None
        text_sections = [sec for sec in self.elffile.iter_sections() if self.filter(sec)]
        text_sections = sorted(text_sections, key=lambda sec : sec.data_size, reverse=True)
        for i, sec in enumerate(text_sections):
            start = len(CodeSizeAnalyser.Prefix)+1
            self.text_sections[sec.name[start:]] = sec.data_size

    def __del__(self):
        if hasattr(self, 'f') and self.f:
            self.f.close()
   
    def filter(self, sec):
        return sec.name != CodeSizeAnalyser.Prefix \
                and sec.name.startswith(CodeSizeAnalyser.Prefix)

if __name__ == "__main__":
    # qrduino sglib-combined aha-mont64 picojpeg cubic statemate st wikisort nettle-aes slre nbody matmult-int tarfind minver ud edn primecount crc32 md5sum huffbench nettle-sha256 nsichneu
    if len(sys.argv) < 3:
        print("Usage:  python3 elf_section.py llvm test.elf")
        exit(0)
    tool = sys.argv[1]
    prefix="bd/src/"
    assert tool in ['gcc', 'llvm']
    size_dict = {}
    for arg in sys.argv[2:]:
        CA = CodeSizeAnalyser(f"{prefix}/{arg}/{arg}")
        size_dict[arg] = CA.text_sections
    data = json.dumps(size_dict, indent=4, separators=(',', ': '))
    with open(f"{tool}.detail.json", "w") as f:
        f.write(data)
