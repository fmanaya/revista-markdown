# -*- coding: utf-8 -*-
import re, PIL
from PIL import Image
#http://en.wikipedia.org/wiki/Help:Wiki_markup

#[[File:wiki.png|alt=Puzzle globe logo|title=Wikipedia Encyclopedia|cp=copyright]]

class mylinea(object):
    def __init__(self, l):
        self.lin = l.rstrip()
        self.charTrans();
        self.imagesTranslator()
        self.isEmpy = len(self.lin)
  
       
    def imagesTranslator(self):
        #m = re.search('\[\[(.+)\]\]', self.lin)
        p = re.compile('\[\[(.+)\]\]')
        m = p.match(self.lin)
        if m:
            #print ('Match found: '+ m.group(1))
            img = m.group(1).split('|')
            #for item in img:
            #    print (item)  
            # verifico imagen
            imgStart = img[0]
            if imgStart.startswith('File'):
                imgd = {}
                imgd['name'] = imgStart.split(':')[1]
                img1 = img[1]
                if img1.startswith('alt'):
                    imgd['alt'] = img1.split('=')[1]
                imgd[img[2].split('=')[0]] = img[2].split('=')[1]
                imgd[img[3].split('=')[0]] = img[3].split('=')[1]
                
                #http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
                try:
                    imgfs = '../data/IMAGENES{nrev}/{src}'.format(nrev=numrev, src=imgd['name'])
                    #print(imgfs)
                    im = Image.open(imgfs)
                except IOError:
                    print ("failed to identify" + imgfs)
                else:
                    #'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
                    newImgTpl = '<img src="/img/srbl{nrev}/{src}" class="imagen" width="{ancho}" height="{alto}" alt="{alt}" title="{title}" copyright="{copyright}">'
                    newImg = newImgTpl.format(nrev=numrev, src=imgd['name'], alt=imgd['alt'], title=imgd['title'], copyright=imgd['cp'],ancho=im.size[0], alto=im.size[1])
                    #print ("image format:" + im.format)
                    #print ("image mode:"+ im.mode)
                    #print ("image size:{ancho}x{alto}".format(ancho=im.size[0], alto=im.size[1]))
                    #if im.info.has_key("description"):
                        #print ("image description:" + im.info["description"])
                    #p = re.compile( '(blue|white|red)')
                    self.lin = p.sub( newImg, self.lin)                    
            else:
                print ('No match')                     
  
    # Aqui sustituyo caracteres feos
    def charTrans(self):
        self.lin = self.lin.replace('’', '')
        self.lin = self.lin.replace('´', '')
               
    def isHR(self):
        return self.lin.startswith('----')

    def fmt(self, wikimarckup, tag):
        return '<' + tag + '>' + self.lin.replace(wikimarckup, '') + '</' + tag + '>' + '\n' 
        
    def tipo(self):
        if self.isHR():
            return '<hr>' + '\n'    
        elif self.lin.startswith(':'):
            return self.fmt(':', 'blockquote')
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
        else:
            return '<p>' + self.lin + '</p>' + '\n'       
    def prn(self):
         return self.tipo().encode('utf-8')
    
    
numrev='153'
line_number = 0

f = open('../out/srbl-'+numrev+'.html', 'wb')


f.write(bytes('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">', 'UTF-8'))
f.write(bytes('<HTML><HEAD><meta http-equiv="Content-Type" content="text/html; charset=utf-8">', 'UTF-8'))
f.write(bytes('<TITLE>SERRABLO '+ numrev +'</TITLE>', 'UTF-8'))
f.write(bytes('</HEAD><BODY>', 'UTF-8'))

#f.write('')


    




with open('../data/serrablo153.txt', encoding='utf-8') as a_file:  
    for a_line in a_file:
        ln = mylinea(a_line);                                               
        line_number += 1
        #print(a_line)
        print('{:>4} {}'.format(line_number, a_line.rstrip()))
        # and at last convert it to utf-8
        #f.write(a_line.encode('utf-8'))
        if ln.isEmpy:
            f.write(ln.prn())
f.write(bytes('</BODY></HTML>', 'UTF-8'))      
f.close()



