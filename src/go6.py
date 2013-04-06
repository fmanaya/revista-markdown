# -*- coding: utf-8 -*-
import re, PIL, os, imgsRevista
from PIL import Image
from array import array

from mark3.markdown import markdown

#http://en.wikipedia.org/wiki/Help:Wiki_markup

#[[File:wiki.png|alt=Puzzle globe logo|title=Wikipedia Encyclopedia|cp=copyright]]

#class imagen(object):
#    imgd = {}
    
#    # valores es un array de key=value
#    def __init__(self, valores):
#        self.nombre = n


class mylinea(object):
    _logging=True   #True#False
    
    def debug(self, txt):
        if self._logging:
            print(str(self.linum) + ": " + txt)
        
    def __init__(self, n, l, linenum, runEnv):
        self.nrev = n
        self.linum = linenum
        self.lin = l.rstrip()
        self.charTrans();
        self.isEmpy = len(self.lin)    
        self.entorno = runEnv    
        self.imagesTranslator()
                        
       
    def imagesTranslator(self):
        #m = re.search('\[\[(.+)\]\]', self.lin)
        p = re.compile(r'\[\[(.+)\]\]')  
        p1 = re.compile('[\[\[(.+)\]\]]+')  
        
        m = p.search(self.lin)
        if m:
            self.debug ('Match found: '+ m.group(1))
            img = m.group(1).split('|')
            imgd = {'pos':'I'}
            imgd['alt']='' # valor por defecto
            imgd['imp']='M' # valor por defecto
            for x in img:
                #print(x)
                k=x.split('=')
                imgd[k[0]] = k[1]
            imgd['name']=imgd['File']    # por conveniencia...
            imgd['alt']=imgd['alt'].replace('"', '&quote;')
            imgd['title']=imgd['title'].replace('"', '\'')

            imgStart = img[0]
            self.debug('imgStart:'+imgStart)

            if imgStart.startswith('File'):

                # si alt no tiene nada pongo title + copyright
                if len(imgd['alt'])==0:
                    #alttext = imgd['alt'].replace('"', '&quote;')
                    imgd['alt']=imgd['title']
                    if len(imgd['cp']) > 0:
                        imgd['alt'] += ' - '+imgd['cp']

                #http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
                # try:
                    #imgfs = '../data/imgtratlargo480/IMAGENES{nrev}/{src}'.format(nrev=self.nrev, src=imgd['name'])
                    #self.debug(imgfs)
                    #im = Image.open(imgfs)
                    
                directory = '../data/IMAGENES' + self.nrev
                importancia = 'M' # media, por defecto
                if imgd['imp']:
                    importancia = imgd['imp']
                imr = imgsRevista.imagenRevista(directory, imgd['name'], imgd['imp'], imgd['pos'])
                imr.trataImg()
    
                # except IOError:
                #     self.debug ("failed to identify" + directory + imgd['name'])
                        
                #else:
                #'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
                path=''
                if self.entorno != 'local':
                    path='/img/srbl{nrev}/{src}'.format(nrev=self.nrev, src=imgd['name'])
                else:
                    path=imr.imagefileOut 
                
                # para debug, añado al title el nombnre de la imagen
                titdbg = imgd['title']
                if self.entorno == 'local':
                    titadded = "    [" + os.path.basename(imr.imagefileOut) + "]"
                    titdbg = titdbg + titadded    #imgd['name']    # para debug, añado el nombre de la imagen
                
                newImgTpl = '<img src="{ipath}" class="{clase}" width="{ancho}" height="{alto}" alt="{alt}" title="{title}" copyright="{copyright}">'
                newImg = newImgTpl.format(ipath=path, alt=imgd['alt'], title=titdbg, copyright=imgd['cp'],ancho=imr.getNewImageSize()[0], alto=imr.getNewImageSize()[1], clase=imr.clase)
                    
                self.lin = p.sub( newImg, self.lin)    
        else:
            self.debug ('No match')                     
      
    # Aqui sustituyo caracteres feos
    def charTrans(self):
        self.lin = self.lin.replace('’', '\'')
        self.lin = self.lin.replace('´', '\'')
        
        self.lin = self.lin.replace('“', '"')
        self.lin = self.lin.replace('”', '"')
        self.lin = self.lin.replace('‘', '\'')
        self.lin = self.lin.replace('’', '\'')
        self.lin = self.lin.replace('»', '&raquo;')
        self.lin = self.lin.replace('«', '&laquo;')
        self.lin = self.lin.replace('**', '<center>***</center>')
        self.lin = self.lin.replace('…', '...')
        
    def isHR(self):
        return self.lin.startswith('----')

    def fmt(self, wikimarckup, tag):
        if len(tag) > 0:
            return '<' + tag + '>' + self.lin.replace(wikimarckup, '') + '</' + tag + '>' + '\n'
        else:
            return self.lin.replace(wikimarckup, '') + '<br/>\n'    
        
    def prn(self):
        #return self.tipo().encode('utf-8')
        return self.lin.encode('utf-8')
    
class myRevista(object):
    def __init__(self, num, runto):
        self.numrev = num
        self.runto=runto
        
    def go(self):
        fname = '../outMark/srbl-' + self.numrev + '.html'
        print('writing: ' + fname)
        f = open(fname, 'wb')
        filelines=[]
        #http://www.penzilla.net/tutorials/python/fileio/
        filelines.append(bytes('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n', 'UTF-8'))
        filelines.append(bytes('<HTML>\n<HEAD>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">', 'UTF-8'))
        filelines.append(bytes('<TITLE>SERRABLO '+ self.numrev +'</TITLE>\n', 'UTF-8'))
        
        filelines.append(bytes('<link rel="stylesheet" type="text/css" href="srbl.css">\n', 'UTF-8'))
        
                 
        
        
        filelines.append(bytes('</HEAD>\n<BODY>', 'UTF-8'))
        
        line_number = 0
        
        with open('../data/serrablo'+self.numrev+'.txt', encoding='utf-8') as a_file:  
            for a_line in a_file:
                ln = mylinea(self.numrev, a_line, line_number, self.runto);                                               
                line_number += 1
                filelines.append(ln.prn()+ bytes('\n', 'UTF-8') )
        filelines.append(bytes('\n</BODY>\n</HTML>', 'UTF-8'))   
        allin=""
        for linea in filelines:
            allin += str(linea, encoding='utf8')
            
        #print (allin) 
        fhtml = markdown(allin)
        print (fhtml) 
        f.write (fhtml.encode(encoding='utf_8', errors='strict'))
        f.close()



nums = ['153','154','155','156','157','158']
nums = ['156']

# en este caso la ruta es la misma
runto='local'


for n in nums:
    print('----------------')
    print('processing ' + n)
    rev1 = myRevista(n, runto); 
    rev1.go()
    print(n + ' processed ')
    
print('FIN runnig to ' + runto)
print('')
print('')
print('')



