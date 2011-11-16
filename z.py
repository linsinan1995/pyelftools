# Just a script for playing around with pyelftools during testing
# please ignore it!
#

import sys, pprint
from elftools.elf.structs import ELFStructs
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import *

# read a little-endian, 64-bit file
es = ELFStructs(True, 64)

stream = open('tests/testfiles/penalty_64.o.elf', 'rb')
#stream = open('binfiles/z32.elf', 'rb')

efile = ELFFile(stream)
print 'elfclass', efile.elfclass
print '===> %s sections!' % efile.num_sections() 

#~ print efile.has_dwarf_info()

dwarfinfo = efile.get_dwarf_info()
print dwarfinfo.get_string_from_table(0x4bc0)
cu = dwarfinfo.get_CU(0)

print cu.structs.Dwarf_dw_form['DW_FORM_strp'].parse('\x01\x00\x00\x00\x01\x00\x00\x00')
print 'CU header', cu.header
topdie = cu.get_top_DIE()

print topdie

#~ print 'siblings.....'

#~ for s in c.iter_siblings():
    #~ print s

#~ from elftools.dwarf.location_expr import DW_OP_name2opcode, DW_OP_opcode2name

#~ print hex(DW_OP_name2opcode['DW_OP_lit14'])
#~ print DW_OP_opcode2name[0x0e]


