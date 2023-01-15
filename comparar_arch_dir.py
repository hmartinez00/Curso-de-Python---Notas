import os
import filecmp
import pprint

fecha = ''

dir1 = r'C:\Users\Hector Martinez\Downloads\Telegram Desktop\Edilis Espinoza 18367802 (updated 20221005)' + '\\' + fecha
dir2 = r'C:\Users\Hector Martinez\Documents\Edilis Espinoza 18367802 (update 20221003)' + '\\' + fecha

dc = filecmp.dircmp(dir1, dir2)
# dc.report_full_closure()
# print(dc.common_dirs)

# file = 'comparacion.txt'

print('Common:')
pprint.pprint(dc.common)

print('\nLeft:')
pprint.pprint(dc.left_only)

print('\nRight:')
pprint.pprint(dc.right_only)

# f = open(file, 'w')
# f.write(string)
# f.close()