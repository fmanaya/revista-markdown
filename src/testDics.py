
"""
#Atributos
    File:s153a2i1.jpg    obligatorio
    alt=                 opcional
    title=Felipe III.    Obligsatorio
    cp=Velázquez         Opcional
    imp=                 Importancia, opcional, defecto M de media
"""
markup = 'File=s153a2i1.jpg|alt=|title=Felipe III.|cp=Velázquez|imp='

img = markup.split('|')

imgd = {}
imgd['imp']='M' # valor por defecto
for x in img:
    print(x)
    k=x.split('=')
    imgd[k[0]] = k[1]
    
print('\n')    
for key in imgd:
    print (key + ' corresponds to', imgd[key]  )  