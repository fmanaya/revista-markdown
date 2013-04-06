# -*- coding: utf-8 -*-
import re, PIL
from PIL import Image
from array import array
#http://en.wikipedia.org/wiki/Help:Wiki_markup

#[[File:wiki.png|alt=Puzzle globe logo|title=Wikipedia Encyclopedia|cp=copyright]]

class mylinea(object):
    _logging=True   #True#False
    
    def debug(self, txt):
        if self._logging:
            print(str(self.linum) + ": " + txt)
        
    def __init__(self, n, l, linenum):
        self.nrev = n
        self.linum = linenum
        self.lin = l.rstrip()
        self.charTrans();
        self.imagesTranslator()
#        self.LinkTranslator()
        self.isEmpy = len(self.lin)
  
    # '''xxx''' ->   <em>xxx</em>
    def replaceWikiMarckup(self, expr):
        p = re.compile(expr)
        m = p.search(self.lin)
        if m:
            self.debug('Match found: ')
#            if m.group(0):
#                print(m.group(0))
#            if m.group(1):
#                print(m.group(1))
#            if m.group(2):
#                print(m.group(2))
            #  self.lin = p.sub( newImg, self.lin)
            #print(m.group(0))  
            #print(m.group(1))  
            #print(m.group(2))  
        else:
            self.debug ('No match found in for [' + expr+ '] in  ['+self.lin + ']')                     
       
       
#[[link:http://www.elmuseodeserrablo.blogspot.com|title=Blog del Museo Ángel Orensanz y Artes de Serrablo|text=blog|tipo=ext]] .       
#    def LinkTranslator(self):
        
       
    def imagesTranslator(self):
        #m = re.search('\[\[(.+)\]\]', self.lin)
        p = re.compile(r'\[\[(.+)\]\]')  
        p1 = re.compile('[\[\[(.+)\]\]]+')  
        
        m = p.search(self.lin)
        if m:
            self.debug ('Match found: '+ m.group(1))
            img = m.group(1).split('|')
            #for item in img:
            #    print (item)  
            # verifico imagen
            imgStart = img[0]
            self.debug(imgStart)
            if imgStart.startswith('File'):
                imgd = {}
                imgd['name'] = imgStart.split(':')[1]
                img1 = img[1]
                if img1.startswith('alt'):
                    alttext = img1.split('=')[1]
                    #print("ANTES:"+alttext)  
                    imgd['alt'] = alttext.replace('"', '&quote;')
                    #print("DESPUES:"+imgd['alt'])  
                    #imgd['alt'] = alttext #img1.split('=')[1]
                
                #title
                alttext = img[2].split('=')[1]
                alttext = alttext.replace('"', '\'')
                imgd[img[2].split('=')[0]] = alttext
                
                #copyright
                imgd[img[3].split('=')[0]] = img[3].split('=')[1]
                # si alt no tiene nada pongo title + copyright
                if len(imgd['alt'])==0:
                    #alttext = imgd['alt'].replace('"', '&quote;')
                    imgd['alt']=imgd['title']
                    if len(imgd['cp']) > 0:
                        imgd['alt'] += ' - '+imgd['cp']


                #http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
                try:
                    imgfs = '../data/imgtratlargo480/IMAGENES{nrev}/{src}'.format(nrev=self.nrev, src=imgd['name'])
                    self.debug(imgfs)
                    im = Image.open(imgfs)
                except IOError:
                    self.debug ("failed to identify" + imgfs)
                        
                else:
                    #'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
                    path=''
                    if runto!='local':
                        path='/img/srbl{nrev}/{src}'.format(nrev=self.nrev, src=imgd['name'])
                    else:
                        path=imgfs
                         
                    newImgTpl = '<img src="{ipath}" class="imagen" width="{ancho}" height="{alto}" alt="{alt}" title="{title}" copyright="{copyright}">'
                    newImg = newImgTpl.format(ipath=path, alt=imgd['alt'], title=imgd['title'], copyright=imgd['cp'],ancho=im.size[0], alto=im.size[1])
                    #print ("image format:" + im.format)
                    #print ("image mode:"+ im.mode)
                    #print ("image size:{ancho}x{alto}".format(ancho=im.size[0], alto=im.size[1]))
                    #if im.info.has_key("description"):
                        #print ("image description:" + im.info["description"])
                    #p = re.compile( '(blue|white|red)')
                    self.lin = p.sub( newImg, self.lin)    
            elif imgStart.startswith('Link'):
                self.debug("L   I   N   K                                 found....")
                #[[link:http://www.elmuseodeserrablo.blogspot.com|title=Blog del Museo Ángel Orensanz y Artes de Serrablo|text=blog|tipo=ext]] .       

                lnk = {}
                enlace = imgStart.split(':')
                lnk['src'] = enlace[1]+':'+enlace[2]
                #lnk['src'] = img[0].split('=')[1]
                lnk[img[1].split('=')[0]] = img[1].split('=')[1]
                lnk[img[2].split('=')[0]] = img[2].split('=')[1]
                lnk[img[3].split('=')[0]] = img[3].split('=')[1]
                self.debug("L   I   N   K:" + lnk['src'])
                self.debug("L   I   N   K:" + lnk['title'])
                self.debug("L   I   N   K:" + lnk['text'])
                self.debug("L   I   N   K:" + lnk['tipo'])
                
                newLnkTpl = '<a href="{src}" title="{title}">{texto}</a>'
                newLnk = newLnkTpl.format(src=lnk['src'], title=lnk['title'], texto=lnk['text'])

                self.lin = p.sub( newLnk, self.lin)                    
                
                
            else:
                self.debug ('No match')                     
  
    # Aqui sustituyo caracteres feos
    def charTrans(self):
        self.lin = self.lin.replace('’', '')
        self.lin = self.lin.replace('´', '')
        self.lin = self.lin.replace('“', '"')
        self.lin = self.lin.replace('”', '"')
        self.lin = self.lin.replace('‘', '"')
        self.lin = self.lin.replace('’', '"')
        self.lin = self.lin.replace('»', '&raquo;')
        self.lin = self.lin.replace('«', '&laquo;')
        self.lin = self.lin.replace('***', '<center>***</center>')

         
        
        
        self.lin = self.lin.replace('…', '...')
#        self.lin = self.lin.replace('\'\'', '<strong>')
#        self.lin = self.lin.replace('\'\'\'', '<em>')
        
        
               
    def isHR(self):
        return self.lin.startswith('----')

    def fmt(self, wikimarckup, tag):
        if len(tag) > 0:
            return '<' + tag + '>' + self.lin.replace(wikimarckup, '') + '</' + tag + '>' + '\n'
        else:
            return self.lin.replace(wikimarckup, '') + '<br/>\n'
         
        
    def tipo(self):
        if self.isHR():
            return '<hr>' + '\n'    
        elif self.lin.startswith(':'):
            return self.fmt(':', 'blockquote')
        elif self.lin.startswith('====='):  
            return self.fmt('=====', 'h5')
        elif self.lin.startswith('===='):
            #return '<h4>' + self.lin + '</h4>' + '\n'    
            return self.fmt('====', 'h4')
        elif self.lin.startswith('==='):
            #return '<h3>' + self.lin + '</h3>' + '\n'    
            return self.fmt('===', 'h3')
        elif self.lin.startswith('=='):
            #return '<h2>' + self.lin.replace('==','') + '</h2>' + '\n'    
            return self.fmt('==', 'h2')
        elif self.lin.startswith('* '):
            #return '<h2>' + self.lin.replace('==','') + '</h2>' + '\n'    
            return self.fmt('* ', 'li')
        elif self.lin.startswith('__'):
            #solo para no poner el parafo <p>
            return self.fmt('__', '')
        else:
            return '<p>' + self.lin + '</p>' + '\n'       
    def prn(self):
        return self.tipo().encode('utf-8')
    
class myRevista(object):
    def __init__(self, num):
        self.numrev = num

    def go(self):
        fname = '../out/srbl-' + self.numrev + '.html'
        print('writing: ' + fname)
        f = open(fname, 'wb')
        f.write(bytes('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">', 'UTF-8'))
        f.write(bytes('<HTML><HEAD><meta http-equiv="Content-Type" content="text/html; charset=utf-8">', 'UTF-8'))
        f.write(bytes('<TITLE>SERRABLO '+ self.numrev +'</TITLE>', 'UTF-8'))
        f.write(bytes('</HEAD><BODY>', 'UTF-8'))

        line_number = 0
        
        with open('../data/serrablo'+self.numrev+'.txt', encoding='utf-8') as a_file:  
            for a_line in a_file:
                ln = mylinea(self.numrev, a_line, line_number);                                               
                line_number += 1
                #print(a_line)
                #print('{:>4} {}'.format(line_number, a_line.rstrip()))
                # and at last convert it to utf-8
                #f.write(a_line.encode('utf-8'))
                if ln.isEmpy:
                    f.write(ln.prn())
        f.write(bytes('</BODY></HTML>', 'UTF-8'))      
        f.close()



nums = ['153','154','155','156','157','158']

# en este caso la ruta es la misma
runto='local'  


for n in nums:
    print('----------------')
    print('processing ' + n)
    rev1 = myRevista(n); 
    rev1.go()
    print(n + ' processed ')
    
print('FIN runnig to ' + runto)
print('')
print('')
print('')


ln = mylinea('000', "Hola ''caracola'', y [[corchetes]] adios",1);                                               
ln.replaceWikiMarckup('\'\'(.+)\'\'')
ln.replaceWikiMarckup("''(.+)''")


ln.replaceWikiMarckup("''.+''")
ln.replaceWikiMarckup("''[.+]''")
ln.replaceWikiMarckup("(.+)")

ln.replaceWikiMarckup("(.+)")

ln.replaceWikiMarckup("(a)")


n = re.compile(r"la", re.IGNORECASE)
print (n.findall('will match all words ''beginning with'' the letter w.'))

regex = re.compile("\[\[(.+)\]\]");
string="Hola [[File:s157a11i1.jpg|alt=|title=|cp=]] adios"
m=regex.search(string)
if m:
    print (m.group(0))
    print (regex.sub( 'kkkk', string))
else:
    print ('NO match')



m2 = regex.match(string)
if m2:
    print (m2.group(0))
else:
    print ('NO match')


#self.lin = p.sub( newImg, self.lin)    