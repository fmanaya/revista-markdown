# -*- coding: utf-8 -*-
import PIL, sys, os
from PIL import Image

"""
Reglas:
Articulo pequeño:
    
"""

#http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio



class imagenRevista(object):
    



    def __init__(self, dirname, filename, importance):
        self.dirname = dirname
        self.filename = filename
        self.importance = importance
        self.im = Image
        self.imgweb = Image

    def getNewImageSize(self):
        return self.imgweb.size

    def _myresize(self):
        _sP = 'portrait'
        _sL = 'landscape'
        _PHI = 1.61803399
        
        """
        Parametros de redimensionado en función de shape e importancia
        """
        pixels = {
            'H-A': 600, 'H-M': 400, 'H-B': 250,   # shape Horizontal, se fija el ancho
            'V-A': 600, 'V-M': 400, 'V-B': 200    # shape Vertical, se fija el alto
            }
        
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
           
    
        clase='imagen'
        #Si el ratio es mayor que phi, la imagen va centrada, no tiene clase izqu ni dcha
        if rat > _PHI:
            noclase=True
            print ('proporcion mayor aurea, tiende a lo largo')
        else:
            print ('proporcion menor aurea, tiende a cuadradota')
    
        print(ancho, alto, shape, rat)
        print(nuevoAncho, nuevoAlto)
        # TODO: comprobar que no hago un resize para arriba 
        self.imgweb = self.im.resize((int(nuevoAncho), int(nuevoAlto)))

    def trataImg (self):
        dirout = self.dirname + '/web' 
        imagefileIn = self.dirname + '/' + self.filename
        imagefileOut = dirout + '/' + self.filename
        if not os.path.exists(dirout):
            os.makedirs(dirout)
    
        self.im = Image.open(imagefileIn)
        fout = os.path.splitext(imagefileOut)[0]+"_"+self.importance+".jpg"
        out = open(fout, "w")
        print ("\nTratsando: "+imagefileIn + " de importancia " + self.importance )
        print ("Creando: " + fout)    
        #save it into a file-like object
        self._myresize()
        self.imgweb.save(out, "JPEG", quality=80)
        

# imagenRevista

directory = '../data/IMAGENES153'


print ('\n\n\n')

images = (
         ('s153a2i1.jpg', 'M'),
         ('s153a2i2.jpg', 'M'),
         ('s153a2i3.jpg', 'M'),
         ('s153a3i1.jpg', 'M'),
         ('s153a4i1.jpg', 'M'),
         ('s153a5i1.jpg', 'M'),
         ('s153a5i2.jpg', 'M'),
         ('s153a5i3.TIFF', 'M'),
         ('s153a5i4.TIFF', 'M'),
         ('s153a5i5.tif', 'M'),
         ('s153a6i1.jpg', 'M'),
         ('s153a6i2.JPG', 'M'),
         ('s153a6i3.jpg', 'M'),
         ('s153a6i4.jpg', 'M'),
         ('s153a6i5.JPG', 'M'),
         ('s153a6i6.JPG', 'M'),
         ('s153a6i7.JPG', 'M'),
         ('s153a7i1.jpg', 'M'),
         ('s153a7i2.jpg', 'M'),
         ('s153a8i1.jpg', 'M'),
         ('s153a8i2.jpg', 'M'),
         ('s153a8i3.jpg', 'A'),
         ('s153a9i1.jpg', 'M')
      )

i=0
for img in images:
    i += 1
    imr = imagenRevista(directory, img[0], img[1])
    imr.trataImg()
    print (imr.getNewImageSize()[0])


