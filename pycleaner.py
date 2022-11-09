import os

def cleaner(__directorio__):
    AL1 = len(os.listdir(__directorio__))
    for __i__ in os.listdir(__directorio__):
        __archivo__ = __directorio__ + '\\' + __i__
        try:
            os.remove(__archivo__)
        except:
            continue
    AL2 = len(os.listdir(__directorio__))
    
    report = __directorio__ + \
    ' - Eliminados: {}'.format(AL2-AL1) + \
    ', Permanecen: {}'.format(AL1)

    print(report)

directorio = [
    r'C:\Windows\Prefetch',
    r'C:\Windows\Temp',
    r'C:\Users\admin\AppData\Local\Temp'
]

Reportes = []

for i in directorio:
    # Reportes.append(cleaner(i))
    cleaner(i)
 
# print(Reportes)