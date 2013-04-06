# -*- coding: utf-8 -*-
import sys, os
from PIL import Image

"""
Reglas:
Articulo pequeño:
    
"""

#http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio



class imagenRevista(object):
    paramsOk = True
    clase=''
    
    def __init__(self, dirname, filename, importance, position):
        self.dirname = dirname
        self.filename = filename
        self.filenameOut = filename.split('.')[0]+"_"+ importance+".jpg"
        self.filenameOutPeq = filename.split('.')[0]+"_"+ importance+"-peq.jpg"
        self.importance = importance
        self.position = position         # I-izqu, C-centro, D-dcha
        self.im = Image
        self.imgweb = Image
        if importance not in 'AMBP':
            self.paramsOk = False

    def getNewImageSize(self):
        if not self.paramsOk:
            return [50,50]
        return self.imgweb.size

    def _myresize(self):
        _sP = 'portrait'
        _sL = 'landscape'
        _PHI = 1.61803399
        
        """
        Parametros de redimensionado en función de shape e importancia
        A.-Alta
        M-Media
        B-Baja
        P-Poca
        """
        pixels = {
            'H-A': 700, 'H-M': 500, 'H-B': 300, 'H-P': 200,   # shape Horizontal, se fija el ancho
            'V-A': 550, 'V-M': 400, 'V-B': 300, 'V-P': 250    # shape Vertical, se fija el alto
        }
        imgpos = {'I':'izqu', 'C':'', 'D':'dcha'}
        
        ancho=self.im.size[0]
        alto=self.im.size[1]
        if ancho > alto:
            shape = 'H' #landscape
            rat = ancho / alto
            res = shape + '-' + self.importance
            nuevoAncho = pixels[res]
            # Calculo proporcionalmente el alto
            # si 
            nuevoAlto = alto * nuevoAncho / ancho
        else:
            rat = alto / ancho
            shape = 'V' #_sP
            res = shape + '-' + self.importance
            nuevoAlto = pixels[res]
            # Calculo proporcionalmente el ancho
            nuevoAncho = ancho * nuevoAlto / alto
           
    
        self.clase='imagen'
        #Si el ratio es mayor que phi, la imagen va centrada, no tiene clase izqu ni dcha
        if rat > _PHI:
            noclase = True
            print ('proporcion MAYOR aurea, tiende a lo largo')
        else:
            print ('proporcion MENOR aurea, tiende a cuadradota')
            #self.clase = self.clase+ " izqu"
        self.clase = self.clase + " " + imgpos[self.position]
    
        print('ancho={x}, alto={y}, shape={s}, rat={r}'.format(x=ancho, y=alto, s=shape, r=rat))
        print('nuevoAncho={x}, nuevoAlto={y}'.format(x=nuevoAncho, y=nuevoAlto))
        
        
        # TODO: comprobar que no hago un resize para arriba 
        if int(nuevoAncho) < int(ancho) and int(nuevoAlto) < int(alto):
            self.imgweb = self.im.resize((int(nuevoAncho), int(nuevoAlto)), Image.ANTIALIAS)
        else:
            print('NO RESIZE')
            self.imgweb = self.im
            


    """
    Si importancia=A y la imagen va posicionada I/D, se crean dos imagenes
            linoleo-larrede-jgavin-peq.jpg    250               326
            linoleo-larrede-jgavin.jpg        600               721 
    """
    def trataImg (self):
        if not self.paramsOk:
            self.imagefileOut="ERROR..."
            return
        self.dirout = self.dirname + '/web' 
        imagefileIn = self.dirname + '/' + self.filename
        self.imagefileOut = self.dirout + '/' + self.filenameOut
        if not os.path.exists(self.dirout):
            os.makedirs(self.dirout)
    
        self.im = Image.open(imagefileIn)
        
        #self.imagefileOut = os.path.splitext(imagefileOut)[0]+"_"+self.importance+".jpg"
        out = open(self.imagefileOut, "w")
        print ("\nTratando: "+imagefileIn + " de importancia " + self.importance + " y posicion " + self.position)
        print ("Creando: " + self.imagefileOut)    
        #save it into a file-like object
        self._myresize()
        self.imgweb.save(out, "JPEG", quality=80)
        #
        if self.importance=='A' and (self.position=='I' or self.position=='D'):
            # hago la pequeña que es la que se verá
            #self.imagefileOut = os.path.splitext(imagefileOut)[0]+"_"+self.importance+"-peq.jpg"
        
            imagefileOut2 = self.dirout + '/' + self.filenameOutPeq            
            
            print("Creando miniatura: " + imagefileOut2)
            self.importance='P'
            out = open(imagefileOut2, "w")
            print ("Tratando: "+imagefileIn + " de importancia " + self.importance )
            print ("Creando: " + imagefileOut2)    
            self._myresize()
            self.imgweb.save(out, "JPEG", quality=100)
            
            
            
        
        
        

# imagenRevista


