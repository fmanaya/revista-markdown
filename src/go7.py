# -*- coding: utf-8 -*-
import re, os, imgsRevista, shutil
#from PIL import Image
#from array import array
        
from mark3.markdown import markdown

#md = markdown.Markdown(
#        extensions=['footnotes'], 
#        extension_configs= {'footnotes': [('PLACE_MARKER','~~~~~~~~')]},
#        safe_mode=True,
#        output_format='xhtml1'
#)



#http://en.wikipedia.org/wiki/Help:Wiki_markup

#[[File:wiki.png|alt=Puzzle globe logo|title=Wikipedia Encyclopedia|cp=copyright]]

#class imagen(object):
#    imgd = {}
    
#    # valores es un array de key=value
#    def __init__(self, valores):
#        self.nombre = n




class mylinea(object):
    _logging=True   #True#False
    isParagraph=True
    def debug(self, txt):
        if self._logging:
            print(str(self.linum) + ": " + txt)
        
    def __init__(self, n, l, linenum, runEnv, processImg):
        self.nrev = n
        self.linum = linenum

        self.trata(l)
#        self.lin = l.rstrip()#
        
        
#       <span class="piepag"> </span>
        self.namesAdS()
        self.charTrans()
        self.isEmpty = len(self.lin)    
        self.entorno = runEnv    
        self.processImg = processImg    
        if processImg:
            self.imagesTranslator()
                      
    # otros tratamientos                    
    def trata(self,l):
        self.lin = l   #.rstrip()
        
        #tto para BR        
        if self.lin.endswith("   \n"):
            self.isParagraph = False
            
                       
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
            #imgd['alt']=imgd['alt'].replace('"', '&quote;')
            #imgd['title']=imgd['title'].replace('"', '\'')
            imgd['alt']=html.escape(imgd['alt'])
            imgd['title']=html.escape(imgd['title'])


            imgStart = img[0]
            self.debug('imgStart:'+imgStart)

            if imgStart.startswith('File'):

                # si alt no tiene nada pongo title + copyright
                if len(imgd['alt'])==0:
                    #alttext = imgd['alt'].replace('"', '&quote;')
                    imgd['alt']=imgd['title']
                    if len(imgd['cp']) > 0:
                        imgd['alt'] += ' - '+imgd['cp']

                directory = '../data/IMAGENES' + self.nrev

                imr = imgsRevista.imagenRevista(directory, imgd['name'], imgd['imp'], imgd['pos'])
                imr.trataImg()
    
                # except IOError:
                #     self.debug ("failed to identify" + directory + imgd['name'])
                        
                #else:
                #'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
                path=''
                if self.entorno != 'local':
                    path='/img/srbl{nrev}/{src}'.format(nrev=self.nrev, src=imr.filenameOut  )
                    #imgd['name'])
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
#        else:
#            self.debug ('No match')                     
      
    # aqui cadenas ad-oc
    def namesAdS(self):
        if not self.lin.startswith("##"):
            self.lin = self.lin.replace('Museo de Dibujo “Julio Gavín-Castillo de Larrés”', '%MDJGCL%')
            self.lin = self.lin.replace('Museo de Dibujo “Julio Gavín”-Castillo de Larrés', '%MDJGCL%')
            self.lin = self.lin.replace('Museo de Dibujo Julio Gavín-Castillo de Larrés', '%MDJGCL%')
            self.lin = self.lin.replace('Museo de Dibujo “Julio Gavín-Castillo de Larrés”', '%MDJGCL%')
            self.lin = self.lin.replace('Museo de Dibujo “Julio Gavín. Castillo de Larrés”', '%MDJGCL%')
            self.lin = self.lin.replace('Museo de Dibujo', '%MDCL%')
            
            self.lin = self.lin.replace('Ayuntamiento de Sabiñánigo', '%AYTOSABI%') 
            self.lin = self.lin.replace('Instituto de Estudios Altoaragoneses', '%IEA%') 
            self.lin = self.lin.replace('Comarca Alto Gállego', '%CAG%') 
            self.lin = self.lin.replace('Museo de Artes Populares de Serrablo', '%MAPS%') 
            self.lin = self.lin.replace('Museo de Serrablo', '%MAPS%') 
            self.lin = self.lin.replace('Gobierno de Aragón', '%GdA%') 
            self.lin = self.lin.replace('Real Academia de las Nobles y Bellas Artes de San Luis', '<a href="http://www.rasanluis.es/">Real Academia de las Nobles y Bellas Artes de San Luis</a>') 
            
            
            
            
            
          
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
        crlf=""
        if not self.isParagraph:
            crlf = "<BR />" 
        lin = self.lin.encode('utf-8')
        return lin.rstrip() + bytes(crlf, 'UTF-8') + bytes('\n', 'UTF-8')
    
    
def art( item ):
#    print(item)
#    key_pat = re.compile( r"s161a(\d+)i\d" )
    regex = r"s161a(\d+)i\d"
    m = re.findall (regex, item )
    if len(m)==0:
        return 0
#    print(m)
    return int(m[0])
    
class myRevista(object):
    def __init__(self, num, runto, processImg):
        self.numrev = num
        self.runto=runto
        self.processImg=processImg
        
    def imagenes(self):
        dirimg='..\data\IMAGENES'+ self.numrev
        files = []
        files = os.listdir(dirimg)       
        for file in sorted(files, key=art):
            img = os.path.join(dirimg, file)
            if os.path.isfile(img):
                print('[[File={i}|alt=|title=|cp=|imp=B|pos=D]]'.format(i=file))
    
    def go(self):
        # vacio el directrorio de imagenes si existe
        dirimg='..\data\IMAGENES'+ self.numrev +'\web'
        if (processImg and os.path.exists(dirimg)):
            shutil.rmtree(dirimg)

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
                ln = mylinea(self.numrev, a_line, line_number, self.runto, self.processImg);                                               
                line_number += 1
                filelines.append(ln.prn() )
                # Si es un título, pongo la url
                # ## <a name="a2"/>Arrieros en el Alto Gállego: Éramos pocos… y llegó el ferrocarril (III)
                h2markup = "## "
                lintratada = a_line #.rstrip()
                        
                # construye la url        
                if lintratada.startswith(h2markup):
                    strtmp1 = lintratada.replace(h2markup, "").rstrip()
                    # busco >
                    inicio = strtmp1.find (">") + 1
                    #>>> x[2:]
                    #'llo World!'
                    res = strtmp1[inicio:]
                    #filelines.append(bytes(res + "\n", 'UTF-8'))
                    print ("*********************************************************") 
                    print ("strtmp1" + strtmp1) 
                    #print ("inicio" + inicio) 
                    print ("inicio= %d", inicio )
                    res = res.lower()
                    res = res.replace(" ", "-")
                    res = res.replace(":", "-")
                    res = res.replace("á", "a")
                    res = res.replace("é", "e")
                    res = res.replace("í", "i")
                    res = res.replace("ó", "o")
                    res = res.replace("ú", "u")
                    res = res.replace("ú", "u")
                    res = res.replace(".", "")
                    res = res.replace("(", "")
                    res = res.replace(")", "")
                    res = res.replace("“", "")
                    res = res.replace("”", "")
                    
                    # quito los dobles que puedan quedar
                    res = res.replace("--", "-").replace("--", "-")
                    
                    
                    #print (res10) 
                    filelines.append(bytes('revista/'+self.numrev+'/'+res + "\n", 'UTF-8'))
                 
        filelines.append(bytes('\n</BODY>\n</HTML>', 'UTF-8'))   
        allin=""
        for linea in filelines:
            allin += str(linea, encoding='utf8')
            
        #print (allin) 
        #return md.convert(some_text)
        fhtml = markdown(allin)
        print (fhtml) 
        f.write (fhtml.encode(encoding='utf_8', errors='strict'))
        f.close()



numskk = ['153','154','155','156','157','158']
nums = ['159','160','161']
numsk = ['161']

numsTest = ['999']

# en este caso la ruta es la misma (filesystem) ../data/IMAGENES... y ademas se escriben trazas (nombre imagen en titulo...
runto='local'
# o relativa en la web /img/srblnnn
#runto='deploy'

processImg=True

for n in nums:
    print('----------------')
    print('processing ' + n)
    rev1 = myRevista(n, runto, processImg); 
    rev1.go()
    print(n + ' processed ')
    rev1.imagenes()
    
print('FIN runnig to ' + runto)
print('')
print('')
print('')



